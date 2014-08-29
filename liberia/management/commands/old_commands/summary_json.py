import json
import re
from liberia.models import Summary
from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Enter location information into db from SitRep pdf data that has been parsed into json.'

    def handle(self, *args, **options):
        fp = open("main.json", "r")
        s = fp.read()
        j = json.loads(s)

        #Just do raw input for now
        print 'Please format date as yyyy-mm-dd'
        date = raw_input ("Enter date: ")

        data_dict = {}

        for entry in j:
            for attr in entry:
                data_dict.setdefault(attr, entry[attr])

        new_summary = Summary(date=date)
        new_summary.total_deaths = data_dict['Total Deaths']
        new_summary.deaths_last_week = data_dict['Deaths Last Week']
        new_summary.deaths_this_week = data_dict['Deaths This Week']
        new_summary.total_cases = data_dict['Total Cases']
        new_summary.cases_last_week = data_dict['Cases Last Week']
        new_summary.cases_this_week = data_dict['Cases This Week']
        new_summary.total_contacts = data_dict['Total Contacts']
        new_summary.contacts_last_week = data_dict['Contacts Last Week']
        new_summary.contacts_this_week = data_dict['Contacts This Week']
        new_summary.total_hcw_deaths = data_dict['Total HealthCare Worker Deaths']
        new_summary.hcw_deaths_last_week = data_dict['HealthCare Worker Deaths Last Week']
        new_summary.hcw_deaths_this_week = data_dict['HealthCare Worker Deaths This Week']
        new_summary.total_hcw_cases = data_dict['Total HealthCare Worker Cases']
        new_summary.hcw_cases_last_week = data_dict['HealthCare Worker Cases Last Week']
        new_summary.hcw_cases_this_week = data_dict['HealthCare Worker Cases This Week']
        new_summary.total_labs_processed = data_dict['Total Labs Processed']
        new_summary.labs_processed_last_week = data_dict['Labs Processed Last Week']
        new_summary.labs_processed_this_week = data_dict['Labs Processed This Week']
        new_summary.total_labs_collected = data_dict['Total Labs Collected']
        new_summary.labs_collected_last_week = data_dict['Labs Collected Last Week']
        new_summary.labs_collected_this_week = data_dict['Labs Collected This Week']
        new_summary.total_fcr = data_dict['FCR']
        new_summary.fcr_last_week = data_dict['FCR Last Week']
        new_summary.fcr_this_week = data_dict['FCR This Week']
        new_summary.total_clinics = data_dict['Total Clinics']
        new_summary.save()
