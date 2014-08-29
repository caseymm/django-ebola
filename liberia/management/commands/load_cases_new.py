import csv
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter date information into db'

    def handle(self, *args, **options):
        with open('data/cases.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')

            print 'Please format date as yyyy-mm-dd'
            original_date = raw_input ("Enter SitRep date: ")

            strp_time = time.strptime(original_date, "%Y-%m-%d")
            date = datetime.fromtimestamp(time.mktime(strp_time))

            current_sit_rep, created = SitRep.objects.get_or_create(date=original_date, formatted_date=date)

            for row in fp:
                location = row[0]

                current_loc, created = Location.objects.get_or_create(name=location)
                new_loc_sr, created = LocationSitRep.objects.get_or_create(location=current_loc, sit_rep=current_sit_rep)
                new_loc_sr.date = original_date
                new_loc_sr.formatted_date = date

                new_loc_sr.cases_new_suspected = row[1]
                new_loc_sr.cases_new_probable = row[2]
                new_loc_sr.cases_new_confirmed = row[3]
                new_loc_sr.cases_new_total = (int(new_loc_sr.cases_new_suspected)+int(new_loc_sr.cases_new_probable)+int(new_loc_sr.cases_new_confirmed))
                new_loc_sr.cases_cum_suspected = row[4]
                new_loc_sr.cases_cum_probable = row[5]
                new_loc_sr.cases_cum_confirmed = row[6]
                new_loc_sr.cases_cum = row[9]
                new_loc_sr.save()
