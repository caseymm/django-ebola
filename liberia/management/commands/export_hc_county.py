from __future__ import division
import json
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):
        national = Location.objects.filter(name='National')

        latest_qs = SitRep.objects.latest('formatted_date')
        county_json=open('latest_data/highcharts_county.json','w')

        #produces json with arrays where each entry in the array represents the total deaths or cases for that county
        new_cds = {}
        d_dict = {}
        c_dict = {}
        for obj in LocationSitRep.objects.filter(sit_rep=latest_qs).exclude(location=national).order_by('location').values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed'):
            d_dict.setdefault('total_deaths_suspected', []).append(obj['total_deaths_suspected'])
            d_dict.setdefault('total_deaths_probable', []).append(obj['total_deaths_probable'])
            d_dict.setdefault('total_deaths_confirmed', []).append(obj['total_deaths_confirmed'])
            new_cds.setdefault("deaths", d_dict)
            c_dict.setdefault('cases_cum_suspected', []).append(obj['cases_cum_suspected'])
            c_dict.setdefault('cases_cum_probable', []).append(obj['cases_cum_probable'])
            c_dict.setdefault('cases_cum_confirmed', []).append(obj['cases_cum_confirmed'])
            new_cds.setdefault("cases", c_dict)


        jsonified = json.dumps(new_cds)
        print>>county_json, jsonified
        county_json.close()
