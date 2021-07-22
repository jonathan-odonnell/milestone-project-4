from django.test import TestCase
from .models import Coupon, Booking
from holidays.models import Package
from extras.models import Extra
from decimal import Decimal
from datetime import date


class TestBookingModels(TestCase):
    def setUp(self):
        """
        Creates a booking, package, extra, booking extra and
        booking passenger in the database
        """
        self.coupon = Coupon.objects.create(
            name='HOLIDAY100',
            start_date=date(2021, 6, 1),
            end_date=date(2021, 8, 1),
            amount=100
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

        self.extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(4.99), 2),
            image='testimage.jpg',
        )

        self.booking = Booking.objects.create(
            package=self.holiday,
            guests=1,
            departure_date=date(2021, 6, 1),
            return_date=date(2021, 6, 10),
            outbound_flight=self.holiday.flights.first(),
            return_flight=self.holiday.flights.first(),
        )

        self.booking.booking_extras.create(
            extra=self.extra,
            quantity=1,
        )

        self.booking.booking_passengers.create(
            full_name='Test User',
            date_of_birth=date(1990, 1, 1),
            passport_number=123456789,
        )

    def test_booking_defaults(self):
        """Tests the defaults on the booking model"""
        self.assertEqual(self.booking.full_name, '')
        self.assertEqual(self.booking.phone_number, '')
        self.assertEqual(self.booking.email, '')
        self.assertEqual(self.booking.street_address1, '')
        self.assertEqual(self.booking.street_address2, '')
        self.assertEqual(self.booking.town_or_city, '')
        self.assertEqual(self.booking.county, '')
        self.assertEqual(self.booking.country, '')
        self.assertEqual(self.booking.postcode, '')
        self.assertEqual(self.booking.stripe_pid, '')
        self.assertEqual(self.booking.paypal_pid, '')

    def test_coupon_string_method(self):
        """ Verifies that the coupon string method is correct """
        self.assertEqual(str(
            self.coupon), f'{self.coupon.name} '
            + f'{self.coupon.start_date} - {self.coupon.end_date}')

    def test_booking_totals(self):
        """
        Verifies that the booking extra total, subtotal
        and grand total are correct
        """
        self.assertEqual(self.booking.extras_total, round(Decimal(4.99), 2))
        self.assertEqual(self.booking.subtotal, 499)
        self.assertEqual(self.booking.grand_total,
                         round(Decimal(499 + 4.99), 2))

    def test_booking_string_method(self):
        """ Verifies that the booking string method is correct """
        self.assertEqual(str(self.booking), self.booking.booking_number)

    def test_booking_extra_string_method(self):
        """ Verifies that the booking extra string method is correct """
        self.assertEqual(str(self.booking.booking_extras.first(
        )), f'{self.booking.booking_extras.first().extra.name} '
            + f'on booking {self.booking.booking_number}')

    def test_booking_passenger_string_method(self):
        """ Verifies that the booking passenger string method is correct """
        self.assertEqual(str(self.booking.booking_passengers.first(
        )), f'{self.booking.booking_passengers.first().full_name} '
            + f'on booking {self.booking.booking_number}')
