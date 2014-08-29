import csv
from liberia.models import DateStats
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter date information into db'

    def handle(self, *args, **options):
        with open('contacts.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in fp:
                original_date = row[0]
                news_contacts = row[1]
                contacts_completed_observation = row[2]
                contacts_lost_followup = row[3]

                try:
                    strp_time = time.strptime(original_date, "%d-%b-%y")
                    date = datetime.fromtimestamp(time.mktime(strp_time))

                    this_date, created = DateStats.objects.get_or_create(date=date)
                    this_date.news_contacts = news_contacts
                    this_date.contacts_completed_observation = contacts_completed_observation
                    this_date.contacts_lost_followup = contacts_lost_followup
                    this_date.save()
                except:
                    pass
