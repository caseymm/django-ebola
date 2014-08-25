from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
import time
import re
import urllib
from StringIO import StringIO
from operator import itemgetter
from django.core.management import call_command


class DateStats(models.Model):
    original_date = models.CharField(max_length=50, blank=True)
    date = models.DateField(null=True)
    total_cases = models.IntegerField(max_length=50, blank=True, null=True)
    total_suspected_cases = models.IntegerField(max_length=50, blank=True, null=True)
    total_probable_cases = models.IntegerField(max_length=50, blank=True, null=True)
    total_confirmed_cases = models.IntegerField(max_length=50, blank=True, null=True)
    new_cases = models.IntegerField(max_length=50, blank=True, null=True)
    new_suspected_cases = models.IntegerField(max_length=50, blank=True, null=True)
    new_probable_cases = models.IntegerField(max_length=50, blank=True, null=True)
    new_confirmed_cases = models.IntegerField(max_length=50, blank=True, null=True)
    news_contacts = models.IntegerField(max_length=50, blank=True, null=True)
    contacts_completed_observation = models.IntegerField(max_length=50, blank=True, null=True)
    contacts_lost_followup = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_all = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_probable = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    today_deaths_all = models.IntegerField(max_length=50, blank=True, null=True)
    today_deaths_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    today_deaths_probable = models.IntegerField(max_length=50, blank=True, null=True)
    today_deaths_confirmed = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural=u'Date statistics'

    def __unicode__(self):
        return str(self.date)
