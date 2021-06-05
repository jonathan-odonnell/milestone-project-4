from holidays.views import holidays
from django.http import response
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import UserProfile
from holidays.models import Package
from .forms import UserProfileForm
from .views import profile
from datetime import datetime, date
from pytz import timezone
import pytz


class TestProfilesViews(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

        self.client.login(
            email=self.user.email,
            password='Password',
        )

        self.holiday = Package.objects.create(
            name='Test Holiday',
            image='testimage.jpg',
            description='Test description',
            offer=True,
            price=499,
            duration=14,
            catering='Full Board',
            transfers_included=True
        )

        """
        Code for adding the flights related object is from 
        https://docs.djangoproject.com/en/3.2/ref/models/relations/
        """
        self.holiday.flights.create(
            flight_number='ZZ001',
            origin='Test Airport',
            destination='Test Airport',
            departure_time=datetime(2021, 6, 1, 12, tzinfo=pytz.utc),
            origin_time_zone=timezone('Europe/London'),
            arrival_time=datetime(2021, 6, 2, 18, 12, tzinfo=pytz.utc),
            destination_time_zone=timezone('Europe/London'),
            baggage=20
        )

        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.bookings.create(
            package=self.holiday,
            guests=2,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            outbound_flight=self.holiday.flights.first(),
            return_flight=self.holiday.flights.first(),
            paid=True,
        )

    def test_get_profile_page(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_can_update_profile(self):
        response = self.client.post('/profile/', {
            'email_address': 'testuser@test.com',
            'street_address1': 'Test',
            'town_or_city': '',
            'county': '',
            'country': 'GB',
            'post_code': ''
        })
        self.assertEqual(response.status_code, 200)
        profile_qs = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile_qs.user.email, 'testuser@test.com')
        self.assertEqual(profile_qs.street_address1, 'Test')
        self.assertEqual(profile_qs.country, 'GB')

    def test_get_bookings_page(self):
        response = self.client.get('/profile/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/bookings.html')

    def test_get_booking_details_page(self):
        response = self.client.get(
            f'/profile/bookings/{self.user_profile.bookings.first().booking_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')


class TestProfilesForm(TestCase):
    def test_only_email_address_field_required(self):
        form = UserProfileForm({
            'email_address': '',
            'phone_number': '',
            'street_address1': '',
            'town_or_city': '',
            'county': '',
            'country': '',
            'postcode': '',
        })
        self.assertEqual(form.errors['email_address']
                         [0], 'This field is required.')

    def test_invalid_email_address(self):
        form = UserProfileForm({
            'email_address': 'Not an email address',
            'phone_number': '',
            'street_address1': '',
            'town_or_city': '',
            'county': '',
            'country': '',
            'postcode': '',
        })
        self.assertEqual(form.errors['email_address']
                         [0], 'Enter a valid email address.')

    def test_excluded_in_form_metaclass(self):
        form = UserProfileForm()
        self.assertEqual(form.Meta.exclude, ('user', 'stripe_customer_id'))


class TestProfilesModel(TestCase):
    def test_string_method_returns_flight_number(self):
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Password',
            first_name='Test',
            last_name='User',
        )
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(user_profile), 'Test User')
