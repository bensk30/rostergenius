from django.utils.safestring import mark_safe
from django.db import models

from geoposition.fields import GeopositionField

METHODS = [
    ('site', 'Site'),
    ('bookmarklet', 'Bookmarklet')
]

empty = {
    'blank': True,
    'null': True,
}

class Roster(models.Model):
    token          = models.CharField(max_length=200, **empty)
    event_title    = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)
    method         = models.CharField(max_length=100, choices=METHODS)
    created        = models.DateTimeField()
    success        = models.BooleanField()
    downloaded     = models.BooleanField(default=False)
    error          = models.CharField(max_length=100, **empty)
    dump           = models.TextField(**empty)


class Store(models.Model):
    name        = models.CharField(max_length=200)
    number      = models.CharField(max_length=10)
    address     = models.TextField(max_length=200, **empty)
    country     = models.CharField(max_length=200, **empty)
    geoposition = GeopositionField(**empty)
    link        = models.URLField(**empty)
    image       = models.URLField(**empty)
    phone       = models.CharField(max_length=200, **empty)
    retailme_id = models.CharField(max_length=200, **empty)

    def __unicode__(self):
        return "%s: %s" % (self.number, self.name)

    def image_tag(self):
        return mark_safe('<img style="max-height:100px" src="%s"/>' % self.image)
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'
