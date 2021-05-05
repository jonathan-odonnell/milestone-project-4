from django import forms
from holidays.widgets import CustomClearableFileInput
from .models import Contact
from crispy_forms.helper import FormHelper


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-4'
        self.helper.label_class = 'form-label'

        placeholders = {
            'name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message',
        }

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['message'].widget.attrs['rows'] = 6

        for field in self.fields:
            if field != 'subject':
                placeholder = f'{placeholders[field]} *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False