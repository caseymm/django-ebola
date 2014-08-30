from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from liberia import views

urlpatterns = patterns(
    'liberia.views',
    url(
        r'^$',
        views.LocationListView.as_view(template_name='home/index.html'),
        name='location_index'
    ),
    url(
        r'^location/(?P<pk>\d+)/$',
        views.LocationDetailView.as_view(template_name='home/index_detail.html'),
        name='location_detail'
    ),
    )
