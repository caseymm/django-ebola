import json
from django.db.models import Avg, Max, Min, Sum, Count
from liberia.models import SitRep, Location, LocationSitRep, WeekOfYear
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Get totals for new weekly deaths and new weekly cases and save to WeekOfYear obj.'

    def handle(self, *args, **options):

        loc_dict = {}
        for loc in Location.objects.all():
            both = {}
            deaths_array = []
            cases_array = []

            lsrs = LocationSitRep.objects.values('location__name', 'sit_rep__week_of_year__week'
            ).annotate(max_deaths=Max("total_deaths_all"), max_cases=Max("cases_cum")).order_by('location__name')

            for entry in lsrs:
                if loc.name == entry['location__name']:
                    # if entry['sit_rep__week_of_year__week']+1:
                    deaths_array.append(entry['max_deaths'])
                    cases_array.append(entry['max_cases'])

            d_sub = []
            c_sub = []

            for d in range(len(deaths_array)):
                try:
                    # if deaths_array[d+1]:
                    d_sub.append(deaths_array[d+1] - deaths_array[d])
                except:
                    pass

            for c in range(len(cases_array)):
                try:
                    c_sub.append(cases_array[c+1] - cases_array[c])
                except:
                    pass

            loc.weekly_deaths = d_sub
            loc.weekly_cases = c_sub
            loc.save()

            both.setdefault('weekly_deaths', d_sub)
            both.setdefault('weekly_cases', c_sub)
            loc_dict.setdefault(loc.name, both)
