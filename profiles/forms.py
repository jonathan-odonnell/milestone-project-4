from django import forms
from .models import UserProfile
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm


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
        self.fields['first_name'] = forms.CharField(max_length=30, label='First Name')
        self.fields['last_name'] = forms.CharField(max_length=30, label='Last Name')
        self.fields['email'].label = 'Email Address'
        self.fields['password2'].label = 'Confirm Password'
        
        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'Enter your email address',
            'password1': 'Enter your password',
            'password2': 'Confirm  your password',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
    
    def signup(self, request, user):
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()
        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email Address'
        self.fields['login'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs['placeholder'] = 'Enter your current password'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your new password'
        self.fields['password2'].label = 'Confirm New Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your new password'
