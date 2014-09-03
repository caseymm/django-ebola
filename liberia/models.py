from __future__ import division
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
import time
import re
import urllib
import json
from datetime import datetime
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
    date = models.CharField(max_length=100, blank=True)
    formatted_date = models.DateField(null=True)
    date_span = models.CharField(max_length=100, blank=True)
    day_of_year = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return str(self.formatted_date)

    def get_doy(self):
        d = datetime.strptime(self.date, '%Y-%m-%d')
        self.day_of_year = datetime.strftime(d, "%j")
        return self.day_of_year

    def save(self):
        self.get_doy()
        call_command("test_this", noreload=True)
        super(SitRep, self).save()

class Location(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=100, blank=True)

    def create_slug(self):
        self.slug = slugify(self.name)
        return self.slug

    def save(self):
        self.create_slug()
        super(Location, self).save()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def _death_total(self):
        qs = LocationSitRep.objects.filter(location=self).latest('formatted_date')
        return qs

    death_total = property(_death_total)

    def _get_dates(self):
        sr_list = []
        latest_qs = SitRep.objects.latest('formatted_date')
        sr_list.append(latest_qs)
        sr_list.append(SitRep.objects.get(day_of_year=(latest_qs.day_of_year-7)))
        sr_list.append(SitRep.objects.get(day_of_year=(latest_qs.day_of_year-14)))
        return sr_list

    get_dates = property(_get_dates)

    def _get_relevant_srs(self):
        srs = self._get_dates()
        list_o_three = []
        list_o_three.append(LocationSitRep.objects.get(location=self, sit_rep=srs[0]))
        list_o_three.append(LocationSitRep.objects.get(location=self, sit_rep=srs[1]))
        list_o_three.append(LocationSitRep.objects.get(location=self, sit_rep=srs[2]))
        return list_o_three

    def _get_new_deaths(self):
        dates = self._get_relevant_srs()
        #get num of deaths
        deaths_total = dates[0].total_deaths_all
        week_ago_deaths_total = dates[1].total_deaths_all
        #get week vals
        deaths_this_week = deaths_total - week_ago_deaths_total
        return deaths_this_week

    new_weekly_deaths = property(_get_new_deaths)


    def _get_death_pct(self):
        dates = self._get_relevant_srs()
        #get num of deaths
        deaths_total = dates[0].total_deaths_all
        week_ago_deaths_total = dates[1].total_deaths_all
        two_week_ago_deaths_total = dates[2].total_deaths_all
        #get week vals
        deaths_this_week = deaths_total - week_ago_deaths_total
        deaths_last_week = week_ago_deaths_total - two_week_ago_deaths_total
        try:
            pct_change = ((deaths_this_week-deaths_last_week)/deaths_last_week)*100
        except:
            pct_change = 'N/A'
        return pct_change

    death_pct_change = property(_get_death_pct)

    def _get_new_cases(self):
        dates = self._get_relevant_srs()
        #get num of deaths
        cases_total = dates[0].cases_cum
        week_ago_cases_total = dates[1].cases_cum
        #get week vals
        cases_this_week = cases_total - week_ago_cases_total
        return cases_this_week

    new_weekly_cases = property(_get_new_cases)

    def _get_cases_pct(self):
        dates = self._get_relevant_srs()
        #get num of cases
        cases_total = dates[0].cases_cum
        week_ago_cases_total = dates[1].cases_cum
        two_week_ago_cases_total = dates[2].cases_cum
        #get week vals
        cases_this_week = cases_total - week_ago_cases_total
        cases_last_week = week_ago_cases_total - two_week_ago_cases_total
        try:
            pct_change = ((cases_this_week-cases_last_week)/cases_last_week)*100
        except:
            pct_change = 'N/A'
        return pct_change

    cases_pct_change = property(_get_cases_pct)

    def _get_new_deaths_hcw(self):
        dates = self._get_relevant_srs()
        #get num of deaths
        deaths_total = dates[0].hcw_deaths_cum
        week_ago_deaths_total = dates[1].hcw_deaths_cum
        #get week vals
        deaths_this_week = deaths_total - week_ago_deaths_total
        return deaths_this_week

    new_weekly_deaths_hcw = property(_get_new_deaths_hcw)


    def _get_death_pct_hcw(self):
        dates = self._get_relevant_srs()
        #get num of deaths
        deaths_total = dates[0].hcw_deaths_cum
        week_ago_deaths_total = dates[1].hcw_deaths_cum
        two_week_ago_deaths_total = dates[2].hcw_deaths_cum
        #get week vals
        deaths_this_week = deaths_total - week_ago_deaths_total
        deaths_last_week = week_ago_deaths_total - two_week_ago_deaths_total
        try:
            pct_change = ((deaths_this_week-deaths_last_week)/deaths_last_week)*100
        except:
            pct_change = 'N/A'
        return pct_change

    death_pct_change_hcw = property(_get_death_pct_hcw)

    def _get_new_cases_hcw(self):
        dates = self._get_relevant_srs()
        #get num of cases
        cases_total = dates[0].hcw_cases_cum
        week_ago_cases_total = dates[1].hcw_cases_cum
        #get week vals
        cases_this_week = cases_total - week_ago_cases_total
        return cases_this_week

    new_weekly_cases_hcw = property(_get_new_cases_hcw)


    def _get_cases_pct_hcw(self):
        dates = self._get_relevant_srs()
        #get num of casess
        cases_total = dates[0].hcw_cases_cum
        week_ago_cases_total = dates[1].hcw_cases_cum
        two_week_ago_cases_total = dates[2].hcw_cases_cum
        #get week vals
        cases_this_week = cases_total - week_ago_cases_total
        cases_last_week = week_ago_cases_total - two_week_ago_cases_total
        try:
            pct_change = ((cases_this_week-cases_last_week)/cases_last_week)*100
        except:
            pct_change = 'N/A'
        return pct_change

    cases_pct_change_hcw = property(_get_cases_pct_hcw)



