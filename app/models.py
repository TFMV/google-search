from __future__ import unicode_literals

from django.db import models

class SearchHistory(models.Model):
    search_dt = models.DateField()
    search_count = models.IntegerField(default=0)

class Terms(models.Model):
    term = models.TextField()
