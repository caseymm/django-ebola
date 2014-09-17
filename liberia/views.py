import json
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_text
from django.http import Http404, HttpResponse
from liberia.models import SitRep, Location, LocationSitRep, Document
from liberia.forms import DocumentForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
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
        context['locations'] = Location.objects.all()
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
        elif 'daily_json' in format:
            return HttpResponse(
                json.dumps(context['list'])
            )

        return super(LocationDetailView, self).render_to_response(context, **kwargs)

class DataResourcesTemplateView(generic.TemplateView):
    template = 'templates/home/data_resources.html'

    def get_context_data(self, **kwargs):
        context = super(DataResourcesTemplateView, self).get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['latest_qs'] = SitRep.objects.latest('formatted_date')
        context['us_date'] = us_date
        new_cds = {}
        d_dict = {}
        c_dict = {}
        for obj in LocationSitRep.objects.filter(sit_rep=context['latest_qs']).exclude(location=national).order_by('location').values('total_deaths_suspected', 'total_deaths_probable', 'total_deaths_confirmed', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed'):
            d_dict.setdefault('total_deaths_suspected', []).append(obj['total_deaths_suspected'])
            d_dict.setdefault('total_deaths_probable', []).append(obj['total_deaths_probable'])
            d_dict.setdefault('total_deaths_confirmed', []).append(obj['total_deaths_confirmed'])
            new_cds.setdefault("deaths", d_dict)
            c_dict.setdefault('cases_cum_suspected', []).append(obj['cases_cum_suspected'])
            c_dict.setdefault('cases_cum_probable', []).append(obj['cases_cum_probable'])
            c_dict.setdefault('cases_cum_confirmed', []).append(obj['cases_cum_confirmed'])
            new_cds.setdefault("cases", c_dict)

        context['county_json'] = json.dumps(new_cds)

        latest_sr = SitRep.objects.latest('formatted_date')
        context['us_date'] = us_date
        latest = datetime.strftime(latest_sr.formatted_date, "%j")

        #No nat
        format_nn = {}
        no_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').exclude(location=national):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            no_nat_list.append(i)
        format_nn.setdefault("aaData", no_nat_list)

        rem_quote_nn = json.dumps(format_nn)
        context['jsonified_nn'] = rem_quote_nn.replace('"[', '[').replace(']"', ']')

        #Inc nat
        format_incn = {}
        inc_nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum'):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            inc_nat_list.append(i)
        format_incn.setdefault("aaData", inc_nat_list)

        rem_quote_incn = json.dumps(format_incn)
        context['jsonified_incn'] = rem_quote_incn.replace('"[', '[').replace(']"', ']')

        #Only nat
        format_n = {}
        nat_list = []
        for i in latest_sr.locationsitrep_set.values('location__name', 'cases_cum', 'total_deaths_all', 'hcw_cases_cum', 'hcw_deaths_cum').filter(location=national):
            loc = Location.objects.get(name=i['location__name'])
            i.setdefault('new_weekly_deaths', loc.weekly_deaths)
            i.setdefault('new_weekly_cases', loc.weekly_cases)
            nat_list.append(i)
        format_n.setdefault("aaData", nat_list)

        rem_quote_n = json.dumps(format_n)
        context['jsonified_n'] = rem_quote_n.replace('"[', '[').replace(']"', ']')

        return context

    def render_to_response(self, context, **kwargs):
        format = self.request.GET.get('format', '')
        if 'hc_json' in format:
            return HttpResponse(
                context['county_json']
            )
        elif 'table_sparkline_ex_natl' in format:
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

        return super(DataResourcesTemplateView, self).render_to_response(context, **kwargs)


class DocumentLoadFormView(generic.FormView):
    template = 'templates/home/upload_sit_rep.html'
    form_class = DocumentForm
    success_url = '../success/'

    def get_context_data(self, **kwargs):
        context = super(DocumentLoadFormView, self).get_context_data(**kwargs)
        context['locations'] = Location.objects.all()

        return context

    def form_valid(self, form):
        form = Document(docfile = self.request.FILES['docfile'], sit_rep_date = self.request.POST['sit_rep_date'], month_format = self.request.POST['month_format'])
        form.save()

        return super(DocumentLoadFormView, self).form_valid(form)
