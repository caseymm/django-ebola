import json
import re
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
        #date needs to be the date of the sitrep, not of the cfr info
        # date = ''

        #Just do raw input for now
        print 'Please format date as yyyy-mm-dd'
        date_span = raw_input ("Enter SitRep number: ")
        num = raw_input ("Enter SitRep number: ")

        loc_dict = {}

        for entry in j:
            for i in entry:
                # if i == 'Type':
                #     get_date = entry[i].split("(",1)[-1].rsplit(")",1)[0]
                #     if '2014' in get_date:
                #         date += get_date
                if i != 'Type':
                    info = {}
                    info.setdefault(entry[i], entry['Type'])
                    set_type = {y:x for x,y in info.iteritems()}
                    # print i, entry[i], entry['Type']
                    loc_dict.setdefault(i, []).append(set_type)
        simple = {}
        for loc in loc_dict:
            agg = {}
            for md in loc_dict[loc]:
                for i in md:
                    agg.setdefault(i, md[i])
            simple.setdefault(loc, agg)
        # print simple

        for loc in simple:
            simple[loc].get('Total deaths in probable cases')
            simple[loc].get('Cumulative (confirmed, probable, suspected) cases')
            simple[loc].get('Deaths')
            simple[loc].get('Cumulative CFR (March 22 - Aug 12, 2014)')
            simple[loc].get('Health Care Workers')
            simple[loc].get('Total deaths in suspected cases')
            simple[loc].get('Total deaths in confirmed cases')
            simple[loc].get('Total cases (confirmed)')
            simple[loc].get('Cumulative  cases among HCW')
            simple[loc].get('Cumulative  deaths among HCW')
            simple[loc].get('Total Cases (Suspected)')
            simple[loc].get('Total deaths in confirmed, probable, suspected cases')
            simple[loc].get('Total Cases (Probable)')

            new_loc_sr = LocationSitRep(date_span=date)

            # Cumulative (confirmed, probable, suspected) cases
            # Deaths
            # Cumulative CFR (March 22 - Aug 12, 2014)
            # Health Care Workers
            # Total deaths in suspected cases
            # Total deaths in confirmed cases
            # Total cases (confirmed)
            # Cumulative  cases among HCW
            # Cumulative  deaths among HCW
            # Total Cases (Suspected)
            # Total deaths in confirmed, probable, suspected cases
            # Total Cases (Probable)
            # new_location, created = Location.objects.get_or_create(name=loc)
