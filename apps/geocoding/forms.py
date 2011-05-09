from django import forms
from django.utils.translation import ugettext_lazy as _

from geocoding.widgets import LocationPickerWidget


class LocationForm(forms.Form):
    test = forms.CharField(widget=LocationPickerWidget())
