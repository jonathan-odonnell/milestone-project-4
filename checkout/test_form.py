from django.test import TestCase
from django.contrib.auth.models import User
from booking.models import Booking
from holidays.models import Package
from .forms import BookingForm
from datetime import date, datetime
from pytz import timezone
import pytz


class TestBookingForm(TestCase):
    def setUp(self):

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

    def test_all_form_fields_required(self):
        form = BookingForm({
            'full_name': '',
            'email': '',
            'phone_number': '',
            'street_address1': '',
            'town_or_city': '',
            'county': '',
            'country': '',
            'postcode': '',
        })
        self.assertEqual(form.errors['full_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['email']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['street_address1']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['town_or_city']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['county']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['country']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['postcode']
                         [0], 'This field is required.')

    def test_invalid_email_address_field(self):
        form = BookingForm({
            'full_name': 'Test User',
            'email': 'Not an email address',
            'phone_number': 'Not a phone number',
            'street_address1': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test',
        })
        self.assertEqual(form.errors['email']
                         [0], 'Enter a valid email address.')

    def test_fields_in_form_metaclass(self):
        form = BookingForm()
        self.assertEqual(form.Meta.fields, ('full_name', 'email', 'phone_number',
                                            'street_address1', 'street_address2',
                                            'town_or_city', 'county', 'postcode',
                                            'country',))
