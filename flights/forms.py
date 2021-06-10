from django import forms
from django.forms.widgets import DateTimeInput
from holidays.models import Flight
from crispy_forms.helper import FormHelper


class FlightForm(forms.ModelForm):
    """
    Adds timezone field blank option values, formats datetime field values,
    adds classes, removes auto-generated labels and sets the autofocus on
    first field. Code for formatting the datetime field values is from
    https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#django.forms.DateTimeInput
    and code for setting the field_class and label_class is from
    https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
    """

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

        self.fields['flight_number'].widget.attrs['autofocus'] = True
        self.fields['direction'].choices = directions
        self.fields['origin_time_zone'].widget.attrs['class'] = 'form-select'
        self.fields['origin_time_zone'].choices = [
            ('', '')] + self.fields['origin_time_zone'].choices[1:]
        self.fields[
            'destination_time_zone'].widget.attrs['class'] = 'form-select'
        self.fields['destination_time_zone'].choices = [
            ('', '')] + self.fields['origin_time_zone'].choices[1:]
        self.fields['departure_time'].widget = DateTimeInput(
            format='%d/%m/%Y %H:%M')
        self.fields['arrival_time'].widget = DateTimeInput(
            format='%d/%m/%Y %H:%M')
