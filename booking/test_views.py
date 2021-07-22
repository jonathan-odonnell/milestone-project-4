from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User
from allauth.account.models import EmailAddress
from .models import Booking, Coupon
from .views import (booking, update_guests, add_extra,
                    update_extra, remove_extra, add_coupon, passengers)
from holidays.models import Package
from extras.models import Extra
from decimal import Decimal
from datetime import date, datetime
from pytz import timezone
import pytz


class TestBookingViews(TestCase):
    def setUp(self):
        """
        Sets up the request factory, user, email address, package, flight,
        extra and booking. Code for the request factory is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory,
        code for creating the user is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/,
        code for creating the email address is from
        https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py,
        code for creating the flight is from
        https://docs.djangoproject.com/en/3.2/ref/models/relations/
        and code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
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

    def test_get_booking_page_with_no_booking(self):
        """
        Verifies that a status of 200 is returned and the booking template was
        used when the user tries to access the booking page and no booking
        number is stored in the browser's session variable
        """
        response = self.client.get('/booking/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking.html')

    def test_get_booking_page_with_booking_added(self):
        """
        Verifies that a status of 200 is returned when the user tries to
        access the booking page and a booking number is stored in the
        browser's session variable. Code for the get request and setting
        the booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.get('/booking/')
        request.session = {'booking_number': self.booking.booking_number}
        response = booking(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_can_add_booking(self):
        """
        Verifies that the user is redirected to the booking page, a new booking
        is created in the database and the totals are correct when a post
        request with valid booking details is submitted to the add booking page
        by an anonymous user. Code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        response = self.client.post(f'/booking/{self.holiday.id}/', {
            'departure_date': '01/06/2021',
            'departure_airport': 'Test Airport',
            'guests': '2',
            'redirect_url': ''
        })
        self.assertRedirects(response, '/booking/')
        booking = Booking.objects.filter(guests=2)
        self.assertEqual(len(booking), 1)
        self.assertEqual(
            booking.first().grand_total, Decimal(998))

    def test_logged_in_user_can_add_booking(self):
        """
        Logs in the user and verifies that they are redirected to the
        booking page, a new booking is created in the database and the
        totals are correct when a post request with valid booking details
        is submitted to the add booking page. Code for the login is from
        https://docs.djangoproject.com/en/3.2/topics/testing/tools/#making-requests
        and code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        self.client.login(
            email=self.user.email,
            password='Password',
        )
        response = self.client.post(f'/booking/{self.holiday.id}/', {
            'departure_date': '01/06/2021',
            'departure_airport': 'Test Airport',
            'guests': '2',
            'redirect_url': ''
        })
        self.assertRedirects(response, '/booking/')
        booking = Booking.objects.filter(guests=2)
        self.assertEqual(len(booking), 1)
        self.assertEqual(
            booking.first().grand_total, Decimal(998))

    def test_can_update_guests(self):
        """
        Verifies that a status of 200 is returned and the guests quantity is
        updated in the database when a post request with the new guests
        quantity is submitted to the update guests page. Code for the post
        request and setting the booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        and code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        request = self.factory.post('/booking/update_guests/', {
            'guests': '3'
        })
        request.session = {'booking_number': self.booking.booking_number}
        response = update_guests(request)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(
            booking_number=self.booking.booking_number)
        self.assertEqual(booking.guests, 3)

    def test_can_add_booking_extra(self):
        """
        Verifies that a status of 200 is returned, the extra has been
        added to the booking in the database and the totals are correct
        when a post request with the quantity is submitted to the add
        extra page. Code for the post request and setting the booking
        number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post(f'/booking/add_extra/{self.extra.id}/', {
            'quantity': '1'
        })
        request.session = {'booking_number': self.booking.booking_number}
        response = add_extra(request, self.extra.id)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(
            booking_number=self.booking.booking_number)
        self.assertEqual(booking.booking_extras.first().quantity, 1)
        self.assertEqual(booking.extras_total, round(Decimal(4.99), 2))
        self.assertEqual(booking.grand_total, round(Decimal(499 + 4.99), 2))

    def test_can_update_booking_extra(self):
        """
        Verifies that a status of 200 is returned, the quantity of the extra
        is updated in the database and the totals are correct when a post
        request with the new quantity is submitted to the update extra page.
        Code for the post request and setting the booking number in the session
        variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        and code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        self.booking.booking_extras.create(
            extra=self.extra,
            quantity=1,
        )
        request = self.factory.post('/booking/update_extra/'
                                    + f'{self.extra.id}/', {
                                        'quantity': '2'
                                    })
        request.session = {'booking_number': self.booking.booking_number}
        response = update_extra(request, self.extra.id)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(
            booking_number=self.booking.booking_number)
        self.assertEqual(booking.booking_extras.first().quantity, 2)
        self.assertEqual(booking.extras_total, round(Decimal(9.98), 2))
        self.assertEqual(booking.grand_total, round(Decimal(499 + 9.98), 2))

    def test_can_remove_booking_extra(self):
        """
        Verifies that a status of 200 is returned, the booking is updated in
        the database and the totals are correct when a post request is
        submitted to the remove extra page. Code for the post request and
        setting the booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        and code for the first method is from
        https://docs.djangoproject.com/en/3.2/ref/models/querysets/#first
        """
        self.booking.booking_extras.create(
            extra=self.extra,
            quantity=1,
        )
        request = self.factory.post(f'/booking/remove_extra/{self.extra.id}/')
        request.session = {'booking_number': self.booking.booking_number}
        response = remove_extra(request, self.extra.id)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.filter(
            booking_number=self.booking.booking_number)
        self.assertEqual(len(booking.first().booking_extras.all()), 0)
        self.assertEqual(booking.first().extras_total, 0)
        self.assertEqual(booking.first().grand_total, 499)

    def test_can_add_coupon_to_booking(self):
        """
        Verifies that a status of 200 is returned, the coupon is added to the
        booking in the database and the totals are correct when a post request
        with a valid coupon code is  submitted to the add coupon page. Code for
        the post request and setting the booking number in the session variable
        is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        Coupon.objects.create(
            name='HOLIDAY100',
            start_date=datetime(2021, 6, 1),
            end_date=datetime(2021, 8, 1),
            amount=100
        )
        request = self.factory.post(
            '/booking/add_coupon/', {'coupon': 'HOLIDAY100'})
        request.session = {'booking_number': self.booking.booking_number}
        response = add_coupon(request)
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.get(
            booking_number=self.booking.booking_number)
        self.assertEqual(booking.coupon, 'HOLIDAY100')
        self.assertEqual(booking.discount, 100)
        self.assertEqual(booking.grand_total, 399)

    def test_anonymous_user_can_get_passengers_page(self):
        """
        Verifies that a status of 200 is returned when the user tries to
        access the passengers page and a booking number is stored in the
        browser's session variable. Code for the get request, setting the
        anonymous user and setting the booking number in the session
        variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.get('/booking/passengers/')
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = passengers(request)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_get_passengers_page(self):
        """
        Logs in the user and verifies that a status of 200 is returned when
        the user tries to access the passengers page and a booking number is
        stored in the browser's session variable. Code for the get request,
        setting the user and setting the booking number in the session
        variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.get('/booking/passengers/')
        request.user = self.user
        request.session = {'booking_number': self.booking.booking_number}
        response = passengers(request)
        self.assertEqual(response.status_code, 200)

    def test_can_add_passenger_details(self):
        """
        Logs in the user and verifies that a status of 302 is returned and a
        new booking passenger is added to the booking in the database when a
        post request with valid passenger details is submitted to the
        passengers page. Code for the post request, setting the anonymous user
        and setting the booking number in the session variable is from
        https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#the-request-factory
        """
        request = self.factory.post('/booking/passengers/', {
            'booking_passengers-TOTAL_FORMS': '1',
            'booking_passengers-INITIAL_FORMS': '0',
            'booking_passengers-MIN_NUM_FORMS': '0',
            'booking_passengers-MAX_NUM_FORMS': '1000',
            'booking_passengers-0-full_name': 'Test User',
            'booking_passengers-0-date_of_birth': '01/01/1990',
            'booking_passengers-0-passport_number': '123456789',
        })
        request.user = AnonymousUser()
        request.session = {'booking_number': self.booking.booking_number}
        response = passengers(request)
        self.assertEqual(response.status_code, 302)
