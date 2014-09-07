import csv
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
import time
from datetime import datetime
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load new sit rep into model objects'

    def handle(self, *args, **options):

        input_file = raw_input('Input file: ')
        # input_file = 'data/sitreps/sr_110.xls'
        print 'Please format date as yyyy-mm-dd'
        original_date = raw_input ("Enter SitRep date: ")
        short_month = raw_input ("Enter month as appears on spreadsheet (including any punctuation): ")

        strp_time = time.strptime(original_date, "%Y-%m-%d")
        date = datetime.fromtimestamp(time.mktime(strp_time))

        year = datetime.strftime(date, "%Y")
        date_ending = datetime.strftime(date, "%d")
        de = str(date_ending)
        #not sure how to do this...
        # call_command("sitrep_date_format", args=de)

        if de[-2] == '0':
            de = de[1:]

        st = '1'
        nd = '2'
        rd = '3'
        th = ['4', '5', '6', '7', '8', '9', '0']

        if len(de) == 1:
            if de == st:
                de += 'st'
            elif de == nd:
                de += 'nd'
            elif de == rd:
                de += 'rd'
            else:
                de += 'th'
        elif len(de) == 2:
            if de[-2] == '1':
                de += 'th'
            else:
                if de[-1] == st:
                    de += 'st'
                elif de[-1] == nd:
                    de += 'nd'
                elif de[-1] == rd:
                    de += 'rd'
                else:
                    de += 'th'

        current_sit_rep, created = SitRep.objects.get_or_create(date=original_date, formatted_date=date)

        df = pd.io.excel.read_excel(input_file, 0, index_col=None, na_values=['NA'])
        sliced = df[:34]
        flipped = sliced.T
        idx = flipped.set_index([3])
        flipback = idx.T
        get_index = flipback.columns[0]
        idx = flipback.set_index(get_index)
        loc_dict = idx.to_dict()
        for i in loc_dict:
            county = loc_dict[i]
            for i in county:
                try:
                    county[i] = int(county[i])
                except:
                    county[i] = 0

        for i in loc_dict:
            current_loc, created = Location.objects.get_or_create(name=i.strip())
            new_loc_sr, created = LocationSitRep.objects.get_or_create(location=current_loc, sit_rep=current_sit_rep)

            new_loc_sr.date = original_date
            new_loc_sr.formatted_date = date

            new_loc_sr.cases_new_probable = loc_dict[i].get("New Case/s (Probable)")
            new_loc_sr.total_deaths_suspected = loc_dict[i].get("Total death/s in suspected cases")
            #Need to fix this
            new_loc_sr.total_discharges = loc_dict[i].get("Total discharges on "+de+" "+short_month+" "+year+"")
            new_loc_sr.hcw_deaths_new = loc_dict[i].get("Newly Reported deaths in HCW on "+de+" "+short_month+" "+year+"")
            new_loc_sr.total_deaths_confirmed = loc_dict[i].get("Total death/s in confirmed cases")
            new_loc_sr.deaths = loc_dict[i].get("Newly reported deaths "+de+" "+short_month+" "+year+"")
            new_loc_sr.CFR = loc_dict[i].get("Case Fatality Rate (CFR) - Confirmed & Probable Cases")
            new_loc_sr.total_deaths_all = loc_dict[i].get("Total death/s in confirmed, probable, suspected cases")
            new_loc_sr.admission_cum = loc_dict[i].get("Cumulative admission/isolation ")
            new_loc_sr.cases_new_confirmed = loc_dict[i].get("New case/s (confirmed) ")
            new_loc_sr.cases_new_suspected = loc_dict[i].get("New Case/s (Suspected)")
            new_loc_sr.cases_cum = loc_dict[i].get("Cumulative (confirmed, probable, suspected) cases")
            new_loc_sr.cases_cum_probable = loc_dict[i].get("Total probable cases")
            new_loc_sr.in_treatment = loc_dict[i].get("Total no. currently in Treatment Units")
            new_loc_sr.hcw_cases_cum = loc_dict[i].get("Cumulative  cases among HCW ")
            new_loc_sr.cases_cum_confirmed = loc_dict[i].get("Total confirmed cases")
            new_loc_sr.admission_new = loc_dict[i].get("New Admission on "+short_month+" "+date_ending+" "+year+"")
            new_loc_sr.hcw_deaths_cum = loc_dict[i].get("Cumulative  deaths among HCW ")
            new_loc_sr.cases_cum_suspected = loc_dict[i].get("Total suspected cases")
            new_loc_sr.hcw_cases_new = loc_dict[i].get("Newly Reported Cases in HCW on "+de+" "+short_month+" "+year+"")
            new_loc_sr.total_deaths_probable = loc_dict[i].get("Total death/s in probable cases")
            new_loc_sr.cases_new_total = (int(new_loc_sr.cases_new_suspected)+int(new_loc_sr.cases_new_probable)+int(new_loc_sr.cases_new_confirmed))
            new_loc_sr.save()

        call_command("export_cases_deaths")
        call_command("export_hc_county")
        call_command("export_hcw")
        call_command("export_json")
        call_command("export_county_wdaily")
        # time.sleep(5)
        call_command("zip_latest")
        time.sleep(5)
        call_command("email")
