from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailagendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wagtailagenda'
    verbose_name = _('WagtailAgenda')
