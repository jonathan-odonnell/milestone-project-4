from django import forms
from .models import BookingPassenger
from crispy_forms.helper import FormHelper
from django.forms import SelectDateWidget


class PassengerForm(forms.ModelForm):
    class Meta:
        model = BookingPassenger
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
        self.fields['date_of_birth'].widget = forms.SelectDateWidget(years=reversed(range(1900, 2022)), empty_label=['Year', 'Month', 'Day'])
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-select'

        for field in self.fields:
            self.fields[field].required = True
