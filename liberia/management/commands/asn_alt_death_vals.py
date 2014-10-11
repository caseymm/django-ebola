from django.db.models import Avg, Max, Min, Sum, Count
from liberia.models import SitRep, Location, LocationSitRep, WeekOfYear
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Go and calculate the daily deaths if it isn\'t provided.'

    def handle(self, *args, **options):
        for loc in LocationSitRep.objects.all():
            def _get_previous_sr(loc):
                latest_qs = SitRep.objects.latest('formatted_date')
                previous_sr = SitRep.objects.get(day_of_year=(latest_qs.day_of_year-1))
                return previous_sr

            def _get_relevant_loc_sr(loc):
                previous_sr_doy = loc._get_previous_sr()
                prev_loc_sr = LocationSitRep.objects.get(location=loc.location, sit_rep=previous_sr_doy)
                return prev_loc_sr

            def _get_new_deaths_alt(loc):
                yesterday = loc._get_relevant_loc_sr()
                new_total_deaths = loc.total_deaths_all
                yesterday_total_deaths = yesterday.total_deaths_all
                loc.auto_new_deaths = new_total_deaths - yesterday_total_deaths
                return loc.auto_new_deaths

            loc.save()
