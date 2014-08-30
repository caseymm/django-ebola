from django.shortcuts import render
from django.views import generic
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

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['location'] = self.object.locationsitrep_set.all()
        return context
