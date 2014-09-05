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

        #All of this data is accessible by hitting the format=json urls as documented in the README. Has more concise
        #dict values, but it is the same info.

        loc_list = []
        for obj in LocationSitRep.objects.exclude(location=national).order_by('location'):
            loc = str(obj.location)
            loc_list.append(loc)
        # print loc_list

        latest_date = SitRep.objects.latest('formatted_date')

        today = datetime.today().strftime("%j")
        latest = datetime.strftime(latest_date.formatted_date, "%j")
        nums = [int(latest)]
        num=int(latest)
        # print num
        while (num - 7) > 0:
            nums.append(num-7)
            num=num-7
        #     print num
        # print nums

        e_json=open('latest_data/export_main_weekly.json','w')
        deaths_list = []
        for obj in LocationSitRep.objects.filter(location=national).order_by('formatted_date'):
            if obj.date:
                d = datetime.strptime(obj.date, '%Y-%m-%d')
                doy = datetime.strftime(d, "%j")
                if int(doy) in nums:
                    obj_dict = {}
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
                    if obj.sit_rep == latest_date:
                        loc = Location.objects.get(name="National")
                        obj_dict.setdefault('new_weekly_deaths', loc.new_weekly_deaths)
                        obj_dict.setdefault('pct_change_death', loc.death_pct_change)
                        obj_dict.setdefault('new_weekly_cases', loc.new_weekly_cases)
                        obj_dict.setdefault('pct_change_cases', loc.cases_pct_change)
                        obj_dict.setdefault('new_weekly_deaths_hcw', loc.new_weekly_deaths_hcw)
                        obj_dict.setdefault('pct_change_death_hcw', loc.death_pct_change_hcw)
                        obj_dict.setdefault('new_weekly_cases_hcw', loc.new_weekly_cases_hcw)
                        obj_dict.setdefault('pct_change_cases_hcw', loc.cases_pct_change_hcw)
                    deaths_list.append(obj_dict)

        jsonified = json.dumps(deaths_list)
        print>>e_json, jsonified
        e_json.close()


        eb_json=open('latest_data/export_main.json','w')
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
                if obj.sit_rep == latest_date:
                    loc = Location.objects.get(name="National")
                    obj_dict.setdefault('new_weekly_deaths', loc.new_weekly_deaths)
                    obj_dict.setdefault('pct_change_death', loc.death_pct_change)
                    obj_dict.setdefault('new_weekly_cases', loc.new_weekly_cases)
                    obj_dict.setdefault('pct_change_cases', loc.cases_pct_change)
                    obj_dict.setdefault('new_weekly_deaths_hcw', loc.new_weekly_deaths_hcw)
                    obj_dict.setdefault('pct_change_death_hcw', loc.death_pct_change_hcw)
                    obj_dict.setdefault('new_weekly_cases_hcw', loc.new_weekly_cases_hcw)
                    obj_dict.setdefault('pct_change_cases_hcw', loc.cases_pct_change_hcw)
                deaths_list.append(obj_dict)

        jsonified = json.dumps(deaths_list)
        print>>eb_json, jsonified
        eb_json.close()
