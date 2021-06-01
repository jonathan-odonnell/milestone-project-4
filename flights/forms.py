from datetime import time
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.fields import DateTimeField
from django.forms.widgets import DateTimeInput
from pytz import timezone
from holidays.models import Flight
from crispy_forms.helper import FormHelper

class FlightForm(forms.ModelForm):

    class Meta:
        model = Flight
        exclude = ('duration',)

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

        timezones = [
            ('', '')
        ]

        self.fields['flight_number'].widget.attrs['autofocus'] = True
        self.fields['direction'].choices = directions
        self.fields['origin_time_zone'].widget.attrs['class'] = 'form-select'
        timezones.extend( self.fields['origin_time_zone'].choices[1:])
        self.fields['origin_time_zone'].choices = timezones
        self.fields['destination_time_zone'].widget.attrs['class'] = 'form-select'
        self.fields['destination_time_zone'].choices = timezones
        self.fields['departure_time'].widget = DateTimeInput(format='%d/%m/%Y %H:%M')
        self.fields['arrival_time'].widget = DateTimeInput(format='%d/%m/%Y %H:%M')