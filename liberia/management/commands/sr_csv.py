import csv
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Create csv for each sitrep'

    def handle(self, *args, **options):
        for i in SitRep.objects.all().order_by('-date')[:5]:
            fields = []
            fields.append('location__name')
            all_counties = LocationSitRep.objects.filter(sit_rep=i)
            for a in all_counties[:1].values():
                for item in a:
                    fields.append(item)

            a_list = list(all_counties.values_list(*fields))

            with open('sr_export_all'+i.date+'.csv', 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',') #quoting=csv.QUOTE_MINIMAL
                writer.writerow(fields)
                writer.writerows(list(a_list))
