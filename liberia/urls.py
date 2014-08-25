from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from liberia import views

urlpatterns = patterns(
    'liberia.views',
    url(
        r'^$',
        views.TemplateView.as_view(template_name='home/index.html'),
        name='index'
    ),
    )
