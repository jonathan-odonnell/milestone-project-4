from django import forms
from .models import UserProfile
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'stripe_customer_id')

    def __init__(self, *args, **kwargs):
        """
        Adds address field, placeholders and classes, removes the Labels,
        and sets the pattern attribute of the phone number widget. Code for
        setting the field_class and label_class is from
        https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        and code for setting the pattern attribute of the phone number
        widget is adapted from
        https://stackoverflow.com/questions/19611599/html5-phone-number-validation-with-pattern
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
        self.fields['phone_number'].widget.attrs[
            'pattern'] = '[+0]{1}[0-9]{0,3}[1-9]{1}[0-9]{8,}'
        for field in self.fields:
            if field != 'country':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                self.fields[field].widget.attrs['class'] = 'form-select'
            self.fields[field].label = False


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        """
        Adds the first name and last name fields and amends the placeholders
        and labels in the register form. Code is from
        https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/
        """
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(
            max_length=30, label='First Name')
        self.fields['last_name'] = forms.CharField(
            max_length=30, label='Last Name')
        self.fields['email'].label = 'Email Address'
        self.fields['password2'].label = 'Confirm Password'

        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'Enter your email address',
            'password1': 'Enter your password',
            'password2': 'Confirm your password',
        }

        for field in self.fields:
            self.fields[field].widget.attrs[
                'placeholder'] = placeholders[field]

    def signup(self, user):
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()
        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        """Amends the placeholders and labels in the login form."""
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email Address'
        self.fields[
            'login'].widget.attrs[
                'placeholder'] = 'Enter your email address'
        self.fields[
            'password'].widget.attrs[
                'placeholder'] = 'Enter your password'


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        """Amends the placeholders and labels in the change password form."""
        super().__init__(*args, **kwargs)
        self.fields[
            'oldpassword'].widget.attrs[
                'placeholder'] = 'Enter your current password'
        self.fields[
            'password1'].widget.attrs[
                'placeholder'] = 'Enter your new password'
        self.fields[
            'password2'].label = 'Confirm New Password'
        self.fields[
            'password2'].widget.attrs[
                'placeholder'] = 'Confirm your new password'
