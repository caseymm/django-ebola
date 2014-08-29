import csv
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):
        with open('deaths.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')

            print 'Please format date as yyyy-mm-dd'
            date = raw_input ("Enter SitRep date: ")

            current_sit_rep, created = SitRep.objects.get_or_create(date=date)

            for row in fp:
                location = row[0]

                current_loc, created = Location.objects.get_or_create(name=location)
                new_loc_sr, created = LocationSitRep.objects.get_or_create(location=current_loc, sit_rep=current_sit_rep)

                new_loc_sr.deaths = row[1]
                new_loc_sr.total_deaths_confirmed = row[2]
                new_loc_sr.total_deaths_probable = row[3]
                new_loc_sr.total_deaths_suspected = row[4]
                new_loc_sr.total_deaths_all = row[5]
                new_loc_sr.CFR = row[6]
                new_loc_sr.save()
