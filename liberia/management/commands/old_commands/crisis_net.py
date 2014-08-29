#!/usr/bin/python
# -*- coding: utf:8 -*-
#will need to download from csv from site (I think) becuase it looks like the api is maxing out on requests

#allow for an export json option for this so that maps can just grab from the url like the campaign stuff when I get it up
import json
import re
from liberia.models import CrisisNetEntry, Author, Tag
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
            remoteID = item['id']

            new_item, created = CrisisNetEntry.objects.get_or_create(remoteID=remoteID)

            new_item.publishedAt = item['publishedAt']
            new_item.summary = item['summary']
            new_item.content = item['content']
            new_item.source = item['source']
            new_item.lifespan = item['lifespan']
            new_item.updatedAt = item['updatedAt']
            new_item.createdAt = item['createdAt']

            try:
                author = item['author'].get('name')
                new_author, created = Author.objects.get_or_create(name=author)
                new_item.author = new_author
                #can't remember if I need this...
                new_item.save()
            except:
                pass

            for attr in item['geo']:
                if attr == 'coords':
                    new_item.longitude = item['geo'][attr][0]
                    new_item.latitude = item['geo'][attr][1]
                    new_item.is_geocoded = True
                elif attr == 'addressComponents':
                    new_item.address = item['geo'][attr].get('formattedAddress')

            for tag in item['tags']:
                tag = tag.get('name')
                new_tag, created = Tag.objects.get_or_create(name = tag)
                new_item.tags.add(new_tag)

            new_item.save()

            # try:
            #     print item['geo'].get('addressComponents').get('formattedAddress')
            # except:
            #     pass
