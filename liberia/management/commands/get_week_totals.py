import json
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Get week totals for cases and deaths'

    def handle(self, *args, **options):
        national = Location.objects.filter(name='National')

        today_total = LocationSitRep.objects.get(date='2014-08-27', location=national)
        week_ago_total = LocationSitRep.objects.get(date='2014-08-20', location=national)
        print today_total.total_deaths_all - week_ago_total.total_deaths_all
        print today_total.cases_cum - week_ago_total.cases_cum
