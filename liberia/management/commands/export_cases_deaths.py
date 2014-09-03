import json
import cPickle
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary cases and deaths from db to json for charts'

    def handle(self, *args, **options):
        national = Location.objects.filter(name='National')
        sr_all = SitRep.objects.all()

        # print 'National all fields (March - present)'
        n_all=open('latest_data/cd_national_all_fields.json','w')
        nat_all_list = []
        for i in sr_all:
            for each in i.locationsitrep_set.values('date', 'total_deaths_probable', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed', 'cases_cum', 'cases_new_total', 'cases_new_suspected', 'cases_new_probable', 'cases_new_confirmed', 'total_deaths_suspected', 'total_deaths_confirmed', 'total_deaths_all', 'deaths', 'new_deaths_probable', 'new_deaths_suspected', 'new_deaths_confirmed').filter(location=national):
                nat_all_list.append(each)

        jsonified_nat_all = json.dumps(nat_all_list)
        print>>n_all, jsonified_nat_all
        n_all.close()

        # print 'National Simple'
        n_simple=open('latest_data/cd_national_simple.json','w')
        nat_simple_list = []
        for i in sr_all:
            for each in i.locationsitrep_set.values('date', 'cases_cum', 'cases_new_total', 'total_deaths_all', 'deaths').filter(location=national):
                nat_simple_list.append(each)

        jsonified_nat_simple = json.dumps(nat_simple_list)
        print>>n_simple, jsonified_nat_simple
        n_simple.close()
