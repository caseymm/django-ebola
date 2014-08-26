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

class SitRep(models.Model):
    num = models.IntegerField(max_length=50, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True)
    date_span = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['num']

    def __unicode__(self):
        return self.num

class Location(models.Model):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class LocationSitRep(models.Model):
    sit_rep = models.ForeignKey('SitRep', null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True)
    num = models.IntegerField(max_length=50, blank=True, null=True)
    date_span = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=100, blank=True)
    total_probable_deaths = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum_probable = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_all = models.IntegerField(max_length=50, blank=True, null=True)
    deaths = models.IntegerField(max_length=50, blank=True, null=True)
    hc_workers = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_cases_cum = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_deaths_cum = models.IntegerField(max_length=50, blank=True, null=True)
    CFR = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['location']

    def __unicode__(self):
        return str(self.location)+', '+self.date_span
