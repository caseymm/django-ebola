import json
from django.db.models import Avg, Max, Min, Sum, Count
from liberia.models import SitRep, Location, LocationSitRep, WeekOfYear
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Get totals for new weekly deaths and new weekly cases and save to WeekOfYear obj.'

    def handle(self, *args, **options):
        # for week in WeekOfYear.objects.all():
        #     for sr in week.sitrep_set.all():
        #         print sr
        for group in LocationSitRep.objects.values('location__name', 'sit_rep__week_of_year__week'
        ).annotate(max_deaths=Max("total_deaths_all")).order_by('location__name'):
            print group
