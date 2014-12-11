from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',

    #The base view - returns index.html
    url(r'^$', 'locationstore.views.home', name='home'),

    # The two views that return Shoot objects
    url(r'^autocomplete/$', 'autocomplete.views.autocomplete', name='autocomplete'),
    url(r'^get_films/$', 'map.views.get_films', name='get_films'),

    # Link to the Django admin panel - useful during development
    url(r'^admin/', include(admin.site.urls)),

    # Needed to show the favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url='/staticfiles/img/favicon.ico')),
)
