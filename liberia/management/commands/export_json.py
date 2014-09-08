from __future__ import division
import json
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):

        latest_date = SitRep.objects.latest('formatted_date')

        latest = datetime.strftime(latest_date.formatted_date, "%j")
        nums = [int(latest)]
        num=int(latest)
        # print num
        while (num - 7) > 0:
            nums.append(num-7)
            num=num-7

        nat = Location.objects.get(name='National')
        list = []
        filtered_list = []
        location_vals = LocationSitRep.objects.filter(location__name="National").values('sit_rep__day_of_year', 'sit_rep__date', 'location__name',
        'location__slug', 'total_deaths_probable', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed', 'cases_cum',
        'cases_new_total', 'cases_new_suspected', 'cases_new_probable', 'cases_new_confirmed', 'total_deaths_suspected', 'total_deaths_confirmed',
        'total_deaths_all', 'deaths', 'new_deaths_probable', 'new_deaths_suspected', 'new_deaths_confirmed', 'hc_workers', 'hcw_cases_new',
        'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum', 'CFR')

        for i in location_vals:
            if i['sit_rep__day_of_year'] == latest_date.day_of_year:
                i.setdefault('new_weekly_deaths', nat.new_weekly_deaths)
                i.setdefault('pct_change_death', nat.death_pct_change)
                i.setdefault('new_weekly_cases', nat.new_weekly_cases)
                i.setdefault('pct_change_cases', nat.cases_pct_change)
                i.setdefault('new_weekly_deaths_hcw', nat.new_weekly_deaths_hcw)
                i.setdefault('pct_change_death_hcw', nat.death_pct_change_hcw)
                i.setdefault('new_weekly_cases_hcw', nat.new_weekly_cases_hcw)
                i.setdefault('pct_change_cases_hcw', nat.cases_pct_change_hcw)
            list.append(i)

        for i in location_vals:
            if i['sit_rep__day_of_year'] == latest_date.day_of_year:
                i.setdefault('new_weekly_deaths', nat.new_weekly_deaths)
                i.setdefault('pct_change_death', nat.death_pct_change)
                i.setdefault('new_weekly_cases', nat.new_weekly_cases)
                i.setdefault('pct_change_cases', nat.cases_pct_change)
                i.setdefault('new_weekly_deaths_hcw', nat.new_weekly_deaths_hcw)
                i.setdefault('pct_change_death_hcw', nat.death_pct_change_hcw)
                i.setdefault('new_weekly_cases_hcw', nat.new_weekly_cases_hcw)
                i.setdefault('pct_change_cases_hcw', nat.cases_pct_change_hcw)
            for n in nums:
                if i['sit_rep__day_of_year'] == n:
                    filtered_list.append(i)


        e_json=open('latest_data/daily_main.json','w')
        jsonified = json.dumps(list)
        print>>e_json, jsonified
        e_json.close()

        eb_json=open('latest_data/weekly_main.json','w')
        jsonified = json.dumps(filtered_list)
        print>>eb_json, jsonified
        eb_json.close()
