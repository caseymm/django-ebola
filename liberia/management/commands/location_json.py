import json
import re
from liberia.models import DateStats, SitRep, Location, LocationSitRep
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
        #use cfr info in date_span field
        date_span = ''

        #Just do raw input for now
        print 'Please format date as yyyy-mm-dd'
        date = raw_input ("Enter SitRep date: ")
        num = raw_input ("Enter SitRep number: ")

        loc_dict = {}

        for entry in j:
            for i in entry:
                if i == 'Type':
                    get_date = entry[i].split("(",1)[-1].rsplit(")",1)[0]
                    if '2014' in get_date:
                        date_span += get_date
                else:
                    info = {}
                    info.setdefault(entry[i], entry['Type'])
                    set_type = {y:x for x,y in info.iteritems()}
                    # print i, entry[i], entry['Type']
                    loc_dict.setdefault(i, []).append(set_type)

        current_sit_rep, created = SitRep.objects.get_or_create(num=num, date=date, date_span=date_span)
        current_sit_rep.save()

        simple = {}
        for loc in loc_dict:
            agg = {}
            for md in loc_dict[loc]:
                for i in md:
                    agg.setdefault(i, md[i])
            simple.setdefault(loc, agg)
        # print simple

        for loc in simple:
            current_loc, created = Location.objects.get_or_create(name=loc)
            current_loc.save()
            
            total_probable_deaths = simple[loc].get('Total deaths in probable cases')
            cases_cum = simple[loc].get('Cumulative (confirmed, probable, suspected) cases')
            deaths = simple[loc].get('Deaths')
            CFR = simple[loc].get('Cumulative CFR (March 22 - Aug 12, 2014)')
            hc_workers = simple[loc].get('Health Care Workers')
            total_deaths_suspected = simple[loc].get('Total deaths in suspected cases')
            total_deaths_confirmed = simple[loc].get('Total deaths in confirmed cases')
            cases_cum_confirmed = simple[loc].get('Total cases (confirmed)')
            hcw_cases_cum = simple[loc].get('Cumulative  cases among HCW')
            hcw_deaths_cum = simple[loc].get('Cumulative  deaths among HCW')
            cases_cum_suspected = simple[loc].get('Total Cases (Suspected)')
            total_deaths_all = simple[loc].get('Total deaths in confirmed, probable, suspected cases')
            cases_cum_probable = simple[loc].get('Total Cases (Probable)')

            new_loc_sr = LocationSitRep(sit_rep=current_sit_rep, location=current_loc, num=num, date_span=date_span, date=date, total_probable_deaths=total_probable_deaths, cases_cum=cases_cum, deaths=deaths, CFR=CFR, hc_workers=hc_workers, total_deaths_suspected=total_deaths_suspected, total_deaths_confirmed=total_deaths_confirmed, cases_cum_confirmed=cases_cum_confirmed, hcw_cases_cum=hcw_cases_cum, hcw_deaths_cum=hcw_deaths_cum, cases_cum_suspected=cases_cum_suspected, total_deaths_all=total_deaths_all, cases_cum_probable=cases_cum_probable)
            new_loc_sr.save()
