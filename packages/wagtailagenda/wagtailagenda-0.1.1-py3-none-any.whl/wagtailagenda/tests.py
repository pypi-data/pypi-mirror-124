from django.test import TestCase
from django.contrib.auth.models import User

from datetime import (
    datetime,
    timedelta,
)

from wagtail.core.models import Page
from wagtailagenda.models import (
    Agenda,
    Activity,
    ActivityLocation,
)


class AgendaTestCase(TestCase):
    """Test the agenda custom code"""
    def setUp(self):
        """Set up the database"""
        # Create a test user to be owner of the pages
        self.user = User.objects.create_user('test', 'test@test.test', 'pass')
        # First, get the home page
        self.home = Page.objects.get(slug='home')
        # Create a location for the teste
        self.location = ActivityLocation(
            name='Location for test',
        )
        self.location.save()
        # Create an agenda
        self.agenda = Agenda(
            title='Test agenda',
            slug='test_agenda',
            owner=self.user,
            live=True,
        )
        self.home.add_child(
            instance=self.agenda
        )
        self.agenda.save()
        # Create 2 actitivies for the agenda: One passed and one
        # future
        now = datetime.now()
        self.passed_activity = Activity(
            title='Passed activity',
            begin=now-timedelta(days=3, hours=2),
            end=now-timedelta(days=3),
            location=self.location,
            slug='passed_activity',
            owner=self.user,
            live=True,
        )
        self.agenda.add_child(instance=self.passed_activity)
        self.agenda.save()
        self.passed_activity.save()
        self.future_activity = Activity(
            title='Future activity',
            begin=now+timedelta(days=3),
            end=now+timedelta(days=3, hours=2),
            location=self.location,
            slug='future_activity',
            owner=self.user,
            live=True,
        )
        self.agenda.add_child(instance=self.future_activity)
        self.agenda.save()
        self.future_activity.save()

    def test_activities(self):
        """Test the activities method"""
        # When archives are not enabled
        self.agenda.archives_enabled = False
        self.agenda.save()

        # Get the agenda activities
        activities = self.agenda.activities()

        # We should found our 2 activities
        self.assertTrue(
            self.passed_activity in activities,
            msg='Passed activity not found in agenda activities()',
        )
        self.assertTrue(
            self.future_activity in activities,
            msg='Future activity not found in agenda activities()',
        )
        self.assertEqual(
            len(activities),
            2,
            msg='Agenda activities() should return only 2 activities',
        )

        # When archives are enabled
        self.agenda.archives_enabled = True
        self.agenda.save()

        # Get the agenda activities
        activities = self.agenda.activities()
        
        # We should found only the future activity
        self.assertTrue(
            self.passed_activity not in activities,
            msg='Passed activity found in agenda activities()',
        )
        self.assertTrue(
            self.future_activity in activities,
            msg='Future activity not found in agenda activities()',
        )
        self.assertEqual(
            len(activities),
            1,
            msg='Agenda activities() should return only 1 activity',
        )

    def test_archived_activities(self):
        """Test the archived_activities() methode of the agenda"""
        # When archives are not enabled
        self.agenda.archives_enabled = False
        self.agenda.save()

        # Get the achived activities
        archived_activities = self.agenda.archived_activities()

        # We should found no actitivies
        self.assertEqual(
            len(archived_activities),
            0,
            msg='Agenda archived_activities() should return no activity',
        )

        # When archives are enabled
        self.agenda.archives_enabled = True
        self.agenda.save()

        # Get the achived activities
        archived_activities = self.agenda.archived_activities()

        # We should found only the passed actitivies
        self.assertTrue(
            self.passed_activity in archived_activities,
            msg='Passed activity not found in agenda activities()',
        )
        self.assertTrue(
            self.future_activity not in archived_activities,
            msg='Future activity found in agenda activities()',
        )
        self.assertEqual(
            len(archived_activities),
            1,
            msg='Agenda activities() should return only 1 activity',
        )

    def test_ics(self):
        """Test the .ics() method"""
        # Get the ICS agenda
        self.agenda.archives_enabled = True
        self.agenda.save()
        ics_agenda = self.agenda.ics()

        # Chek that the future activity are in the ics
        ics_event = list(ics_agenda.events)[0]
        self.assertEqual(
            ics_event.name,
            self.future_activity.title,
        )
        self.assertEqual(
            ics_event.begin.naive,
            self.future_activity.begin,
        )
        self.assertEqual(
            ics_event.end.naive,
            self.future_activity.end,
        )
        self.assertEqual(
            ics_event.description,
            self.future_activity.description,
        )
        self.assertEqual(
            ics_event.url,
            self.future_activity.get_full_url(),
        )


class ActivityLocationTestCase(TestCase):
    """Test the ActivityLocation mothodes"""

    def test_has_address(self):
        """Test if has_address() method work"""
        # Create an ActivityLocation without an address
        activity_with_no_address = ActivityLocation(
            name='Test with no address',
        )

        # Create an ActivityLocation with an address
        activity_with_address = ActivityLocation(
            name='Test with address',
            street='Test street',
            street_number='19B',
            zip='00A',
            city='No city',
            country='No country',
        )

        # Create an ActivityLocation with a partial address
        activity_with_partial_address = ActivityLocation(
            name='Test with address',
            street='Test street',
            street_number='19B',
        )

        # Check that the ActivityLocation without an address return
        # False to .has_address()
        self.assertFalse(
            activity_with_no_address.has_address()
        )

        # Check that the ActivityLocation with an address return True
        # to .has_address()
        self.assertTrue(
            activity_with_address.has_address()
        )

        # Check that the ActivityLocation with a partial address
        # return True to .has_address()
        self.assertTrue(
            activity_with_partial_address.has_address()
        )
