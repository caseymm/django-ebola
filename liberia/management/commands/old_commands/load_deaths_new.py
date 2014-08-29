import csv
from liberia.models import DateStats
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter date information into db'

    def handle(self, *args, **options):
        with open('deaths_new.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in fp:
                original_date = row[0]
                today_deaths_all = row[1]
                today_deaths_suspected = row[2]
                today_deaths_probable = row[3]
                today_deaths_confirmed = row[4]

                try:
                    strp_time = time.strptime(original_date, "%d-%b-%y")
                    date = datetime.fromtimestamp(time.mktime(strp_time))

                    this_date, created = DateStats.objects.get_or_create(date=date)
                    this_date.today_deaths_all = today_deaths_all
                    this_date.today_deaths_suspected = today_deaths_suspected
                    this_date.today_deaths_probable = today_deaths_probable
                    this_date.today_deaths_confirmed = today_deaths_confirmed
                    this_date.save()
                except:
                    pass
