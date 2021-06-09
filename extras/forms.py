from django import forms
from holidays.widgets import CustomClearableFileInput
from .models import Extra
from crispy_forms.helper import FormHelper


class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        exclude = ('image_url',)

    def __init__(self, *args, **kwargs):
        """
        Sets the image field widget as the CustomClearableFileInput, adds
        classe and amends the description textarea number of rows. Code for
        setting the field_class and label_class is from
        https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
        self.fields['image'].widget = CustomClearableFileInput()
        self.fields['description'].widget.attrs['rows'] = 8
