from django import forms
from .models import Booking, BookingPassenger
from crispy_forms.helper import FormHelper
from django.forms import SelectDateWidget, inlineformset_factory, BaseInlineFormSet


class PassengerForm(forms.ModelForm):
    class Meta:
        model = BookingPassenger
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
        self.fields['date_of_birth'].widget = SelectDateWidget(years=reversed(range(1900, 2022)), empty_label=['Year', 'Month', 'Day'])
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-select'

        for field in self.fields:
            self.fields[field].widget.attrs['required'] = True

# https://stackoverflow.com/questions/23084595/basemodelformset-init-got-an-unexpected-keyword-argument
# https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#passing-custom-parameters-to-formset-forms

class BaseInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, extra, min_num, **kwargs):
        self.extra = extra
        self.min_num = min_num
        super(BaseInlineFormSet, self).__init__(*args, **kwargs)

PassengersFormSet = inlineformset_factory(Booking, BookingPassenger, form=PassengerForm, formset=BaseInlineFormSet)
