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
        r'^sitreps/$',
        views.SitRepListView.as_view(template_name='home/sitreps_list.html'),
        name='sitreps_list'
    ),
    url(
        r'^sitreps/(?P<date>[-\w\d]+)/$',
        views.SitRepDetailView.as_view(template_name='home/sitreps_detail.html'),
        name='sitreps_detail'
    ),
    url(
        r'^data/$',
        views.DataResourcesTemplateView.as_view(template_name='home/data_resources.html'),
        name='data_resources'
    ),
    url(
        r'^upload/$',
        views.DocumentFormView.as_view(template_name='home/upload_sit_rep.html'),
        name='upload_xls'
    ),
    url(
        r'^success/$',
        views.DocumentFormView.as_view(template_name='home/success.html'),
        name='success'
    ),
    )
