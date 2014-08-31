from __future__ import division
import json
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime


class Command(BaseCommand):
    help = 'Get week totals for cases and deaths'

    def handle(self, *args, **options):
        national = Location.objects.filter(name='National')

        today_total = LocationSitRep.objects.get(date='2014-08-27', location=national)
        week_ago_total = LocationSitRep.objects.get(date='2014-08-20', location=national)
        two_week_ago_total = LocationSitRep.objects.get(date='2014-08-13', location=national)

        deaths_this_week = today_total.total_deaths_all - week_ago_total.total_deaths_all
        deaths_last_week = week_ago_total.total_deaths_all - two_week_ago_total.total_deaths_all

        cases_this_week = today_total.cases_cum - week_ago_total.cases_cum
        cases_last_week = week_ago_total.cases_cum - two_week_ago_total.cases_cum

        print 'new deaths this week'
        print deaths_this_week
        print 'new deaths last week'
        print deaths_last_week
        print ((deaths_this_week-deaths_last_week)/deaths_last_week)*100
        print
        print 'new cases this week'
        print cases_this_week
        print 'new cases last week'
        print cases_last_week
        print ((cases_this_week-cases_last_week)/cases_last_week)*100
        print

        hcw_deaths_this_week = today_total.hcw_deaths_cum - week_ago_total.hcw_deaths_cum
        hcw_deaths_last_week = week_ago_total.hcw_deaths_cum - two_week_ago_total.hcw_deaths_cum

        hcw_cases_this_week = today_total.hcw_cases_cum - week_ago_total.hcw_cases_cum
        hcw_cases_last_week = week_ago_total.hcw_cases_cum - two_week_ago_total.hcw_cases_cum
        print 'new hcw deaths this week'
        print hcw_deaths_this_week
        print 'new hcw deaths last week'
        print hcw_deaths_last_week
        print ((hcw_deaths_this_week-hcw_deaths_last_week)/hcw_deaths_last_week)*100
        print
        print 'new hcw cases this week'
        print hcw_cases_this_week
        print 'new hcw cases last week'
        print hcw_cases_last_week
        print ((hcw_cases_this_week-hcw_cases_last_week)/hcw_cases_last_week)*100
