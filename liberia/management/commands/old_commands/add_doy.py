from liberia.models import SitRep, Location, LocationSitRep, WeekOfYear
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Add doy to SitRep'

    def handle(self, *args, **options):
        for sr in SitRep.objects.all():
            d = datetime.strptime(sr.date, '%Y-%m-%d')
            # sr.day_of_year = datetime.strftime(d, "%j")
            week = datetime.strftime(d, "%U")
            year = datetime.strftime(d, "%Y")
            print week
            print year
            current_week, created = WeekOfYear.objects.get_or_create(week=week, year=year)
            sr.week_of_year = current_week
            sr.save()
