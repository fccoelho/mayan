import os

from django import forms
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

MEDIA_LOCATION = u'packages/location_picker'

# http://djangosnippets.org/snippets/752/
# http://code.google.com/p/django-gmapi/source/browse/gmapi/forms/widgets.py?r=65c30523b078bcab1bee698293912bb49dec9fb8
# http://facstaff.unca.edu/mcmcclur/GoogleMaps/Projections/
# http://earth.google.com/support/bin/static.py?page=guide.cs&guide=22373&topic=23750&answer=148111

class LocationPickerWidget(forms.widgets.Widget):
    class Media:
        css = {
            'all':(
                os.path.join(settings.MEDIA_URL, MEDIA_LOCATION, u'location_picker.css'),
            )
        }
        js = (
            u'http://www.google.com/jsapi?key=%s' % getattr(settings, 'GOOGLE_MAPS_API_KEY', u''),
            os.path.join(settings.MEDIA_URL, MEDIA_LOCATION, u'jquery.location_picker.js'),
        )

    def __init__(self, language=None, attrs=None):
        self.help_text = _(u'Move the marker to the desired location to update the coordinates.')
        #self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        #if isinstance(value, unicode):
        #    x, y = value.split(DELIMITER)
        #else:
        #    x, y = value
        #lat, lng = float(x), float(y)
        
        if None == attrs:
            attrs = {}
        attrs['class'] = u'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)
