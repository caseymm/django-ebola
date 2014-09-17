from django.contrib import admin
from django import forms
from liberia.models import SitRep, Location, LocationSitRep, Tag, Author, CrisisNetEntry
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
import datetime
import time
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
# from liberia.forms import UploadFileForm

class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

class SitRepAdmin(admin.ModelAdmin):
    search_fields = ['date',]
    # list_filter = ()
    save_on_top = True
    form = UploadFileForm
    # e_json=open('latest_data/export_main_weekly.json','w')
    def handle_uploaded_file(self, f):
        print 'got here'
        df = pd.io.excel.read_excel(f, 0, index_col=None, na_values=['NA'])
        print 'dd'
        print df
    #
    # def upload_file(self):
    #     form = UploadFileForm(POST, FILES)
    #     if form.is_valid():
    #     self.handle_uploaded_file(self.FILES['file'])
    #         return HttpResponseRedirect('/success/url/')

    def save(self, commit=True):
        self.handle_uploaded_file(self.form.FILES['file'])

        # else:
        #     form = UploadFileForm()
        # return render_to_response('upload.html', {'form': form})

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

# class TagAdminForm(forms.ModelForm):
#     crisisnetentry_set = forms.ModelMultipleChoiceField(queryset=CrisisNetEntry.objects.all(), required=False, widget=FilteredSelectMultiple(verbose_name=_('Obituaries'), is_stacked=False))
#     class Meta:
#         model = Tag
#
#     def __init__(self, *args, **kwargs):
#         super(TagAdminForm, self).__init__(*args, **kwargs)
#
#         if self.instance and self.instance.pk:
#             self.fields['crisisnetentry_set'].initial = self.instance.crisisnetentry_set.all()
#
#     def save(self, commit=True):
#         tag = super(TagAdminForm, self).save(commit=False)
#         if commit:
#             tag.save()
#         if tag.pk:
#             tag.crisinetentries = self.cleaned_data['crisisnetentry_set']
#             self.save_m2m()
#
#         return tag

# class TagAdmin(admin.ModelAdmin):
#     search_fields = ['name', ]
#     # list_filter = ()
#     save_on_top = True
#     form = TagAdminForm
# admin.site.register(Tag, TagAdmin)
#
# class AuthorAdmin(admin.ModelAdmin):
#     search_fields = ['name', ]
#     # list_filter = ()
#     save_on_top = True
# admin.site.register(Author, AuthorAdmin)
#
# class CrisisNetEntryAdminForm(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=FilteredSelectMultiple(verbose_name=_('Tags'), is_stacked=False))
#     class Meta:
#         model = CrisisNetEntry
#
#     def __init__(self, *args, **kwargs):
#         super(CrisisNetEntryAdminForm, self).__init__(*args, **kwargs)
#
#         if self.instance and self.instance.pk:
#             self.fields['tags'].initial = self.instance.tags.all()
#
#     def save(self, commit=True):
#         crisisnetentry = super(CrisisNetEntryAdminForm, self).save(commit=False)
#         if commit:
#             crisisnetentry.save()
#         if CrisisNetEntry.pk:
#             crisisnetentry.crisisnetentries = self.cleaned_data['tags']
#             self.save_m2m()
#
#         return CrisisNetEntry
#
# class CrisisNetEntryAdmin(admin.ModelAdmin):
#     # search_fields = ['', ]
#     list_filter = ('is_geocoded', 'source')
#     list_display = ['createdAt', 'is_geocoded', 'author', 'source']
#     save_on_top = True
#     form = CrisisNetEntryAdminForm
# admin.site.register(CrisisNetEntry, CrisisNetEntryAdmin)
