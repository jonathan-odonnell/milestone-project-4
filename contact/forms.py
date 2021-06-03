from django import forms
from holidays.widgets import CustomClearableFileInput
from .models import CustomerContact
from crispy_forms.helper import FormHelper


class ContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-4'
        self.helper.label_class = 'form-label'

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message',
        }

        subjects = [
            ('', 'Subject *'),
            ('Holiday Information', 'Holiday Information'),
            ('Offers', 'Offers'),
            ('Bookings', 'Bookings'),
            ('General Enquiries', 'General Enquiries'),
            ('Other', 'Other')
        ]

        self.fields['full_name'].widget.attrs['autofocus'] = True
        self.fields['subject'].choices = subjects
        self.fields['message'].widget.attrs['rows'] = 8
        self.fields['subject'].widget.attrs['class'] = 'form-select'

        for field in self.fields:
            if field != 'subject':
                placeholder = f'{placeholders[field]} *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False