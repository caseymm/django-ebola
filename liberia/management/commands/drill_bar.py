import json
import cPickle
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):

        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        national = Location.objects.filter(name='National')
        latest_sr = SitRep.objects.latest('formatted_date')

        print 'Not including national'
        print
        no_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').exclude(location=national):
            no_nat_list.append(i)

        jsonified_nn = json.dumps(no_nat_list)
        print jsonified_nn

        print
        print
        print 'Including national'
        print
        inc_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum'):
            inc_nat_list.append(i)

        jsonified_incn = json.dumps(inc_nat_list)
        print jsonified_incn

        print
        print
        print 'just national'
        print
        nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').filter(location=national):
            nat_list.append(i)

        jsonified_n = json.dumps(nat_list)
        print jsonified_n
