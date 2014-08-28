from liberia.models import CrisisNetEntry, Author, Tag
from django.core.management.base import BaseCommand
import time
from datetime import datetime
from geopy.geocoders import GoogleV3

class Command(BaseCommand):
    help = 'Try to geocode any entries that have locations but no coordinates.'

    def handle(self, *args, **options):
        #Obviously have some cleaning to do...
        blank_address = ['', '    ', '    General-conflict', 'General-conflict']
        for entry in CrisisNetEntry.objects.filter(is_geocoded=False).exclude(address__in=blank_address):
            print entry.address
            try:
                geolocator = GoogleV3()
                address, (latitude, longitude) = geolocator.geocode(entry.address)
                new_coords = str(latitude), str(longitude)
                print '-----------------'
                print address
                print new_coords
            except:
                pass
