import json
from django.db.models import Avg, Max, Min, Sum, Count
from liberia.models import SitRep, Location, LocationSitRep, WeekOfYear
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Get totals for new weekly deaths and new weekly cases and save to WeekOfYear obj.'

    def handle(self, *args, **options):
        # for loc in Location.objects.all():
        #     print loc

        loc_dict = {}
        for loc in Location.objects.all():
            both = {}
            deaths_array = []
            cases_array = []
            for entry in LocationSitRep.objects.values('location__name', 'sit_rep__week_of_year__week'
            ).annotate(max_deaths=Max("total_deaths_all"), max_cases=Max("cases_cum")).order_by('location__name'):
                if loc.name == entry['location__name']:
                    deaths_array.append(entry['max_deaths'])
                    cases_array.append(entry['max_cases'])
                    both.setdefault('weekly_deaths', deaths_array)
                    both.setdefault('weekly_cases', cases_array)
                    loc_dict.setdefault(entry['location__name'], both)

        print loc_dict
