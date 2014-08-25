import json
from liberia.models import DateStats
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter location information into db from SitRep pdf data that has been parsed into json.'

    def handle(self, *args, **options):
        fp = open("overview_0812.json", "r")
        s = fp.read()
        j = json.loads(s)

        loc_dict = {}

        for entry in j:

            for i in entry:
                if i != 'Type':
                    info = {}
                    info.setdefault(entry[i], entry['Type'])
                    set_type = {y:x for x,y in info.iteritems()}
                    # print i, entry[i], entry['Type']
                    loc_dict.setdefault(i, []).append(set_type)
        simple = {}
        for loc in loc_dict:
            # print loc, loc_dict[loc]
            agg = {}
            for md in loc_dict[loc]:
                for i in md:
                    agg.setdefault(i, md[i])
            simple.setdefault(loc, agg)
        print simple
