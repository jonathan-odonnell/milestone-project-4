from django import forms
from django.forms import inlineformset_factory
from .widgets import CustomClearableFileInput
from crispy_forms.helper import FormHelper
from .models import Activity, Feature, Itinerary, Package, Review


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        exclude = ('rating',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['image'].widget = CustomClearableFileInput()
        self.fields['description'].widget.attrs['rows'] = 8
        self.fields['category'].empty_label = ''
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['country'].empty_label = ''
        self.fields['country'].widget.attrs['class'] = 'form-select'
        self.fields['region'].empty_label = ''
        self.fields['region'].widget.attrs['class'] = 'form-select'


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Feature
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 form-label'
        self.helper.field_class = 'col-md-9'


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('package', 'full_name', 'date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
        self.fields['review'].widget.attrs['rows'] = 8


FeatureFormset = inlineformset_factory(
    Package, Feature, form=FeatureForm, extra=5, max_num=5)

ActivityFormset = inlineformset_factory(
    Package, Activity, form=ActivityForm, extra=1)

ItineraryFormset = inlineformset_factory(
    Package, Itinerary, form=ItineraryForm, extra=1)
