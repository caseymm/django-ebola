from django.core.management.base import BaseCommand
import time
from datetime import datetime

class Command(BaseCommand):
    help = 'Format date for dict get in sitrep excel data'

    def handle(self, *args, **options):
        def date_ending(de):
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
            print de
