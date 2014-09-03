from liberia.models import SitRep, Location, LocationSitRep
from django.core.management.base import BaseCommand
from shutil import make_archive
import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path

class Command(BaseCommand):
    help = 'Zip file of latest data for email'

    def handle(self, *args, **options):

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        SITE_ROOT = dirname(BASE_DIR)
        my_root = dirname(SITE_ROOT)

        data_dir = os.path.expanduser(os.path.join(my_root, 'latest_data'))
        make_archive('latest', 'zip', data_dir)
