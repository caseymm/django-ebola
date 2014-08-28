#!/usr/bin/python
# -*- coding: utf:8 -*-
#will need to download from csv from site (I think) becuase it looks like the api is maxing out on requests

#allow for an export json option for this so that maps can just grab from the url like the campaign stuff when I get it up
import csv
import re
from liberia.models import CrisisNetEntry, Author, Tag
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads CrisisNet api data for cataloging and geocoding.'

    def handle(self, *args, **options):
        with open('crisisnet.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in fp:
                remoteID = row[0]
                new_item, created = CrisisNetEntry.objects.get_or_create(remoteID=remoteID)
                new_item.publishedAt = row[5]
                new_item.summary = row[10]
                new_item.content = row[1]
                new_item.source = row[2]
                new_item.lifespan = row[11]
                new_item.updatedAt = row[7]
                new_item.createdAt = row[6]
                new_item.longitude = row[19]
                new_item.latitude = row[20]

                new_item.address = row[16]+' '+row[17]+' '+row[15]+' '+row[14]+' '+row[13]

                if len(new_item.longitude) > 0:
                    new_item.is_geocoded = True

                tags=row[18].split('|')
                for tag in tags:
                    new_tag, created = Tag.objects.get_or_create(name = tag)
                    new_item.tags.add(new_tag)

                new_item.save()
