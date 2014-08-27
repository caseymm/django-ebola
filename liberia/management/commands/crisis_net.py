#!/usr/bin/python
# -*- coding: utf:8 -*-
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

        #gets dict for each item
        for item in data:

            #gets attributes in the item specific dictionary
            for attr in item:
                item.attr = item[attr]
                print attr, item.attr

                # remoteID
                # license
                # language
                # tags
                # author
                # publishedAt
                # summary
                # content
                # source
                # lifespan
                # updatedAt
                # entities
                # geo
                # id
                # createdAt

                #checks to see if the attr value is a dict or an item
                # val_list = re.search(r'\[', str(item[attr]))
                # val_dict = re.search(r'\{', str(item[attr]))

                # if val_list:
                #     print attr, item[attr]
                #
                # if val_dict:
                #     print attr, item[attr]

                # try:
                #     if item[attr].find('['):
                #         print item[attr]
                # except:
                #     pass
