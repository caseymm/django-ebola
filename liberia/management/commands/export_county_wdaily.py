import json
import cPickle
from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Export necessary json for charts from db'

    def handle(self, *args, **options):
        exp_county=open('latest_data/export_county_wdaily.json','w')
        latest_date = SitRep.objects.latest('formatted_date')

        today = datetime.today().strftime("%j")
        latest = datetime.strftime(latest_date.formatted_date, "%j")
        nums = [int(latest)]
        num=int(latest)

        while (num - 7) > 0:
            nums.append(num-7)
            num=num-7

        locs_daily_dict = {}
        for i in Location.objects.all():
            daily_info = {}
            daily_deaths = []
            daily_cases = []

            for obj in LocationSitRep.objects.order_by('location'):
                if i == obj.location:
                    d = datetime.strptime(obj.date, '%Y-%m-%d')
                    doy = datetime.strftime(d, "%j")
                    if int(doy) in nums:
                        daily_deaths.append(obj.deaths)
                        daily_cases.append(obj.cases_new_total)

            daily_info.setdefault('daily_deaths', daily_deaths)
            daily_info.setdefault('daily_cases', daily_cases)

            locs_daily_dict.setdefault(i.name, daily_info)

        print>>exp_county, locs_daily_dict
        print>>exp_county

        national = Location.objects.filter(name='National')
        latest_sr = SitRep.objects.latest('formatted_date')

        print>>exp_county, 'Not including national'
        print>>exp_county
        no_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').exclude(location=national):
            daily_deaths = locs_daily_dict[i['location__name']].get('daily_deaths')
            daily_cases = locs_daily_dict[i['location__name']].get('daily_cases')
            i.setdefault('daily_deaths', daily_deaths)
            i.setdefault('daily_cases', daily_cases)
            no_nat_list.append(i)

        jsonified_nn = json.dumps(no_nat_list)
        print>>exp_county, jsonified_nn

        print>>exp_county
        print>>exp_county
        print>>exp_county, 'Including national'
        print>>exp_county
        inc_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum'):
            daily_deaths = locs_daily_dict[i['location__name']].get('daily_deaths')
            daily_cases = locs_daily_dict[i['location__name']].get('daily_cases')
            i.setdefault('daily_deaths', daily_deaths)
            i.setdefault('daily_cases', daily_cases)
            inc_nat_list.append(i)

        jsonified_incn = json.dumps(inc_nat_list)
        print>>exp_county, jsonified_incn

        print>>exp_county
        print>>exp_county
        print>>exp_county, 'just national'
        print>>exp_county
        nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').filter(location=national):
            daily_deaths = locs_daily_dict[i['location__name']].get('daily_deaths')
            daily_cases = locs_daily_dict[i['location__name']].get('daily_cases')
            i.setdefault('daily_deaths', daily_deaths)
            i.setdefault('daily_cases', daily_cases)
            nat_list.append(i)

        jsonified_n = json.dumps(nat_list)
        print>>exp_county, jsonified_n

        exp_county.close()
