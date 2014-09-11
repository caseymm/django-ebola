import csv
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter date information into db'

    def handle(self, *args, **options):
        with open('data/sr_backup_no_str.csv', 'rU') as csvfile:
            csvfile.readline()
            fp = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in fp:
                location = row[0]
                date_str = row[1]
                print location, date_str

                strp_time = time.strptime(date_str, "%d-%b-%y")
                date = datetime.fromtimestamp(time.mktime(strp_time))
                original_date = str(date)[:10]

                current_sit_rep, created = SitRep.objects.get_or_create(date=original_date, formatted_date=date)

                current_loc, created = Location.objects.get_or_create(name=location)

                new_loc_sr, created = LocationSitRep.objects.get_or_create(location=current_loc, sit_rep=current_sit_rep)

                new_loc_sr.date = original_date
                new_loc_sr.formatted_date = date
                if len(row[16]) > 0:
                    new_loc_sr.cases_new_suspected = row[16]
                else:
                    new_loc_sr.cases_new_suspected = 0
                if len(row[14]) > 0:
                    new_loc_sr.cases_new_probable = row[14]
                else:
                    new_loc_sr.cases_new_probable = 0
                if len(row[12]) > 0:
                    new_loc_sr.cases_new_confirmed = row[12]
                else:
                    new_loc_sr.cases_new_confirmed = 0
                if len(row[8]) > 0:
                    new_loc_sr.cases_cum_suspected = row[8]
                else:
                    new_loc_sr.cases_cum_suspected = 0
                if len(row[6]) > 0:
                    new_loc_sr.cases_cum_probable = row[6]
                else:
                    new_loc_sr.cases_cum_probable = 0
                if len(row[4]) > 0:
                    new_loc_sr.cases_cum_confirmed = row[4]
                else:
                    new_loc_sr.cases_cum_confirmed = 0
                if len(row[2]) > 0:
                    new_loc_sr.cases_cum = row[2]
                else:
                    new_loc_sr.cases_cum = 0
                if len(row[11]) > 0:
                    new_loc_sr.deaths = row[11]
                else:
                    new_loc_sr.deaths = 0
                if len(row[5]) > 0:
                    new_loc_sr.total_deaths_confirmed = row[5]
                else:
                    new_loc_sr.total_deaths_confirmed = 0
                if len(row[7]) > 0:
                    new_loc_sr.total_deaths_probable = row[7]
                else:
                    new_loc_sr.total_deaths_probable = 0
                if len(row[9]) > 0:
                    new_loc_sr.total_deaths_suspected = row[9]
                else:
                    new_loc_sr.total_deaths_suspected = 0
                if len(row[3]) > 0:
                    new_loc_sr.total_deaths_all = row[3]
                else:
                    new_loc_sr.total_deaths_all = 0
                if len(row[18]) > 0:
                    new_loc_sr.hcw_cases_cum = row[18]
                else:
                    new_loc_sr.hcw_cases_cum = 0
                if len(row[19]) > 0:
                    new_loc_sr.hcw_deaths_cum = row[19]
                    # new_loc_sr.admission_new = row[1]
                    # new_loc_sr.in_treatment = row[2]
                    # new_loc_sr.total_discharges = row[3]
                    # new_loc_sr.admission_cum = row[4]
                    # new_loc_sr.CFR = row[]
                    # new_loc_sr.hcw_cases_new = row[]
                    # new_loc_sr.hcw_deaths_new = row[]
                else:
                    new_loc_sr.hcw_deaths_cum = 0
                if len(row[17]) > 0:
                    new_loc_sr.new_deaths_suspected = row[17]
                else:
                    new_loc_sr.new_deaths_suspected = 0
                if len(row[15]) > 0:
                    new_loc_sr.new_deaths_probable = row[15]
                else:
                    new_loc_sr.new_deaths_probable = 0
                if len(row[13]) > 0:
                    new_loc_sr.new_deaths_confirmed = row[13]
                else:
                    new_loc_sr.new_deaths_confirmed = 0
                if len(row[10]) > 0:
                    new_loc_sr.cases_new_total = row[10]
                else:
                    new_loc_sr.cases_new_total = 0
                new_loc_sr.save()
