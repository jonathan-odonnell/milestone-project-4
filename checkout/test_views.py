from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from .views import checkout, cache_checkout_data, checkout_success
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
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
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

    def test_get_checkout_page(self):
        request = self.factory.get('/checkout/')
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        self.assertEqual(response.status_code, 200)

    def test_get_checkout_success_page(self):
        request = self.factory.get(f'/checkout/success/{self.booking.booking_number}/')
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout_success(request, self.booking.booking_number)
        self.assertEqual(response.status_code, 200)

    def test_cache_checkout(self):
        request = self.factory.post('/checkout/cache_checkout_data/', {
            'save_info': 'true',
            'client_secret': self.intent.client_secret
        })
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = cache_checkout_data(request)
        self.assertEqual(response.status_code, 200)

    def test_submit_checkout_form_stripe(self):
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
        booking = Booking.objects.get(booking_number=self.booking.booking_number)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(booking.paid)
        self.assertEqual(booking.stripe_pid, self.intent.client_secret.split('_secret')[0])

    def test_submit_checkout_form_paypal(self):
        self.booking.stripe_pid = ''
        self.booking.paid = False
        self.booking.save()
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
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = checkout(request)
        booking = Booking.objects.get(booking_number=self.booking.booking_number)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(booking.paid)
        self.assertEqual(booking.paypal_pid, '1A5H6J8L9N6H5D')
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '00000000000')
        self.assertEqual(profile.street_address1, 'Test')
        self.assertEqual(profile.street_address2, 'Test')
        self.assertEqual(profile.town_or_city, 'Test')
        self.assertEqual(profile.county, 'Test')
        self.assertEqual(profile.country, 'GB')
        self.assertEqual(profile.postcode, 'Test')