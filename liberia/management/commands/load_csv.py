import csv
from liberia.models import DateStats
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter date information into db'

    def handle(self, *args, **options):
        with open('cases_cum.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in fp:
                original_date = row[0]
                total_cases = row[1]
                total_suspected_cases = row[2]
                total_probable_cases = row[3]
                total_confirmed_cases = row[4]

                try:
                    strp_time = time.strptime(original_date, "%d-%b-%y")
                    date = datetime.fromtimestamp(time.mktime(strp_time))

                    this_date = DateStats(date=date, original_date=original_date, total_cases=total_cases, total_suspected_cases=total_suspected_cases, total_probable_cases=total_probable_cases, total_confirmed_cases=total_confirmed_cases)
                    this_date.save()
                except:
                    pass
