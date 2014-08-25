from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
from django.conf import settings
from liberia import views
# from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^', include('liberia.urls')),

    # Examples:
    # url(r'^$', 'ebola_project.views.home', name='home'),
    # url(r'^ebola_project/', include('ebola_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', views.TemplateView.as_view(), template_name='index'),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
