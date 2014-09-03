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
        print "county deaths info"

        county_d = 'series:['
        new_deaths = {}
        for obj in LocationSitRep.objects.filter(sit_rep=latest_qs).exclude(location=national).order_by('location').values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed'):
            for attr in obj:
                new_deaths.setdefault(attr, []).append(obj[attr])
            #     print obj[attr]

        for i in new_deaths:
            county_d += '{'
            county_d += 'name: '+i+','
            county_d += 'data: '+str(new_deaths[i])
            county_d += '},'
        county_d += ']'

        print county_d.replace(',]',']')

        # locations = Location.objects.all()
        # for loc in locations:
        #     print loc.locationsitrep_set.values()

        print "county cases info"

        county_c = 'series:['
        new_cases = {}
        for obj in LocationSitRep.objects.filter(sit_rep=latest_qs).exclude(location=national).order_by('location').values('cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed'):
            for attr in obj:
                new_cases.setdefault(attr, []).append(obj[attr])
            #     print obj[attr]

        for i in new_cases:
            county_c += '{'
            county_c += 'name: '+i+','
            county_c += 'data: '+str(new_cases[i])
            county_c += '},'
        county_c += ']'

        print county_c.replace(',]',']')
