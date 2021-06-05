from django.test import TestCase
from .forms import PassengerForm


class TestBookingForm(TestCase):
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

    def test_invalid_passport_number(self):
        form = PassengerForm({
            'full_name': 'Test User',
            'date_of_birth': '01/01/1990',
            'passport_number': 'aaaaaaaaaa',
        })
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
