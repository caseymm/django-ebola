import json
import cPickle
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):
        exp_county=open('latest_data/export_county_wdaily.json','w')
        latest_sr = SitRep.objects.latest('formatted_date')
        latest = datetime.strftime(latest_sr.formatted_date, "%j")

        national = Location.objects.filter(name='National')

        print>>exp_county, 'Not including national'
        print>>exp_county
        no_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').exclude(location=national):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            no_nat_list.append(i)

        jsonified_nn = json.dumps(no_nat_list)
        print>>exp_county, jsonified_nn

        print>>exp_county
        print>>exp_county
        print>>exp_county, 'Including national'
        print>>exp_county
        inc_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum'):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            inc_nat_list.append(i)

        jsonified_incn = json.dumps(inc_nat_list)
        print>>exp_county, jsonified_incn

        print>>exp_county
        print>>exp_county
        print>>exp_county, 'just national'
        print>>exp_county
        nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').filter(location=national):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            nat_list.append(i)

        jsonified_n = json.dumps(nat_list)
        print>>exp_county, jsonified_n

        exp_county.close()
