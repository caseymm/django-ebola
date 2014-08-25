from django.contrib import admin
from liberia.models import DateStats

# Register your models here.
class DateStatsAdmin(admin.ModelAdmin):
    exclude = ['original_date',]
    search_fields = ['date', ]
    # list_filter = ()
    save_on_top = True
admin.site.register(DateStats, DateStatsAdmin)
