from django import forms
from .widgets import CustomClearableFileInput
from .models import Activity, Category, Country, Feature, Flight, Itinerary, Package, Price
from extras.models import Extra
from crispy_forms.helper import FormHelper


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
        activities_names = [(a.id, a.name) for a in activities]
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
