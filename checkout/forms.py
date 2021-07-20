from django import forms
from booking.models import Booking
from crispy_forms.helper import FormHelper


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'county', 'postcode',
                  'country',)

    def __init__(self, *args, **kwargs):
        """
        Adds address field, placeholders, classes, and country field blank
        option, removes the labels, sets the autofocus on the full name field
        and sets the pattern attribute of the phone number field widget.
        Code for setting the field_class and label_class is from
        https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        and code for setting the pattern attribute is adapted from
        https://stackoverflow.com/questions/19611599/html5-phone-number-validation-with-pattern
        """
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postcode',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        self.fields['address'] = forms.CharField(required=False)
        self.fields['phone_number'].widget.attrs[
            'pattern'] = '[+]{1}[0-9]{2,3}[1-9]{1}[0-9]{8,}'

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                self.fields[field].choices = [
                    ('', 'Country *')] + self.fields[field].choices
            self.fields[field].label = False
