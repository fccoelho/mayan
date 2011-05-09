from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import MetadataType

COORDINATE_TYPE_X = u'x'
COORDINATE_TYPE_Y = u'y'
COORDINATE_TYPE_XY = u'xy'
COORDINATE_TYPE_YX = u'yx'

COORDINATE_TYPE_CHOICES = (
    (COORDINATE_TYPE_X, _(u'X (horizontal) only')),
    (COORDINATE_TYPE_Y, _(u'Y (vertical) only')),
    (COORDINATE_TYPE_XY, _(u'Both, X (horizontal) first')),
    (COORDINATE_TYPE_YX, _(u'Both, Y (vertical) first')),
)


class GeocodedMetadata(models.Model):
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))
    coordinate_type = models.CharField(max_length=2, choices=COORDINATE_TYPE_CHOICES, verbose_name=_(u'coordinate type'))
    delimiter = models.CharField(max_length=8, blank=True, null=True, verbose_name=_(u'delimiter'))
    
    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'geocoded metadata')
        verbose_name_plural = _(u'geocoded metadata')
