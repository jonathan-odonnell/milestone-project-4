from django import forms
from holidays.widgets import CustomClearableFileInput
from .models import Extra
from crispy_forms.helper import FormHelper


class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        exclude = ('image_url',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.helper.label_class = 'form-label'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['image'].widget = CustomClearableFileInput()
        self.fields['description'].widget.attrs['rows'] = 8
