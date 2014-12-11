from django.db import models

from djangotoolbox.fields import ListField

class Film(models.Model):
    """
    Contains all of the information for a particular film shoot. We can store zero to many locations
    for a particular film, though our management script will delete any shoots that don't have any
    locations.
    """
    title = models.CharField(max_length=200, default="", blank=True)
    release_year = models.CharField(max_length=4, default="", blank=True)
    location = ListField()

    def __unicode__(self):
        return self.title