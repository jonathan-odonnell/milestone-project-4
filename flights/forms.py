from django import forms
from django.forms.fields import DateTimeField
from django.forms.widgets import DateTimeInput
from holidays.models import Flight
from crispy_forms.helper import FormHelper

class FlightForm(forms.ModelForm):

    class Meta:
        model = Flight
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'

        directions = [
            ('', ''),
            ('Outbound', 'Outbound'),
            ('Return', 'Return'),
        ]

        self.fields['flight_number'].widget.attrs['autofocus'] = True
        self.fields['direction'].choices = directions
        self.fields['departure_time'].widget = DateTimeInput(format='%d/%m/%Y %H:%M')
        self.fields['arrival_time'].widget = DateTimeInput(format='%d/%m/%Y %H:%M')