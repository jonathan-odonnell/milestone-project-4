from django import forms
from .models import BookingPassenger
from crispy_forms.helper import FormHelper


class PassengerForm(forms.ModelForm):
    class Meta:
        model = BookingPassenger
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
