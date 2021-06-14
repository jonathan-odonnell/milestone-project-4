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

    def test_invalid_email_address_field(self):
        """Tests the email address invalid input in the extra form"""
        form = CheckoutForm({
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
        """Tests the excluded attribute of the checkout form meta class"""
        form = CheckoutForm()
        self.assertEqual(
            form.Meta.fields, ('full_name', 'email', 'phone_number',
                               'street_address1', 'street_address2',
                               'town_or_city', 'county', 'postcode',
                               'country',))
