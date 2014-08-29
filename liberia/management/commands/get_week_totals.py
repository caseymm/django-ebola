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
        deaths = today_total.total_deaths_all - week_ago_total.total_deaths_all
        cases = today_total.cases_cum - week_ago_total.cases_cum
        print 'deaths'
        print deaths
        print (deaths/week_ago_total.total_deaths_all)*100
        print
        print 'cases'
        print cases
        print (cases/week_ago_total.cases_cum)*100
        print

        hcw_deaths = today_total.hcw_deaths_cum - week_ago_total.hcw_deaths_cum
        hcw_cases = today_total.hcw_cases_cum - week_ago_total.hcw_cases_cum
        print 'hcw deaths'
        print hcw_deaths
        print (hcw_deaths/week_ago_total.hcw_deaths_cum)*100
        print
        print 'hcw cases'
        print hcw_cases
        print (hcw_cases/week_ago_total.hcw_cases_cum)*100
