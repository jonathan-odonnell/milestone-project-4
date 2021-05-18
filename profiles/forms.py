from django import forms
from .models import UserProfile
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','stripe_customer_id')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'

        placeholders = {
            'email_address': 'Email Address',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postcode',
        }
        self.fields['email_address'] = forms.EmailField(required=True)
        self.fields['address'] = forms.CharField(required=False)
        self.fields['phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                if field != 'address':
                    self.fields[field].label = placeholders[field]
                else:
                    self.fields[field].label = False
                self.fields[field].widget.attrs['placeholder'] = placeholder


class CustomSignupForm(SignupForm):

    # https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=30)
        self.fields['last_name'] = forms.CharField(max_length=30)
        
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = False
    
    def signup(self, request, user):
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()
        return user
