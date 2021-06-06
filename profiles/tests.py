from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from .models import UserProfile
from holidays.models import Package
from .forms import UserProfileForm, CustomSignupForm
from datetime import datetime, date
from pytz import timezone
import pytz


class TestProfilesViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

        # https://stackoverflow.com/questions/29721360/django-test-with-allauth
        current_site = Site.objects.get_current()

        current_site.socialapp_set.create(
            provider="facebook",
            name="facebook",
            client_id="1234567890",
            secret="0987654321",
        )

        current_site.socialapp_set.create(
            provider="google",
            name="google",
            client_id="1234567890",
            secret="0987654321",
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

        self.user.userprofile.bookings.create(
            package=self.holiday,
            guests=2,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            outbound_flight=self.holiday.flights.first(),
            return_flight=self.holiday.flights.first(),
            paid=True,
        )

    def test_get_anonymous_user_profile_page(self):
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_get_logged_in_profile_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_can_update_profile(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.post('/profile/', {
            'email_address': 'testuser@test.com',
            'street_address1': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test'
        })
        self.assertEqual(response.status_code, 200)
        profile_qs = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile_qs.user.email, 'testuser@test.com')
        self.assertEqual(profile_qs.street_address1, 'Test')
        self.assertEqual(profile_qs.town_or_city, 'Test')
        self.assertEqual(profile_qs.county, 'Test')
        self.assertEqual(profile_qs.country, 'GB')
        self.assertEqual(profile_qs.postcode, 'Test')

    def test_anonymous_user_get_bookings_page(self):
        response = self.client.get('/profile/bookings/')
        self.assertRedirects(
            response, '/accounts/login/?next=/profile/bookings/')

    def test_logged_in_user_get_bookings_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/profile/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/bookings.html')

    def test_anonymous_user_get_booking_details_page(self):
        response = self.client.get(
            f'/profile/bookings/{self.user.userprofile.bookings.first().booking_number}/')
        self.assertRedirects(
            response, f'/accounts/login/?next=/profile/bookings/{self.user.userprofile.bookings.first().booking_number}/')

    def test_logged_in_user_get_booking_details_page(self):
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(
            f'/profile/bookings/{self.user.userprofile.bookings.first().booking_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')


class TestProfilesForms(TestCase):
    def test_user_profile_form_email_address_field_required(self):
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

    def test_user_profile_form_invalid_email_address(self):
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

    def test_user_profile_form_excluded_in_metaclass(self):
        form = UserProfileForm()
        self.assertEqual(form.Meta.exclude, ('user', 'stripe_customer_id'))

    def test_custom_signup_form_all_fields_required(self):
        form = CustomSignupForm({
            'first_name'
            'last_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        })
        self.assertEqual(form.errors['first_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['last_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['email']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['password1']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['password2']
                         [0], 'This field is required.')


class TestProfilesModels(TestCase):
    def test_user_profile_string_method_returns_flight_number(self):
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Password',
            first_name='Test',
            last_name='User',
        )
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(user_profile), 'Test User')
