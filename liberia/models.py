from __future__ import division
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django import forms
import time
import re
import urllib
import requests
import json
from datetime import datetime
from StringIO import StringIO
from operator import itemgetter
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
import time
from datetime import datetime
from django.core.management import call_command

class WeekOfYear(models.Model):
    week = models.IntegerField(max_length=50, blank=True, null=True)
    year = models.IntegerField(max_length=50, blank=True, null=True)
    new_cases = models.IntegerField(max_length=50, blank=True, null=True)
    new_deaths = models.IntegerField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-week', '-year']

    def __unicode__(self):
        return str(self.week)+' '+str(self.year)


class SitRep(models.Model):
    date = models.CharField(max_length=100, blank=True)
    formatted_date = models.DateField(null=True)
    date_span = models.CharField(max_length=100, blank=True)
    day_of_year = models.IntegerField(max_length=50, blank=True, null=True)
    week_of_year = models.ForeignKey('WeekOfYear', null=True, blank=True)
    is_copy = models.BooleanField(default=False)


    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return str(self.formatted_date)

    def get_doy(self):
        d = datetime.strptime(self.date, '%Y-%m-%d')
        self.day_of_year = datetime.strftime(d, "%j")
        return self.day_of_year

    def get_woy(self):
        d = datetime.strptime(self.date, '%Y-%m-%d')
        week = datetime.strftime(d, "%U")
        year = datetime.strftime(d, "%Y")
        current_week, created = WeekOfYear.objects.get_or_create(week=week, year=year)
        self.week_of_year = current_week
        return self.week_of_year

    def save(self, **kwargs):
        self.get_doy()
        self.get_woy()
        # self.upload_file()
        super(SitRep, self).save()

class Location(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=100, blank=True)
    weekly_deaths = models.TextField(blank=True)
    weekly_cases = models.TextField(blank=True)

    def create_slug(self):
        self.slug = slugify(self.name)
        return self.slug

    def save(self, **kwargs):
        self.create_slug()
        super(Location, self).save()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def _dc_totals(self):
        qs = LocationSitRep.objects.filter(location=self).latest('formatted_date')
        return qs

    dc_totals = property(_dc_totals)

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
            pct_change = round((((deaths_this_week-deaths_last_week)/deaths_last_week)*100), 2)
            return pct_change
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
            pct_change = round((((cases_this_week-cases_last_week)/cases_last_week)*100), 2)
            return pct_change
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
            pct_change = round((((deaths_this_week-deaths_last_week)/deaths_last_week)*100), 2)
            return pct_change
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
            pct_change = round((((cases_this_week-cases_last_week)/cases_last_week)*100), 2)
            return round(pct_change, 2)
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
    auto_new_deaths = models.IntegerField(max_length=50, blank=True, null=True) #if we aren't given the new deaths
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

    def _get_previous_sr(self):
        latest_qs = SitRep.objects.filter(date=self.sit_rep)
        previous_sr = SitRep.objects.get(day_of_year=(latest_qs[0].day_of_year-1))
        return previous_sr

    def _get_relevant_loc_sr(self):
        previous_sr_doy = self._get_previous_sr()
        prev_loc_sr = LocationSitRep.objects.get(location=self.location, sit_rep=previous_sr_doy)
        return prev_loc_sr

    def _get_previous_sr_b(self):
        latest_qs = SitRep.objects.filter(date=self.sit_rep)
        previous_sr = SitRep.objects.get(day_of_year=(latest_qs[0].day_of_year-2))
        return previous_sr

    def _get_relevant_loc_sr_b(self):
        previous_sr_doy = self._get_previous_sr_b()
        prev_loc_sr_b = LocationSitRep.objects.get(location=self.location, sit_rep=previous_sr_doy)
        return prev_loc_sr_b

    def _get_new_deaths_alt(self):
        yesterday = self._get_relevant_loc_sr()
        two_ago = self._get_relevant_loc_sr_b()
        new_total_deaths = self.total_deaths_all
        yesterday_total_deaths = yesterday.total_deaths_all
        if yesterday_total_deaths > two_ago.total_deaths_all:
            self.auto_new_deaths = new_total_deaths - yesterday_total_deaths
        else:
            self.auto_new_deaths = new_total_deaths - two_ago.total_deaths_all
        return self.auto_new_deaths

    def _display_valid_number(self):
        if self.deaths:
            return self.deaths
        else:
            if self.auto_new_deaths >= 0:
                return self.auto_new_deaths
            else:
                return 'Null'

    show_new_death_num = property(_display_valid_number)

    def save(self, **kwargs):
        try:
            self._get_new_deaths_alt()
        except:
            pass
        self._display_valid_number()
        super(LocationSitRep, self).save()


