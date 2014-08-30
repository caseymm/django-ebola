import json
from django.shortcuts import render
from django.views import generic
from django.utils.encoding import smart_text
from django.http import Http404, HttpResponse
from liberia.models import SitRep, Location, LocationSitRep

class DataPrepMixin(object):
    """
    Provides a method for preping a context object
    for serialization as JSON or CSV.
    """
    def prep_context_for_serialization(self, context):
        field_names = self.model._meta.get_all_field_names()
        values = self.get_queryset().values_list(*field_names)
        data_list = []
        for i in values:
            d = {field_names[index]:val for index, val in enumerate(i)}
            data_list.append(d)

        return (data_list, field_names)


class JSONResponseMixin():
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        data, fields = self.context
        return HttpResponse(
            json.dumps(data, default=smart_text),
            content_type='application/json',
            **response_kwargs
        )

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
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['location'] = self.object.locationsitrep_set.all()
        for ent in context['location']:
            context['date_str'] = ent.date
        context['list'] = []
        context['location_vals'] = self.object.locationsitrep_set.values('location__name', 'total_deaths_probable', 'cases_cum_suspected', 'cases_cum_probable', 'cases_cum_confirmed', 'cases_cum', 'cases_new_total', 'cases_new_suspected', 'cases_new_probable', 'cases_new_confirmed', 'total_deaths_suspected', 'total_deaths_confirmed', 'total_deaths_all', 'deaths', 'new_deaths_probable', 'new_deaths_suspected', 'new_deaths_confirmed', 'hc_workers', 'hcw_cases_new', 'hcw_cases_cum', 'hcw_deaths_new', 'hcw_deaths_cum', 'CFR')

        for i in context['location_vals']:
            i.setdefault('date_str', context['date_str'])
            context['list'].append(i)
        return context

    def render_to_response(self, context, **kwargs):
        # See if the user has requested a special format
        format = self.request.GET.get('format', '')
        if 'json' in format:
            return HttpResponse(
                json.dumps(context['list'])
            )

        # And if it's none of the above return something normal
        return super(LocationDetailView, self).render_to_response(context, **kwargs)
