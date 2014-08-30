import json
import cPickle
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):

        print 'HCW graph data for cases and deaths'

        national = Location.objects.filter(name='National')
        sr_all = SitRep.objects.all()
        sr_aug = SitRep.objects.filter(formatted_date__gte='2014-08-01')

        print 'National all (March - present)'
        n_all=open('hcw_national_all.json','w')
        print
        nat_all_list = []
        for i in sr_all:
            for each in i.locationsitrep_set.values('date', 'hcw_cases_new', 'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum').filter(location=national):
                nat_all_list.append(each)

        jsonified_nat_all = json.dumps(nat_all_list)
        print>>n_all, jsonified_nat_all
        n_all.close()

        print 'National August'
        n_aug=open('hcw_national_aug.json','w')
        print
        nat_aug_list = []
        for i in sr_aug:
            for each in i.locationsitrep_set.values('date', 'hcw_cases_new', 'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum').filter(location=national):
                nat_aug_list.append(each)

        jsonified_nat_aug = json.dumps(nat_aug_list)
        print>>n_aug, jsonified_nat_aug
        n_aug.close()

        print 'Locations all (March - present)'
        loc_all=open('hcw_locations_all.json','w')
        print
        all_locs_list = []
        for i in sr_all:
            date_dict = {}
            for each in i.locationsitrep_set.values('location__name','date', 'hcw_cases_new', 'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum').exclude(location=national):
                date_dict.setdefault(each['date'], []).append(each)
            all_locs_list.append(date_dict)

        jsonified_all_locs = json.dumps(all_locs_list)
        print>>loc_all, jsonified_all_locs
        loc_all.close()

        print 'Locations August'
        loc_aug=open('hcw_locations_aug.json','w')
        print
        aug_locs_list = []
        for i in sr_aug:
            date_dict = {}
            for each in i.locationsitrep_set.values('location__name','date', 'hcw_cases_new', 'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum').exclude(location=national):
                date_dict.setdefault(each['date'], []).append(each)
            aug_locs_list.append(date_dict)

        jsonified_aug_locs = json.dumps(aug_locs_list)
        print>>loc_aug, jsonified_aug_locs
        loc_aug.close()
