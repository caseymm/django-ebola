from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Add doy to SitRep'

    def handle(self, *args, **options):
        for sr in SitRep.objects.all():
            d = datetime.strptime(sr.date, '%Y-%m-%d')
            sr.day_of_year = datetime.strftime(d, "%j")
            sr.save()
