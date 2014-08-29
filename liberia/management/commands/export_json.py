import json
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):
        national = Location.objects.filter(name='National')
        deaths_list = []
        for obj in LocationSitRep.objects.filter(location=national).order_by('formatted_date'):
            if obj.date:
                obj_dict = {}
                d = datetime.strptime(obj.date, '%Y-%m-%d')
                obj_dict['Date'] = datetime.strftime(d, "%b %d")
                obj_dict['1. Total deaths in confirmed, probable and suspected cases'] = obj.total_deaths_all
                obj_dict['2. Total deaths in suspected cases'] = obj.total_deaths_suspected
                obj_dict['3. Total deaths in probable cases'] = obj.total_deaths_probable
                obj_dict['4. Total deaths in confirmed cases'] = obj.total_deaths_confirmed
                deaths_list.append(obj_dict)

        jsonified = json.dumps(deaths_list)
        print jsonified

        print 'series:['
        new_deaths = {}
        for obj in LocationSitRep.objects.filter(date='2014-08-27').exclude(location=national).order_by('location').values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed'):
            for attr in obj:
                new_deaths.setdefault(attr, []).append(obj[attr])
            #     print obj[attr]

        for i in new_deaths:
            print '{'
            print 'name: '+i+','
            print 'data: '+str(new_deaths[i])
            print '},'
        print ']'
