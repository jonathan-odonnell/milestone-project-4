from django import forms
from .models import Booking, BookingPassenger
from crispy_forms.helper import FormHelper
from django.forms import (
    SelectDateWidget, inlineformset_factory, BaseInlineFormSet)


class PassengerForm(forms.ModelForm):
    class Meta:
        model = BookingPassenger
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Sets the date of birth field widget as the SelectDateWidget, adds
        classes and sets all fields to be required.
        Code for the SelectDateWidget is from
        https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#multiwidget
        and code for setting the field_class and label_class is from
        https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
        self.fields['date_of_birth'].widget = SelectDateWidget(
            years=range(2021, 1900, -1),
            empty_label=['Year', 'Month', 'Day'])
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-select'

        for field in self.fields:
            self.fields[field].widget.attrs['required'] = True


class BaseInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, min_num, **kwargs):
        """
        Sets the number of extra rows in the formset.
        Code is from
        https://stackoverflow.com/questions/23084595/basemodelformset-init-got-an-unexpected-keyword-argument
        and
        https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#passing-custom-parameters-to-formset-forms
        """
        self.min_num = min_num
        super(BaseInlineFormSet, self).__init__(*args, **kwargs)


"""
Code for the inline formset is from
https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
and https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
"""
PassengersFormSet = inlineformset_factory(
    Booking, BookingPassenger, form=PassengerForm,
    formset=BaseInlineFormSet, extra=0, validate_min=True)
