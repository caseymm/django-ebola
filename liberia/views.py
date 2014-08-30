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


class JSONResponseMixin(DataPrepMixin):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        data, fields = self.prep_context_for_serialization(context)
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

class LocationDetailView(JSONResponseMixin, generic.DetailView):
    model = Location
    template = 'templates/home/index_detail.html'
    context_object_name = 'loc'

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['location'] = self.object.locationsitrep_set.all()
        # context['loc_name'] = self.object.location
        return context

    def render_to_response(self, context, **kwargs):
        """
        Return a normal response, or CSV or JSON depending
        on a URL param from the user.
        """
        # See if the user has requested a special format
        format = self.request.GET.get('format', '')
        if 'json' in format:
            return self.render_to_json_response(context['location'].values())

        # And if it's none of the above return something normal
        return super(LocationDetailView, self).render_to_response(context, **kwargs)
