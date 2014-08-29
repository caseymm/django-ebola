import json
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):
        national = Location.objects.filter(name='National')

        loc_list = []
        for obj in LocationSitRep.objects.filter(date='2014-08-27').exclude(location=national).order_by('location'):
            loc = str(obj.location)
            loc_list.append(loc)
        # print loc_list





        deaths_list = []
        for obj in LocationSitRep.objects.filter(location=national, formatted_date__gte='2014-08-01').order_by('formatted_date'):
            if obj.date:
                obj_dict = {}
                d = datetime.strptime(obj.date, '%Y-%m-%d')
                obj_dict['Date'] = datetime.strftime(d, "%b %d")
                obj_dict['1. Total deaths in confirmed, probable and suspected cases'] = obj.total_deaths_all
                obj_dict['2. Total deaths in suspected cases'] = obj.total_deaths_suspected
                obj_dict['3. Total deaths in probable cases'] = obj.total_deaths_probable
                obj_dict['4. Total deaths in confirmed cases'] = obj.total_deaths_confirmed
                obj_dict['1. Total daily deaths'] = obj.deaths
                obj_dict['2. Daily deaths in suspected cases'] = obj.new_deaths_suspected
                obj_dict['3. Daily deaths in probable  cases'] = obj.new_deaths_probable
                obj_dict['4. Daily deaths in confirmed cases'] = obj.new_deaths_confirmed
                obj_dict['1. Total cases'] = obj.cases_cum
                obj_dict['2. Total suspected cases'] = obj.cases_cum_suspected
                obj_dict['3. Total probable cases'] = obj.cases_cum_probable
                obj_dict['4.Total confirmed cases'] = obj.cases_cum_confirmed
                obj_dict['1. Total new cases'] = obj.cases_new_total
                obj_dict['2. New suspected cases'] = obj.cases_new_suspected
                obj_dict['3. New probable cases'] = obj.cases_new_probable
                obj_dict['4. New confirmed cases'] = obj.cases_new_confirmed
                obj_dict['HealthCare worker new cases'] = obj.hcw_cases_new
                obj_dict['HealthCare worker total cases'] = obj.hcw_cases_cum
                obj_dict['HealthCare worker new deaths'] = obj.hcw_deaths_new
                obj_dict['HealthCare worker total deaths'] = obj.hcw_deaths_cum
                deaths_list.append(obj_dict)

        jsonified = json.dumps(deaths_list)
        print jsonified







        # print 'series:['
        # new_deaths = {}
        # for obj in LocationSitRep.objects.filter(date='2014-08-27').exclude(location=national).order_by('location').values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed'):
        #     for attr in obj:
        #         new_deaths.setdefault(attr, []).append(obj[attr])
        #     #     print obj[attr]
        #
        # for i in new_deaths:
        #     print '{'
        #     print 'name: '+i+','
        #     print 'data: '+str(new_deaths[i])
        #     print '},'
        # print ']'

        # locations = Location.objects.all()
        # for loc in locations:
        #     print loc.locationsitrep_set.values()