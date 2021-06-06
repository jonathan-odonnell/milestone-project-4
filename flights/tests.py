from django.test import TestCase
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .models import Flight
from .forms import FlightForm
from datetime import datetime
from pytz import timezone
import pytz


class TestFlightsViews(TestCase):
    def setUp(self):

        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=user,
            email='admin@example.com',
        )

        self.client.login(
            email='admin@example.com',
            password='Password',
        )

        self.flight = Flight.objects.create(
            flight_number='ZZ001',
            direction='Outbound',
            origin='Test Airport',
            destination='Test Airport',
            departure_time=datetime(2021, 6, 1, 12, tzinfo=pytz.utc),
            origin_time_zone=timezone('Europe/London'),
            arrival_time=datetime(2021, 6, 1, 16, tzinfo=pytz.utc),
            destination_time_zone=timezone('America/Toronto'),
            baggage=20
        )

    def test_get_airports_json(self):
        self.flight.packages.create(
            name='Test Holiday',
            image='test_image.jpg',
            description='Test description',
            offer=True,
            price=499,
            duration=14,
            catering='Full Board',
            transfers_included=True
        )
        response = self.client.get(f'/flights/airports/{self.flight.packages.first().id}/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'airports': ['Test Airport']})

    def test_get_flights_page(self):
        response = self.client.get('/flights/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flights/flights.html')

    def test_get_sorted_flights_page(self):
        # https://stackoverflow.com/questions/4794457/unit-testing-django-json-view
        response = self.client.get('/flights/?sort=number&direction=desc',  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flights/includes/flights_table.html')

    def test_get_add_flight_page(self):
        response = self.client.get('/flights/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flights/add_flight.html')

    def test_can_add_flight(self):
        response = self.client.post(f'/flights/add/', {
            'flight_number': 'ZZ002',
            'direction': 'Outbound',
            'origin': 'Test Airport',
            'destination': 'Test Airport',
            'departure_time': '01/06/2021 12:00 ',
            'origin_time_zone': 'Europe/London',
            'arrival_time': '01/06/2021 16:00',
            'destination_time_zone': 'America/Toronto',
            'baggage': '20',
        })
        self.assertRedirects(response, '/flights/')
        flight = Flight.objects.filter(flight_number='ZZ002')
        self.assertEqual(len(flight), 1)

    def test_get_edit_flight_page(self):
        response = self.client.get(f'/flights/edit/{self.flight.flight_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flights/edit_flight.html')

    def test_can_edit_flight(self):
        response = self.client.post(f'/flights/edit/{self.flight.flight_number}/', {
            'flight_number': 'ZZ001',
            'direction': 'Outbound',
            'origin': 'Test Airport',
            'destination': 'Test Airport 2',
            'departure_time': '01/06/2021 12:00 ',
            'origin_time_zone': 'Europe/London',
            'arrival_time': '01/06/2021 16:00',
            'destination_time_zone': 'America/Toronto',
            'baggage': '20',
        })
        self.assertRedirects(response, '/flights/')
        flight = Flight.objects.get(flight_number='ZZ001')
        self.assertEqual(flight.destination, 'Test Airport 2')

    def test_can_delete_flight(self):
        response = self.client.get(f'/flights/delete/{self.flight.flight_number}/')
        self.assertRedirects(response, '/flights/')
        flight = Flight.objects.filter(flight_number='ZZ001')
        self.assertEqual(len(flight), 0)


class TestFlightsForm(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Password',
        )

        EmailAddress.objects.create(
            user=user,
            email='admin@example.com',
        )

        self.client.login(
            email='admin@example.com',
            password='Password',
        )

    def test_all_form_fields_required(self):
        form = FlightForm({
            'flight_number': '',
            'direction': '',
            'origin': '',
            'destination': '',
            'departure_time': '',
            'origin_time_zone': '',
            'arrival_time': '',
            'destination_time_zone': '',
            'baggage': '',
        })
        self.assertEqual(form.errors['flight_number']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['direction']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['origin'][0], 'This field is required.')
        self.assertEqual(form.errors['destination']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['departure_time']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['origin_time_zone']
                         [0], 'This field is required.')
        self.assertEqual(form.errors['arrival_time']
                         [0], 'This field is required.')
        self.assertEqual(
            form.errors['destination_time_zone'][0], 'This field is required.')
        self.assertEqual(form.errors['baggage'][0], 'This field is required.')

    def test_invalid_form_field_input(self):
        form = FlightForm({
            'flight_number': 'ZZ001',
            'direction': 'outward',
            'origin': 'Test Airport',
            'destination': 'Test Airport',
            'departure_time': '12:00 01/06/2021 ',
            'origin_time_zone': 'Canada/Ottawa',
            'arrival_time': '16:00 01/06/2021',
            'destination_time_zone': 'Canada/Calgary',
            'baggage': 'a',
        })
        self.assertEqual(
            form.errors['direction'][0], 'Select a valid choice. outward is not one of the available choices.')
        self.assertEqual(form.errors['departure_time']
                         [0], 'Enter a valid date/time.')
        self.assertEqual(form.errors['origin_time_zone'][0],
                         'Select a valid choice. Canada/Ottawa is not one of the available choices.')
        self.assertEqual(form.errors['arrival_time']
                         [0], 'Enter a valid date/time.')
        self.assertEqual(form.errors['destination_time_zone'][0],
                         'Select a valid choice. Canada/Calgary is not one of the available choices.')
        self.assertEqual(form.errors['baggage'][0], 'Enter a number.')

    def test_excluded_in_form_metaclass(self):
        form = FlightForm()
        self.assertEqual(form.Meta.exclude, ('duration',))


class TestFlightsModel(TestCase):
    def test_filght_string_method_returns_flight_number(self):
        flight = Flight.objects.create(
            flight_number='ZZ001',
            direction='Outbound',
            origin='Test Airport',
            destination='Test Airport',
            departure_time=datetime(2021, 6, 1, 12, tzinfo=pytz.utc),
            origin_time_zone=timezone('Europe/London'),
            arrival_time=datetime(2021, 6, 1, 16, tzinfo=pytz.utc),
            destination_time_zone=timezone('America/Toronto'),
            baggage=20
        )
        self.assertEqual(str(flight), 'ZZ001')
