import csv
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
import json
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Load new sit rep into model objects'

    def handle(self, *args, **options):
        # input_file = raw_input('Input file: ')
        df = pd.io.excel.read_excel('data/sr_104.xls', 0, index_col=None, na_values=['NA'])
        # with open(input_file, 'rU') as csvfile:
        #     csvfile.readline()
        #     fp = csv.reader(csvfile, delimiter=',', quotechar='"')
        sliced = df[:34]
        flipped = sliced.T
        idx = flipped.set_index([3])
        flipback = idx.T
        get_index = flipback.columns[0]
        idx = flipback.set_index(get_index)
        print idx.to_dict()

            # print 'Please format date as yyyy-mm-dd'
            # date = raw_input ("Enter SitRep date: ")
            #
            # # current_sit_rep, created = SitRep.objects.get_or_create(date=date)
            #
            # for row in fp:
            #     location = row[0]
            #
            #     # current_loc, created = Location.objects.get_or_create(name=location)
            #     # new_loc_sr, created = LocationSitRep.objects.get_or_create(location=current_loc, sit_rep=current_sit_rep)
            #
            #     new_loc_sr.deaths = row[1]
            #     new_loc_sr.total_deaths_confirmed = row[2]
            #     new_loc_sr.total_deaths_probable = row[3]
            #     new_loc_sr.total_deaths_suspected = row[4]
            #     new_loc_sr.total_deaths_all = row[5]
            #     new_loc_sr.CFR = row[6]
            #     new_loc_sr.save()
