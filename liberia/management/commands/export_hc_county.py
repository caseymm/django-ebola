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
        # print "county deaths info"

        # county_d = 'series:['
        # new_deaths = {}
        # for obj in LocationSitRep.objects.filter(sit_rep=latest_qs).exclude(location=national).order_by('location').values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed'):
        #     for attr in obj:
        #         new_deaths.setdefault(attr, []).append(obj[attr])
        #     #     print obj[attr]
        #
        # for i in new_deaths:
        #     county_d += '{'
        #     county_d += 'name: '+i+','
        #     county_d += 'data: '+str(new_deaths[i])
        #     county_d += '},'
        # county_d += ']'
        #
        # print>>county_json, county_d.replace(',]',']')
        # print>>county_json
        #
        # # print "county cases info"
        #
        # county_c = 'series:['
        # new_cases = {}
        # for obj in LocationSitRep.objects.filter(sit_rep=latest_qs).exclude(location=national).order_by('location').values('cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed'):
        #     for attr in obj:
        #         new_cases.setdefault(attr, []).append(obj[attr])
        #     #     print obj[attr]
        #
        # for i in new_cases:
        #     county_c += '{'
        #     county_c += 'name: '+i+','
        #     county_c += 'data: '+str(new_cases[i])
        #     county_c += '},'
        # county_c += ']'
        #
        # # print county_c.replace(',]',']')
        # print>>county_json, county_c.replace(',]',']')
        # county_json.close()

        latest = SitRep.objects.latest('formatted_date')
        nums = [int(latest.day_of_year)]
        num=int(latest.day_of_year)
        # print num
        while (num - 7) > 0:
            nums.append(num-7)
            num=num-7
        #     print num
        # print nums

        weekly_deaths = []
        weekly_cases = []
        for obj in LocationSitRep.objects.filter(location=national).order_by('formatted_date'):
            if obj.date:
                d = datetime.strptime(obj.date, '%Y-%m-%d')
                doy = datetime.strftime(d, "%j")
                if int(doy) in nums:
                    weekly_deaths.append(obj.deaths)
                    weekly_cases.append(obj.cases_new_total)

        county_cd = 'series:['
        new_cases = {}
        loc_query = LocationSitRep.objects.filter(sit_rep=latest_qs).exclude(location=national).order_by('location').values(
        'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed', 'total_deaths_suspected', 'total_deaths_probable',
         'total_deaths_confirmed')
        for obj in loc_query:
            # obj['weekly_deaths'] = weekly_deaths
            # obj['weekly_cases'] = weekly_cases
            for attr in obj:
                new_cases.setdefault(attr, []).append(obj[attr])

        for i in new_cases:
            county_cd += '{'
            county_cd += 'name: '+i+','
            county_cd += 'data: '+str(new_cases[i])
            county_cd += '},'
        county_cd += ']'

        print county_cd.replace(',]',']')
        # print>>county_json, county_cd.replace(',]',']')
        # county_json.close()
