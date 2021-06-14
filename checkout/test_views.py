from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .views import checkout, cache_checkout_data, paypal, checkout_success
from holidays.models import Package
from booking.models import Booking
from profiles.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from datetime import date, datetime
from pytz import timezone
import pytz
import stripe


class TestCheckoutViews(TestCase):
    def setUp(self):
        """
        Sets up the request factory, user, email address, package, flight,
        booking, booking passenger and payment intent. Code for the request
        factory is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory,
        code for creating the user is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/,
        code for creating the email address is from
        https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py,
        code for creating the flight and booking passenger is from
        https://docs.djangoproject.com/en/3.2/ref/models/relations/
        """
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
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
            destination_time_zone=timezone('America/Toronto'),
            baggage=20
        )

        self.booking = Booking.objects.create(
            package=self.holiday,
            guests=1,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            outbound_flight=self.holiday.flights.first(),
            return_flight=self.holiday.flights.first(),
        )

        self.booking.booking_passengers.create(
            full_name='Test User',
            date_of_birth=date(1990, 1, 1),
            passport_number=123456789,
        )

        stripe_secret_key = settings.STRIPE_SECRET_KEY
        total = self.booking.grand_total
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        self.intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    def test_anonymous_user_get_checkout_page(self):
        """
        Verifies that a status of 200 is returned when the user tries to
        access the checkout page and a booking number is stored in the
        browser's session variable. Code for the get request, setting
        the anonymous user and setting the booking number in the session
        variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.get('/checkout/')
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_get_checkout_page(self):
        """
        Logs in the user and verifies that a status of 200 is returned
        when the user tries to access the checkout page and a booking
        number is stored in the browser's session variable. Code for
        the get request, setting the logging in the user and setting
        the booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.get('/checkout/')
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        self.assertEqual(response.status_code, 200)

    def test_get_checkout_success_page(self):
        """
        Verifies that a status of 200 is returned when the user tries to
        access the checkout success page and a booking number is stored
        in the browser's session variable. Code for the get request and
        setting the booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.get(
            f'/checkout/success/{self.booking.booking_number}/')
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout_success(request, self.booking.booking_number)
        self.assertEqual(response.status_code, 200)

    def test_cache_checkout(self):
        """
        Verifies that a status of 200 is returned when a post request
        with valid client secret and save info details is submitted to the
        cache checkout page and a booking number is stored in the browser's
        session variable. Code for the post request and setting the
        booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post('/checkout/cache_checkout_data/', {
            'save_info': 'true',
            'client_secret': self.intent.client_secret
        })
        request.session = {'booking_number': self.booking.booking_number}
        response = cache_checkout_data(request)
        self.assertEqual(response.status_code, 200)

    def test_create_paypal_order(self):
        """
        Verifies that a status of 200 is returned when a post request is
        submitted to the paypal page and a booking number is stored in the
        browser's session variable. Code for the post request and setting the
        booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post('/checkout/paypal/', {})
        request.session = {'booking_number': self.booking.booking_number}
        response = paypal(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_submit_checkout_form_stripe(self):
        """
        Verifies that a status of 302 is returned and a the user's profile is
        updated in the database when a post request with valid customer and
        stripe payment details is submitted to the checkout page. Code for the
        post request, setting the anonymous user and setting the booking number
        in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post('/checkout/', {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '00000000000',
            'street_address1': 'Test',
            'street_address2': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test',
            'client_secret': self.intent.client_secret,
            'paypal_pid': '',

        })
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.get(
            booking_number=self.booking.booking_number)
        self.assertEqual(booking.phone_number, '00000000000')
        self.assertEqual(booking.street_address1, 'Test')
        self.assertEqual(booking.street_address2, 'Test')
        self.assertEqual(booking.town_or_city, 'Test')
        self.assertEqual(booking.county, 'Test')
        self.assertEqual(booking.country, 'GB')
        self.assertEqual(booking.postcode, 'Test')
        self.assertTrue(booking.paid)
        self.assertEqual(booking.stripe_pid,
                         self.intent.client_secret.split('_secret')[0])

    def test_logged_in_user_submit_checkout_form_stripe(self):
        """
        Logs in the user and verifies that a status of 302 is returned and a
        the user's profile is updated in the database when a post request with
        valid customer and stripe payment details is submitted to the checkout
        page. Code for the post request, setting the user and setting the
        booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post('/checkout/', {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '00000000000',
            'street_address1': 'Test',
            'street_address2': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test',
            'client_secret': self.intent.client_secret,
            'paypal_pid': '',

        })
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        self.assertEqual(response.status_code, 302)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '00000000000')
        self.assertEqual(profile.street_address1, 'Test')
        self.assertEqual(profile.street_address2, 'Test')
        self.assertEqual(profile.town_or_city, 'Test')
        self.assertEqual(profile.county, 'Test')
        self.assertEqual(profile.country, 'GB')
        self.assertEqual(profile.postcode, 'Test')

    def test_submit_checkout_form_paypal(self):
        """
        Verifies that a status of 302 is returned and a the booking is updated
        in the database when a post request with valid customer and paypal
        payment details is submitted to the checkout page. Code for the post
        request, setting the anonymous user and setting the booking number in
        the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post('/checkout/', {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '00000000000',
            'street_address1': 'Test',
            'street_address2': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test',
            'save_info': 'on',
            'client_secret': self.intent.client_secret,
            'paypal_pid': '1A5H6J8L9N6H5D',

        })
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.get(
            booking_number=self.booking.booking_number)
        self.assertEqual(booking.phone_number, '00000000000')
        self.assertEqual(booking.street_address1, 'Test')
        self.assertEqual(booking.street_address2, 'Test')
        self.assertEqual(booking.town_or_city, 'Test')
        self.assertEqual(booking.county, 'Test')
        self.assertEqual(booking.country, 'GB')
        self.assertEqual(booking.postcode, 'Test')
        self.assertTrue(booking.paid)
        self.assertEqual(booking.paypal_pid, '1A5H6J8L9N6H5D')