class LocationSitRep(models.Model):
    sit_rep = models.ForeignKey('SitRep', null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True)
    date_span = models.CharField(max_length=100, blank=True)
    formatted_date = models.DateField(null=True)
    date = models.CharField(max_length=100, blank=True)
    total_deaths_probable = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum_probable = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    cases_cum = models.IntegerField(max_length=50, blank=True, null=True)
    cases_new_total = models.IntegerField(max_length=50, blank=True, null=True)
    cases_new_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    cases_new_probable = models.IntegerField(max_length=50, blank=True, null=True)
    cases_new_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    total_deaths_all = models.IntegerField(max_length=50, blank=True, null=True)
    deaths = models.IntegerField(max_length=50, blank=True, null=True)
    new_deaths_probable = models.IntegerField(max_length=50, blank=True, null=True)
    new_deaths_suspected = models.IntegerField(max_length=50, blank=True, null=True)
    new_deaths_confirmed = models.IntegerField(max_length=50, blank=True, null=True)
    hc_workers = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_cases_new = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_cases_cum = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_deaths_new = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_deaths_cum = models.IntegerField(max_length=50, blank=True, null=True)
    CFR = models.CharField(max_length=100, null=True, blank=True)
    admission_new = models.IntegerField(max_length=50, blank=True, null=True)
    in_treatment = models.IntegerField(max_length=50, blank=True, null=True)
    total_discharges = models.IntegerField(max_length=50, blank=True, null=True)
    admission_cum = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return str(self.location)+', '+str(self.formatted_date)

class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name+' ('+str(self.crisisnetentry_set.count())+')'

class Author(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name

class CrisisNetEntry(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey('Author', null=True, blank=True)
    publishedAt = models.CharField(max_length=500, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    source = models.CharField(max_length=500, blank=True)
    lifespan = models.CharField(max_length=500, blank=True)
    updatedAt = models.CharField(max_length=500, blank=True)
    longitude = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=500, blank=True)
    is_geocoded = models.BooleanField(default=False)
    createdAt = models.CharField(max_length=500, blank=True)
    remoteID = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['createdAt', 'is_geocoded', 'author', 'source']
        verbose_name_plural=u'Crisis Net Entries'

    def __unicode__(self):
        return self.createdAt

class Summary(models.Model):
    date = models.DateField(null=True)
    total_deaths = models.IntegerField(max_length=50, blank=True, null=True)
    deaths_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    deaths_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_cases = models.IntegerField(max_length=50, blank=True, null=True)
    cases_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    cases_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_contacts = models.IntegerField(max_length=50, blank=True, null=True)
    contacts_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    contacts_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_hcw_deaths = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_deaths_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_deaths_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_hcw_cases = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_cases_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    hcw_cases_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_labs_processed = models.IntegerField(max_length=50, blank=True, null=True)
    labs_processed_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    labs_processed_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_labs_collected = models.IntegerField(max_length=50, blank=True, null=True)
    labs_collected_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    labs_collected_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_fcr = models.IntegerField(max_length=50, blank=True, null=True)
    fcr_last_week = models.IntegerField(max_length=50, blank=True, null=True)
    fcr_this_week = models.IntegerField(max_length=50, blank=True, null=True)
    total_clinics = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural=u'Summaries'

    def __unicode__(self):
        return str(self.date)
