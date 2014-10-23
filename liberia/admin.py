from django.contrib import admin
# from django import forms
from liberia.models import SitRep, Location, LocationSitRep, Tag, Author, CrisisNetEntry, Document, Uploader
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
import datetime
import time

class SitRepAdmin(admin.ModelAdmin):
    search_fields = ['date',]
    list_display = ['date', 'is_copy']
    # list_filter = ()
    save_on_top = True

admin.site.register(SitRep, SitRepAdmin)
#
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    # list_filter = ()
    save_on_top = True
admin.site.register(Location, LocationAdmin)

class LocationSitRepAdmin(admin.ModelAdmin):
    search_fields = ['location', 'num']
    exclude = ('date_span','hc_workers','date')
    list_display = ['location', 'formatted_date']
    # list_filter = ()
    save_on_top = True
admin.site.register(LocationSitRep, LocationSitRepAdmin)

class UploaderAdmin(admin.ModelAdmin):
    save_on_top = True
admin.site.register(Uploader, UploaderAdmin)
