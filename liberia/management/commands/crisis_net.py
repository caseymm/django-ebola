#will need to download from csv from site (I think) becuase it looks like the api is maxing out on requests

#pull out all necessary items
    #for locations, save coords, and other info
    #when run geocoder, assign bool so we can just grab the entries that are coded
    #allow for an export json option for this so that maps can just grab from the url like the campaign stuff when I get it up
import json
import re
from liberia.models import DateStats, SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads CrisisNet api data for cataloging and geocoding.'

    def handle(self, *args, **options):
        fp = open("example_data.json", "r")
        s = fp.read()
        j = json.loads(s)
        data = j['data']

        for item in data[:2]:
            #gets dict for each item
            # print item
            for attr in item:
                #gets attributes in the item specific dictionary
                # print attr, item[attr]
                # if '[' in item[attr]:
                #     print item[attr]
                val_list = re.search(r'\[', str(item[attr]))
                val_dict = re.search(r'\{', str(item[attr]))

                if val_list:
                    print attr, item[attr]

                if val_dict:
                    print attr, item[attr]

                # try:
                #     if item[attr].find('['):
                #         print item[attr]
                # except:
                #     pass
