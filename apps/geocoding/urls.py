from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('geocoding.views',
    url(r'^edit/$', 'edit_map', (), 'edit_map'),
)
