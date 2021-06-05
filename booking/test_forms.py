from django.test import TestCase
from .models import Booking
from holidays.models import Package
from .forms import PassengerForm
from datetime import date, datetime
from pytz import timezone
import pytz


class TestBookingForm(TestCase):
    def setUp(self):

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

    def test_all_fields_required(self):
        form = PassengerForm({
            'full_name': '',
            'date_of_birth': '',
            'passport_number': '',
        })
        self.assertEqual(form.errors['full_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['date_of_birth']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['passport_number']
                         [0], 'This field is required.')

    def test_invalid_field_inputs(self):
        form = PassengerForm({
            'full_name': 'Test User',
            'date_of_birth': '00000000',
            'passport_number': 'aaaaaaaaaa',
        })
        self.assertEqual(form.errors['date_of_birth']
                         [0], 'Enter a valid date.')
        self.assertEqual(form.errors['passport_number']
                         [0], 'Enter a number.')

    def test_passport_number_too_long(self):
        form = PassengerForm({
            'full_name': 'Test User',
            'date_of_birth': '01/01/1990',
            'passport_number': '1234567890',
        })
        self.assertEqual(form.errors['passport_number']
                         [0], 'Ensure that there are no more than 9 digits in total.')

    def test_fields_in_form_metaclass(self):
        form = PassengerForm()
        self.assertEqual(form.Meta.fields, '__all__')
