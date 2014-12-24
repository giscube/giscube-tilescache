import os
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' % self.title or self.name


LAYER_TYPE_CHOICES = [ 
    ('WMS', 'WMS'),
]


class Layer(models.Model):
    service = models.ForeignKey(Service, related_name='layers')
    type = models.CharField(max_length=10, choices=LAYER_TYPE_CHOICES)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    layers = models.CharField(max_length=255, null=True, blank=True)
    projection = models.IntegerField(help_text='EPSG code')
    tms_type = models.CharField(max_length=10, null=True, blank=True)
    levels = models.IntegerField(null=True, blank=True)
    bbox = models.CharField(max_length=100, null=True, blank=True)
    resolutions = models.CharField(max_length=1024, null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    debug = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % self.title or self.name
