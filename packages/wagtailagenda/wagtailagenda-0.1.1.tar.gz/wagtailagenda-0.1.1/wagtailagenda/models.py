from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.contrib.routable_page.models import (
    RoutablePageMixin,
    route,
)
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtailperson.models import Person

import ics

@register_snippet
class ActivityLocation(index.Indexed, ClusterableModel):
    """The location of an activity"""
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )
    street_name = models.CharField(
        max_length=255,
        verbose_name=_('street name'),
        blank=True,
    )
    street_number = models.CharField(
        max_length=5,
        verbose_name=_('street number'),
        blank=True,
    )
    zip_code = models.CharField(
        max_length=255,
        verbose_name=_('zip'),
        blank=True,
    )
    city = models.CharField(
        max_length=255,
        verbose_name=_('city'),
        blank=True,
    )
    country = models.CharField(
        max_length=255,
        verbose_name=_('country'),
        blank=True,
    )
    floor = models.CharField(
        max_length=255,
        verbose_name=_('floor'),
        blank=True,
    )
    OSM_url = models.URLField(
        max_length=255,
        verbose_name=_('OpenStreetMap URL'),
        blank=True,
    )

    pannels = [
        FieldPanel('name'),
        FieldPanel('description'),
        MultiFieldPanel(
            children=(
                FieldPanel('street_name'),
                FieldPanel('zip_code'),
                FieldPanel('city'),
                FieldPanel('country'),
                FieldPanel('floor'),
            ),
            heading=_('Address')
        ),
        FieldPanel('OSM_url'),
        InlinePanel(
            'public_transport_stops',
            label=_('Public transport stops'),
        ),
    ]

    serch_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('street_name', partial_match=True),
        index.SearchField('NPA', partial_match=True),
        index.SearchField('city', partial_match=True),
        index.SearchField('country', partial_match=True),
        index.SearchField('description', partial_match=True),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Activity location')
        verbose_name_plural = _('Activity locations')
        ordering = ['name']

    def has_address(self):
        """Return True if this location have an address, else False"""
        return any(
            (
                self.street_name,
                self.street_number,
                self.zip_code,
                self.city,
                self.country,
            )
        )


class PublicTransportStop(Orderable, models.Model):
    """A public transport stop"""
    name = models.CharField(
        max_length=255,
        verbose_name=_('type'),
    )
    type = models.CharField(
        max_length=20,
        verbose_name=_('type'),
    )
    line_number = models.CharField(
        max_length=20,
        verbose_name=_('line number'),
    )
    location = ParentalKey(
        ActivityLocation,
        on_delete=models.CASCADE,
        related_name='public_transport_stops',
    )

    pannels = [
        FieldPanel('name'),
        FieldPanel('type'),
        FieldPanel('line_number'),
    ]

    
    def __str__(self):
        return f'{self.type} {self.line_number}: {self.name}'
    
    class Meta:
        verbose_name = _('Public Transport Stop')
        verbose_name_plural = _('Public Transport Stops')
        ordering = ['name']


class Activity(Page):
    """An activity, to be added to an agenda"""
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )
    begin = models.DateTimeField(
        verbose_name=_('begin on'),
    )
    end = models.DateTimeField(
        verbose_name=_('end on'),
    )
    location = models.ForeignKey(
        ActivityLocation,
        on_delete=models.CASCADE,
        verbose_name=_('where'),
    )
    organizers = models.ManyToManyField(
        Person,
        verbose_name=_('organizers'),
    )
    program = RichTextField(
        verbose_name=_('program of the activity'),
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('organizers'),
        MultiFieldPanel(
            children=(
                FieldPanel('begin'),
                FieldPanel('end'),
            ),
            heading=_('when')
        ),
        FieldPanel('location'),
        FieldPanel('program'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('program'),
        index.FilterField('organizers'),
        index.FilterField('location'),
    ]

    subpage_types = []

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ['begin', 'end', 'title']

    def __str__(self):
        return self.title


class Agenda(RoutablePageMixin, Page):
    """An agenda"""

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )
    archives_enabled = models.BooleanField(
        default=False,
        verbose_name=_('archives_enabled'),
        help_text=_(
            'Each passed activities will be shown on a ./archives page'
        ),
    )

    settings_panels = Page.settings_panels + [
        FieldPanel('archives_enabled'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]
    
    subpage_types = ['wagtailagenda.Activity']

    class Meta:
        verbose_name = _('Agenda')
        verbose_name_plural = _('Agendas')
        ordering = ['title']

    def activities(self):
        """Return the activities of the agenda"""
        if self.archives_enabled:
            now = datetime.now()
            return Activity.objects.descendant_of(
                self
            ).order_by('begin').filter(
                end__date__gte=now,
            ).live().public()
        else:
            return Activity.objects.descendant_of(
                self
            ).order_by('begin').live().public()

    def archived_activities(self):
        """Return the archived activities of the agenda"""
        if self.archives_enabled:
            now = datetime.now()
            return Activity.objects.descendant_of(
                self
            ).live().public().order_by('begin').filter(
                end__date__lt=now,
            )
        else:
            return []

    def ics(self):
        # Create the ICS agenda
        ics_agenda = ics.Calendar()
        for activity in self.activities():
            ics_agenda.events.add(
                ics.Event(
                    name=activity.title,
                    begin=activity.begin,
                    end=activity.end,
                    description=activity.description,
                    location=activity.location.name,
                    organizer=','.join(
                        (orginizer.name
                         for orginizer in activity.organizers.all())
                    ),
                    url=activity.get_full_url(),
                )
            )
        return ics_agenda

    def __str__(self):
        self.title

    def get_context(self, request, archives=False):
        """Overload the context building to include all children activities"""
        context = super(Agenda, self).get_context(request)
        context['is_archives'] = archives
        if archives:
            context['activities'] = self.archived_activities()
        else:
            context['activities'] = self.activities()
        return context

    @route(r'^archives/$', name='archives')
    def archived_activities_subpage(self, request):
        """The subpage that show the archived activities"""
        context = self.get_context(request, archives=True)
        return render(request, self.template, context)

    @route(r'^webcal/$', name='webcal')
    def webcal_subpage(self, request):
        """The subpage that provide the agenda ICS file"""
        return HttpResponse(
            str(self.ics()),
            headers={
                'Content-Type': 'text/calendar',
                'Content-Disposition': 'attachment; filename="webcal.ics"',
            },
        )
