from django.test import TestCase
from .forms import CheckoutForm


class TestCheckoutForm(TestCase):
    def test_all_form_fields_required(self):
        """Tests the required fields in the extra form."""
        form = CheckoutForm({
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

    def test_invalid_email_address_input(self):
        """Tests invalid email_address input in the extra form"""
        form = CheckoutForm({
            'full_name': 'Test User',
            'email': 'Not an email address',
            'phone_number': '0000000000',
            'street_address1': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test',
        })
        self.assertEqual(form.errors['email']
                         [0], 'Enter a valid email address.')

    def test_invalid_phone_number_input(self):
        """Tests invalid phone number input in the extra form"""
        form = CheckoutForm({
            'full_name': 'Test User',
            'email': 'Not an email address',
            'phone_number': '0000000000',
            'street_address1': 'Test',
            'town_or_city': 'Test',
            'county': 'Test',
            'country': 'GB',
            'postcode': 'Test',
        })
        self.assertEqual(form.errors['phone_number'][0],
                         'Enter a valid phone number (e.g. 0121 234 5678) or '
                         + 'a number with an international call prefix.')

    def test_fields_in_form_metaclass(self):
        """Tests the excluded attribute of the checkout form meta class"""
        form = CheckoutForm()
        self.assertEqual(
            form.Meta.fields, ('full_name', 'email', 'phone_number',
                               'street_address1', 'street_address2',
                               'town_or_city', 'county', 'postcode',
                               'country',))
