from django.contrib import admin
from liberia.models import DateStats, SitRep, Location, LocationSitRep, Tag, Author, CrisisNetEntry

# Register your models here.
class DateStatsAdmin(admin.ModelAdmin):
    exclude = ['original_date',]
    search_fields = ['date', ]
    # list_filter = ()
    save_on_top = True
admin.site.register(DateStats, DateStatsAdmin)

class SitRepAdmin(admin.ModelAdmin):
    search_fields = ['date', 'num']
    # list_filter = ()
    save_on_top = True
admin.site.register(SitRep, SitRepAdmin)

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    # list_filter = ()
    save_on_top = True
admin.site.register(Location, LocationAdmin)

class LocationSitRepAdmin(admin.ModelAdmin):
    search_fields = ['name', 'num']
    # list_filter = ()
    save_on_top = True
admin.site.register(LocationSitRep, LocationSitRepAdmin)

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    # list_filter = ()
    save_on_top = True
admin.site.register(Tag, TagAdmin)

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    # list_filter = ()
    save_on_top = True
admin.site.register(Author, AuthorAdmin)

class CrisisNetEntryAdmin(admin.ModelAdmin):
    # search_fields = ['', ]
    list_filter = ('is_geocoded', 'source')
    list_display = ['createdAt', 'is_geocoded', 'author', 'source']
    save_on_top = True
admin.site.register(CrisisNetEntry, CrisisNetEntryAdmin)
