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

        categories = Category.objects.all()
        category_names = [(c.id, c.name) for c in categories]
        countries = Country.objects.all()
        country_names = [(c.id, c.name) for c in countries]
        features = Feature.objects.all()
        features_names = [(f.id, f.name) for f in features]
        activities = Activity.objects.all()
        activities_names = [(a.id, a.activity) for a in activities]
        extras = Extra.objects.all()
        extra_names = [(e.id, e.name) for e in extras]

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['image'].widget = CustomClearableFileInput()
        self.fields['category'].choices = category_names
        self.fields['country'].choices = country_names
        self.fields['features'].choices = features_names
        self.fields['activities'].choices = activities_names
        self.fields['extras'].choices = extra_names
        self.fields['description'].widget.attrs['rows'] = 5


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

        days = (
            ('1', 'Day 1'),
            ('2', 'Day 2'),
            ('3', 'Day 3'),
            ('4', 'Day 4'),
            ('5', 'Day 5'),
            ('6', 'Day 6'),
            ('7', 'Day 7'),
            ('8', 'Day 8'),
            ('9', 'Day 9'),
            ('10', 'Day 10'),
        )

        self.fields['day'].choices = days


PriceFormset = inlineformset_factory(Package, Price, form=PriceForm, extra=1)
ItineraryFormset = inlineformset_factory(
    Package, Itinerary, form=ItineraryForm, extra=1)
