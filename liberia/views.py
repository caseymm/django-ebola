import json
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_text
from django.http import Http404, HttpResponse
from liberia.models import SitRep, Location, LocationSitRep
import time
from datetime import datetime

national = Location.objects.filter(name='National')
latest_date = SitRep.objects.latest('formatted_date')
us_date = datetime.strftime(latest_date.formatted_date, "%x")

class NavLocationListView(generic.ListView):
    model = Location
    template = 'templates/nav_locs.html'
    context_object_name = 'locations'

class LocationListView(generic.ListView):
    model = Location
    template = 'templates/home/index.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['us_date'] = us_date
        return context

class LocationDetailView(generic.DetailView):
    model = Location
    template = 'templates/home/index_detail.html'
    context_object_name = 'loc'

    def get_context_data(self, **kwargs):
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
        context['location_vals'] = self.object.locationsitrep_set.values('sit_rep__day_of_year', 'sit_rep__date', 'location__name',
        'location__slug', 'total_deaths_probable', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed', 'cases_cum',
        'cases_new_total', 'cases_new_suspected', 'cases_new_probable', 'cases_new_confirmed', 'total_deaths_suspected', 'total_deaths_confirmed',
        'total_deaths_all', 'deaths', 'new_deaths_probable', 'new_deaths_suspected', 'new_deaths_confirmed', 'hc_workers', 'hcw_cases_new',
        'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum', 'CFR')

        for i in context['location_vals']:
            if i['sit_rep__day_of_year'] == latest_date.day_of_year:
                i.setdefault('new_weekly_deaths', self.object.new_weekly_deaths)
                i.setdefault('pct_change_death', self.object.death_pct_change)
                i.setdefault('new_weekly_cases', self.object.new_weekly_cases)
                i.setdefault('pct_change_cases', self.object.cases_pct_change)
                i.setdefault('new_weekly_deaths_hcw', self.object.new_weekly_deaths_hcw)
                i.setdefault('pct_change_death_hcw', self.object.death_pct_change_hcw)
                i.setdefault('new_weekly_cases_hcw', self.object.new_weekly_cases_hcw)
                i.setdefault('pct_change_cases_hcw', self.object.cases_pct_change_hcw)
            context['list'].append(i)

        for i in context['location_vals']:
            if i['sit_rep__day_of_year'] == latest_date.day_of_year:
                i.setdefault('new_weekly_deaths', self.object.new_weekly_deaths)
                i.setdefault('pct_change_death', self.object.death_pct_change)
                i.setdefault('new_weekly_cases', self.object.new_weekly_cases)
                i.setdefault('pct_change_cases', self.object.cases_pct_change)
                i.setdefault('new_weekly_deaths_hcw', self.object.new_weekly_deaths_hcw)
                i.setdefault('pct_change_death_hcw', self.object.death_pct_change_hcw)
                i.setdefault('new_weekly_cases_hcw', self.object.new_weekly_cases_hcw)
                i.setdefault('pct_change_cases_hcw', self.object.cases_pct_change_hcw)
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

class HighchartsTemplateView(generic.TemplateView):
    template = 'templates/home/highcharts_data.html'

    def get_context_data(self, **kwargs):
        context = super(HighchartsTemplateView, self).get_context_data(**kwargs)
        context['latest_qs'] = SitRep.objects.latest('formatted_date')
        context['us_date'] = us_date
        county_d = 'series:['
        new_deaths = {}
        for obj in LocationSitRep.objects.filter(sit_rep=context['latest_qs']).exclude(location=national).order_by('location'
        ).values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed'):
            for attr in obj:
                new_deaths.setdefault(attr, []).append(obj[attr])

        for i in new_deaths:
            county_d += '{name: '+i+','
            county_d += 'data: '+str(new_deaths[i])+'},'
        county_d += ']'

        context['county_d'] = county_d.replace(',]',']')

        county_c = 'series:['
        new_cases = {}
        for obj in LocationSitRep.objects.filter(sit_rep=context['latest_qs']).exclude(location=national).order_by('location'
        ).values('cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed'):
            for attr in obj:
                new_cases.setdefault(attr, []).append(obj[attr])

        for i in new_cases:
            county_c += '{name: '+i+','
            county_c += 'data: '+str(new_cases[i])+'},'
        county_c += ']'

        context['county_c'] = county_c.replace(',]',']')

        return context

    def render_to_response(self, context, **kwargs):
        format = self.request.GET.get('format', '')
        if 'deaths_hc_json' in format:
            return HttpResponse(
                context['county_d']
            )
        elif 'cases_hc_json' in format:
            return HttpResponse(
                context['county_c']
            )

        return super(HighchartsTemplateView, self).render_to_response(context, **kwargs)

class TableTemplateView(generic.TemplateView):
    template = 'templates/home/table_data.html'

    def get_context_data(self, **kwargs):
        context = super(TableTemplateView, self).get_context_data(**kwargs)
        latest_sr = SitRep.objects.latest('formatted_date')
        context['us_date'] = us_date
        latest = datetime.strftime(latest_sr.formatted_date, "%j")

        #No nat
        no_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').exclude(location=national):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            no_nat_list.append(i)

        context['jsonified_nn'] = json.dumps(no_nat_list)

        #Inc nat
        inc_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum'):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            inc_nat_list.append(i)

        context['jsonified_incn'] = json.dumps(inc_nat_list)

        #Only nat
        nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').filter(location=national):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            nat_list.append(i)

        context['jsonified_n'] = json.dumps(nat_list)

        return context

    def render_to_response(self, context, **kwargs):
        format = self.request.GET.get('format', '')
        if 'table_sparkline_ex_natl' in format:
            return HttpResponse(
                context['jsonified_nn']
            )
        elif 'table_sparkline_w_natl' in format:
            return HttpResponse(
                context['jsonified_incn']
            )
        elif 'table_sparkline_natl' in format:
            return HttpResponse(
                context['jsonified_n']
            )

        return super(TableTemplateView, self).render_to_response(context, **kwargs)
