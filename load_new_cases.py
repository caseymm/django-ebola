import csv
from liberia.models import DateStats
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter date information into db'

    def handle(self, *args, **options):
        with open('cases_new.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in fp:
                original_date = row[0]
                new_cases = row[1]
                new_suspected_cases = row[2]
                new_probable_cases = row[3]
                new_confirmed_cases = row[4]


                try:
                    strp_time = time.strptime(original_date, "%d-%b-%y")
                    date = datetime.fromtimestamp(time.mktime(strp_time))

                    this_date, created = DateStats.objects.get_or_create(date=date)
                    this_date.new_cases = new_cases
                    this_date.new_suspected_cases = new_suspected_cases
                    this_date.new_probable_cases = new_probable_cases
                    this_date.new_confirmed_cases = new_confirmed_cases
                    this_date.save()
                except:
                    pass
