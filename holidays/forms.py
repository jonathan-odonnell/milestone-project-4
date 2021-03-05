from django import forms
from django.forms import inlineformset_factory
from .widgets import CustomClearableFileInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Div
from crispy_forms.bootstrap import InlineField
from .models import Activity, Category, Country, Feature, Flight, Itinerary, Package, Price
from extras.models import Extra


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['image'].widget = CustomClearableFileInput()
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['category'].empty_label = 'Category'
        self.fields['country'].empty_label = 'Country'


class PriceForm(forms.ModelForm):

    class Meta:
        model = Price
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 form-label'
        self.helper.field_class = 'col-md-9'


class ItineraryForm(forms.ModelForm):

    class Meta:
        model = Itinerary
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 form-label'
        self.helper.field_class = 'col-md-9'


PriceFormset = inlineformset_factory(Package, Price, form=PriceForm, extra=1)
ItineraryFormset = inlineformset_factory(
    Package, Itinerary, form=ItineraryForm, extra=1)
