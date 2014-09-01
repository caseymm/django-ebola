import json
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_text
from django.http import Http404, HttpResponse
from liberia.models import SitRep, Location, LocationSitRep

class LocationListView(generic.ListView):
    model = Location
    template = 'templates/home/index.html'
    context_object_name = 'locations'

    # def get_queryset(self):
    #     locations = Location.objects.all()
    #     return locations

class LocationDetailView(generic.DetailView):
    model = Location
    template = 'templates/home/index_detail.html'
    context_object_name = 'loc'

    def get_context_data(self, **kwargs):
        latest_date = SitRep.objects.latest('formatted_date')
        nums=[latest_date.day_of_year]
        num=latest_date.day_of_year
        while (num - 7) > 0:
            for sr in SitRep.objects.all():
                if sr.day_of_year == (num-7):
                    nums.append(sr.day_of_year)
            num=num-7

        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['location'] = self.object.locationsitrep_set.all()
        for ent in context['location']:
            context['date_str'] = ent.date
        context['list'] = []
        context['filtered_list'] = []
        context['location_vals'] = self.object.locationsitrep_set.values('sit_rep__day_of_year', 'sit_rep__date', 'location__name', 'location__slug', 'total_deaths_probable', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed', 'cases_cum', 'cases_new_total', 'cases_new_suspected', 'cases_new_probable', 'cases_new_confirmed', 'total_deaths_suspected', 'total_deaths_confirmed', 'total_deaths_all', 'deaths', 'new_deaths_probable', 'new_deaths_suspected', 'new_deaths_confirmed', 'hc_workers', 'hcw_cases_new', 'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum', 'CFR')

        for i in context['location_vals']:
            i.setdefault('pct_change_death', self.object.death_pct_change)
            i.setdefault('pct_change_cases', self.object.cases_pct_change)
            context['list'].append(i)

        for i in context['location_vals']:
            for n in nums:
                if i['sit_rep__day_of_year'] == n:
                    context['filtered_list'].append(i)

        return context

    #I should really be using a mixin for this
    def render_to_response(self, context, **kwargs):
        format = self.request.GET.get('format', '')
        if 'weekly_json' in format:
            return HttpResponse(
                json.dumps(context['filtered_list'])
            )
        elif 'json' in format:
            return HttpResponse(
                json.dumps(context['list'])
            )

        return super(LocationDetailView, self).render_to_response(context, **kwargs)
#
# class PctChangeListView(generic.ListView):
#     template = 'templates/home/pct_change.html'
#     model = Location
#     context_object_name = 'locations'
#
#     # def get_queryset(self):
#     #     locations = Location.objects.all()
#     #     return locations
#
#     def get_context_data(self, **kwargs):
#         context = super(PctChangeTemplateView, self).get_context_data(**kwargs)
#         context[''] = .objects.get()
#         return context