class Document(models.Model):
    docfile = models.FileField(upload_to='sitreps')
    sit_rep_date = models.CharField(max_length=200, blank=True)
    month_format = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.sit_rep_date

    def save(self, **kwargs):
        strp_time = time.strptime(self.sit_rep_date, "%Y-%m-%d")
        print strp_time
        date = datetime.fromtimestamp(time.mktime(strp_time))
        print date

        year = datetime.strftime(date, "%Y")
        date_ending = datetime.strftime(date, "%d")
        de = str(date_ending)

        if de[-2] == '0':
            de = de[1:]

        st = '1'
        nd = '2'
        rd = '3'
        th = ['4', '5', '6', '7', '8', '9', '0']

        if len(de) == 1:
            if de == st:
                de += 'st'
            elif de == nd:
                de += 'nd'
            elif de == rd:
                de += 'rd'
            else:
                de += 'th'
        elif len(de) == 2:
            if de[-2] == '1':
                de += 'th'
            else:
                if de[-1] == st:
                    de += 'st'
                elif de[-1] == nd:
                    de += 'nd'
                elif de[-1] == rd:
                    de += 'rd'
                else:
                    de += 'th'

        current_sit_rep, created = SitRep.objects.get_or_create(date=self.sit_rep_date, formatted_date=date)
        cdoy = int(current_sit_rep.day_of_year)

        #latest sitrep before this one
        temp_latest =  SitRep.objects.all().order_by('-date')[1]
        dates_needed = []
        while cdoy - temp_latest.day_of_year > 1:
            cdoy+=-1
            dates_needed.append(cdoy)

        dates_needed.reverse()
        for dn in dates_needed:
            d = datetime.strptime(str(dn), '%j')
            get_date = datetime.strftime(d, '2014-%m-%d')
            copy_sit_rep, created = SitRep.objects.get_or_create(date=get_date, formatted_date=get_date, is_copy=True)
            loc_info = LocationSitRep.objects.filter(sit_rep=temp_latest)
            for lsr in loc_info:
                new_lsr, created = LocationSitRep.objects.get_or_create(sit_rep=copy_sit_rep, location=lsr.location, date=get_date, formatted_date=get_date, auto_new_deaths=lsr.auto_new_deaths)
                new_lsr.cases_new_probable = lsr.cases_new_probable
                new_lsr.total_deaths_suspected = lsr.total_deaths_suspected
                new_lsr.total_discharges = lsr.total_discharges
                new_lsr.hcw_deaths_new = lsr.hcw_deaths_new
                new_lsr.total_deaths_confirmed = lsr.total_deaths_confirmed
                new_lsr.deaths = lsr.deaths
                new_lsr.CFR = lsr.CFR
                new_lsr.total_deaths_all = lsr.total_deaths_all
                new_lsr.admission_cum = lsr.admission_cum
                new_lsr.cases_new_confirmed = lsr.cases_new_confirmed
                new_lsr.cases_new_suspected = lsr.cases_new_suspected
                new_lsr.cases_cum = lsr.cases_cum
                new_lsr.cases_cum_probable = lsr.cases_cum_probable
                new_lsr.in_treatment = lsr.in_treatment
                new_lsr.hcw_cases_cum = lsr.hcw_cases_cum
                new_lsr.cases_cum_confirmed = lsr.cases_cum_confirmed
                new_lsr.admission_new = lsr.admission_new
                new_lsr.hcw_deaths_cum = lsr.hcw_deaths_cum
                new_lsr.cases_cum_suspected = lsr.cases_cum_suspected
                new_lsr.hcw_cases_new = lsr.hcw_cases_new
                new_lsr.total_deaths_probable = lsr.total_deaths_probable
                new_lsr.cases_new_total = (int(lsr.cases_new_suspected)+int(lsr.cases_new_probable)+int(lsr.cases_new_confirmed))
                new_lsr.save()

        df = pd.io.excel.read_excel(self.docfile, 0, index_col=None, na_values=['NA'])
        sliced = df[:34]
        flipped = sliced.T
        idx = flipped.set_index([3])
        flipback = idx.T
        get_index = flipback.columns[0]
        idx = flipback.set_index(get_index)
        loc_dict = idx.to_dict()
        for i in loc_dict:
            county = loc_dict[i]
            for i in county:
                try:
                    county[i] = int(county[i])
                except:
                    county[i] = 0

        for i in loc_dict:
            current_loc, created = Location.objects.get_or_create(name=i.strip())
            new_loc_sr, created = LocationSitRep.objects.get_or_create(location=current_loc, sit_rep=current_sit_rep)

            new_loc_sr.date = self.sit_rep_date
            new_loc_sr.formatted_date = date

            new_loc_sr.cases_new_probable = loc_dict[i].get("New Case/s (Probable)")
            new_loc_sr.total_deaths_suspected = loc_dict[i].get("Total death/s in suspected cases")
            new_loc_sr.total_discharges = loc_dict[i].get("Total discharges on "+self.month_format+" "+de+". "+year+"")
            new_loc_sr.hcw_deaths_new = loc_dict[i].get("Newly Reported deaths in HCW on "+self.month_format+" "+de+". "+year+"")
            new_loc_sr.total_deaths_confirmed = loc_dict[i].get("Total death/s in confirmed cases")
            new_loc_sr.deaths = loc_dict[i].get("Newly reported deaths "+self.month_format+" "+de+". "+year+"")
            new_loc_sr.CFR = loc_dict[i].get("Case Fatality Rate (CFR) - Confirmed & Probable Cases")
            new_loc_sr.total_deaths_all = loc_dict[i].get("Total death/s in confirmed, probable, suspected cases")
            new_loc_sr.admission_cum = loc_dict[i].get("Cumulative admission/isolation ")
            new_loc_sr.cases_new_confirmed = loc_dict[i].get("New case/s (confirmed) ")
            new_loc_sr.cases_new_suspected = loc_dict[i].get("New Case/s (Suspected)")
            new_loc_sr.cases_cum = loc_dict[i].get("Cumulative (confirmed, probable, suspected) cases")
            new_loc_sr.cases_cum_probable = loc_dict[i].get("Total probable cases")
            new_loc_sr.in_treatment = loc_dict[i].get("Total no. currently in Treatment Units")
            new_loc_sr.hcw_cases_cum = loc_dict[i].get("Cumulative  cases among HCW ")
            new_loc_sr.cases_cum_confirmed = loc_dict[i].get("Total confirmed cases")
            new_loc_sr.admission_new = loc_dict[i].get("New Admission on "+self.month_format+" "+de+". "+year+"")
            new_loc_sr.hcw_deaths_cum = loc_dict[i].get("Cumulative  deaths among HCW ")
            new_loc_sr.cases_cum_suspected = loc_dict[i].get("Total suspected cases")
            new_loc_sr.hcw_cases_new = loc_dict[i].get("Newly Reported Cases in HCW on "+self.month_format+" "+de+". "+year+"")
            new_loc_sr.total_deaths_probable = loc_dict[i].get("Total death/s in probable cases")
            new_loc_sr.cases_new_total = (int(new_loc_sr.cases_new_suspected)+int(new_loc_sr.cases_new_probable)+int(new_loc_sr.cases_new_confirmed))
            new_loc_sr.is_copy = False
            new_loc_sr.save()


        call_command("get_new_weekly")  #Gets the weekly total in change of deaths and cases and appends to Location

        #former location where I'd write the static files - just noting for future reference

        r = requests.get('http://ebolainliberia.org/scripts/grab-data.php', headers={'Connection':'close'})
        super(Document, self).save()
