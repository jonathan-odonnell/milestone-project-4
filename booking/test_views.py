from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import Booking, Coupon
from .views import(update_guests, add_extra, 
update_extra, remove_extra, add_coupon, passengers)
from holidays.models import Package
from extras.models import Extra
from decimal import Decimal
from datetime import date, datetime
from pytz import timezone
import pytz


class TestBookingViews(TestCase):
    def setUp(self):
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
            destination_time_zone=timezone('America/Toronto'),
            baggage=20
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

    def test_can_add_booking(self):
        response = self.client.post(f'/booking/{self.holiday.id}/', {
            'departure_date': '01/06/2021',
            'departure_airport': 'Test Airport',
            'guests': '2'
        })
        self.assertRedirects(response, '/booking/')

    def test_can_update_guests(self):
        booking = Booking.objects.create(
            package=self.holiday,
            guests=2,
            departure_date=datetime(2021, 6, 1, tzinfo=pytz.utc),
            return_date=datetime(2021, 6, 10, tzinfo=pytz.utc),
            outbound_flight=self.holiday.flights.first(),
            return_flight=self.holiday.flights.first(),
        )
        request = self.factory.post('/booking/update_guests/', {
            'guests': '3'
        })
        request.session = {'booking_number': booking.booking_number}
        response = update_guests(request)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(booking_number=booking.booking_number)
        self.assertEqual(booking.guests, 3)

    def test_can_add_booking_extra(self):
        request = self.factory.post(f'/booking/add_extra/{self.extra.id}/', {
            'quantity': '1'
        })
        request.session = {'booking_number': self.booking.booking_number}
        response = add_extra(request, self.extra.id)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(booking_number=self.booking.booking_number)
        self.assertEqual(booking.booking_extras.first().quantity, 1)

    def test_can_update_booking_extra(self):
        self.booking.booking_extras.create(
            extra=self.extra,
            quantity=1,
        )
        request = self.factory.post(f'/booking/update_extra/{self.extra.id}/', {
            'quantity': '2'
        })
        request.session = {'booking_number': self.booking.booking_number}
        response = update_extra(request, self.extra.id)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(booking_number=self.booking.booking_number)
        self.assertEqual(booking.booking_extras.first().quantity, 2)
        self.assertEqual(booking.extras_total, round(Decimal(9.98), 2))
        self.assertEqual(booking.grand_total, round(Decimal(499 + 9.98), 2))

    def test_can_remove_booking_extra(self):
        extra = Extra.objects.create(
            name='Test Extra',
            description='Test Description',
            price=round(Decimal(4.99), 2),
            image='testimage.jpg',
        )
        booking = Booking.objects.create(
            package=self.holiday,
            guests=2,
            departure_date=datetime(2021, 6, 1, tzinfo=pytz.utc),
            return_date=datetime(2021, 6, 10, tzinfo=pytz.utc),
            outbound_flight=self.holiday.flights.first(),
            return_flight=self.holiday.flights.first(),
        )
        booking.booking_extras.create(
            extra=extra,
            quantity=1,
        )
        request = self.factory.post(f'/booking/remove_extra/{extra.id}/')
        request.session = {'booking_number': booking.booking_number}
        response = remove_extra(request, extra.id)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(booking_number=booking.booking_number)
        self.assertEqual(len(booking.booking_extras.all()), 0)
        self.assertEqual(booking.extras_total, 0)
        self.assertEqual(booking.grand_total, 998)

    def test_can_add_coupon_to_booking(self):
        Coupon.objects.create(
            name='HOLIDAY100',
            start_date=datetime(2021, 6, 1),
            end_date=datetime(2021, 8, 1),
            amount=100
        )
        request = self.factory.post(
            f'/booking/add_coupon/', {'coupon': 'HOLIDAY100'})
        request.session = {'booking_number': self.booking.booking_number}
        response = add_coupon(request)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(booking_number=self.booking.booking_number)
        self.assertEqual(booking.coupon, 'HOLIDAY100')
        self.assertEqual(booking.discount, 100)
        self.assertEqual(booking.grand_total, 399)

    def test_can_get_passengers_page(self):
        request = self.factory.get('/booking/passengers/')
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = passengers(request)
        self.assertEqual(response.status_code, 200)

    def test_can_add_passenger(self):
        request = self.factory.post('/booking/passengers/', {
            'booking_passengers-TOTAL_FORMS': '1',
            'booking_passengers-INITIAL_FORMS': '0',
            'booking_passengers-MIN_NUM_FORMS': '0',
            'booking_passengers-MAX_NUM_FORMS': '1000',
            'booking_passengers-0-full_name': 'Test User',
            'booking_passengers-0-date_of_birth': '01/01/1990',
            'booking_passengers-0-passport_number': '123456789',
        })
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = passengers(request)
        self.assertEqual(response.status_code, 302)
