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

        # attr_list = []
        #gets dict for each item
        for item in data:
            #gets attributes in the item specific dictionary
            # for attr in item:
                # attr_list.append(str(attr))
                # entry.attr = item[attr]
                # print attr, entry.attr
            print item['entities']
            print item['id']
            print

                # remoteID
                # tags --m (name)
                # author --m (remoteID, image, name)
                # publishedAt
                # summary
                # content
                # source
                # lifespan
                # updatedAt
                # geo --m (coords: list, address components, many(pull out and put into list?))
                # id
                # createdAt


                # try:
                #     attr_val = str(item[attr])
                #     # #checks to see if the attr value is a dict or an item
                #     val_list = re.search(r'\[', attr_val)
                #     val_dict = re.search(r'\{', attr_val)
                #
                #     if val_list:
                #         print attr, item[attr]
                #         item_dict = item[attr]
                #         print
                #         for desc in item_dict:
                #             print desc, item_dict[desc]
                #
                #     if val_dict:
                #         print attr, item[attr]
                #         item_dict = item[attr]
                #         print
                #         for desc in item_dict:
                #             print desc, item_dict[desc]
                # except:
                #     pass
