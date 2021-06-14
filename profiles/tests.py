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
        """
        Sets up the user, email address, site, social apps, holiday, flight
        and user profile. Code for creating the user is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/,
        code for creating the email address is from
        https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py,
        code for creating the site and social apps is from
        https://stackoverflow.com/questions/29721360/django-test-with-allauth,
        code for creating the flight is from
        https://docs.djangoproject.com/en/3.2/ref/models/relations/
        and code for creating the user profile is from
        https://stackoverflow.com/questions/11088901/django-onetoone-reverse-access
        """
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
        )

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
        """
        Verifies that an anonymous user is redirected to the login page
        when they try and access the profile page.
        """
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_get_logged_in_profile_page(self):
        """
        Logs in the user and verifies that a status of 200 is returned and
        the profile template was used when they try and access the profile
        page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_can_update_profile(self):
        """
        Logs in the user and verifies that a status of 200 is returned,
        the bookings template was used and the user's profile is updated
        in the database when a post request with valid profile details is
        submitted to the profile page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
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
        """
        Verifies that an anonymous user is redirected to the login page
        when they try and access the bookings page.
        """
        response = self.client.get('/profile/bookings/')
        self.assertRedirects(
            response, '/accounts/login/?next=/profile/bookings/')

    def test_logged_in_user_get_bookings_page(self):
        """
        Logs in the user and verifies that a status of 200 is returned and
        the bookings template was used when they try and access the bookings
        page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get('/profile/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/bookings.html')

    def test_anonymous_user_get_booking_details_page(self):
        """
        Verifies that an anonymous user is redirected to the login page
        when they try and access the booking details page. Code for the
        first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        response = self.client.get(
            f'/profile/bookings/\
                {self.user.userprofile.bookings.first().booking_number}/')
        self.assertRedirects(
            response, f'/accounts/login/?next=/profile/bookings/\
                {self.user.userprofile.bookings.first().booking_number}/')

    def test_logged_in_user_get_booking_details_page(self):
        """
        Logs in the user and verifies that a status of 200 is returned and
        the checkout success template was used when they try and access the
        booking details page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        and code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.get(
            f'/profile/bookings/\
            {self.user.userprofile.bookings.first().booking_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')


class TestProfilesForms(TestCase):
    """Tests the email address field is required in the extra form"""
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

    def test_user_profile_form_invalid_email_address_field(self):
        """Tests the email address invalid input in the extra form"""
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
        """Tests the excluded attribute of the profile form meta class"""
        form = UserProfileForm()
        self.assertEqual(form.Meta.exclude, ('user', 'stripe_customer_id'))

    def test_custom_signup_form_all_fields_required(self):
        """Tests the required fields in the custom sign up form"""
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
        """
        Creates a user and verifies that the string
        method is correct. Code for creating the user is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/
        """
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Password',
            first_name='Test',
            last_name='User',
        )
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(user_profile), 'Test User')
