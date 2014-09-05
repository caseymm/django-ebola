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
        r'^location/(?P<slug>[-\w\d]+)/$',
        views.LocationDetailView.as_view(template_name='home/index_detail.html'),
        name='location_detail'
    ),
    url(
        r'^highcharts/$',
        views.HighchartsTemplateView.as_view(template_name='home/highcharts_data.html'),
        name='highcharts_data'
    ),
    url(
        r'^table/$',
        views.TableTemplateView.as_view(template_name='home/table_data.html'),
        name='table_data'
    ),
    )
