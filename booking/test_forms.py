from django.test import TestCase
from .forms import PassengerForm, PassengersFormSet


class TestBookingForm(TestCase):
    """Tests the required fields in the passengers formset"""

    def test_all_form_fields_required(self):
        form = PassengersFormSet({
            'booking_passengers-TOTAL_FORMS': '1',
            'booking_passengers-INITIAL_FORMS': '1',
            'booking_passengers-MIN_NUM_FORMS': '1',
            'booking_passengers-MAX_NUM_FORMS': '1000',
            'booking_passengers-0-full_name': '',
            'booking_passengers-0-date_of_birth': '',
            'booking_passengers-0-passport_number': '',
        }, min_num=1)
        self.assertEqual(form.errors[0]['full_name']
                         [0], 'This field is required.')
        self.assertEqual(form.errors[0]['date_of_birth']
                         [0], 'This field is required.')
        self.assertEqual(
            form.errors[0]['passport_number'][0], 'This field is required.')

    def test_invalid_passport_number_input(self):
        """Tests invalid passport number input in the passengers formet"""
        form = PassengersFormSet({
            'booking_passengers-TOTAL_FORMS': '1',
            'booking_passengers-INITIAL_FORMS': '1',
            'booking_passengers-MIN_NUM_FORMS': '1',
            'booking_passengers-MAX_NUM_FORMS': '1000',
            'booking_passengers-0-full_name': 'Test User',
            'booking_passengers-0-date_of_birth': '01/01/1990',
            'booking_passengers-0-passport_number': 'aaaaaaaaaa',
        }, min_num=1)
        self.assertEqual(
            form.errors[0]['passport_number'][0], 'Enter a number.')

    def test_passport_number_input_too_long(self):
        """Tests passport number input too long in the passengers formset"""
        form = PassengersFormSet({
            'booking_passengers-TOTAL_FORMS': '1',
            'booking_passengers-INITIAL_FORMS': '1',
            'booking_passengers-MIN_NUM_FORMS': '1',
            'booking_passengers-MAX_NUM_FORMS': '1000',
            'booking_passengers-0-full_name': 'Test User',
            'booking_passengers-0-date_of_birth': '01/01/1990',
            'booking_passengers-0-passport_number': '1234567890',
        }, min_num=1)
        self.assertEqual(form.errors[0]
                         ['passport_number'][0],
                         'Ensure that there are no more than '
                         + '9 digits in total.')

    def test_fields_in_form_metaclass(self):
        """Tests the all attribute of the passenger form meta class"""
        form = PassengerForm()
        self.assertEqual(form.Meta.fields, '__all__')
