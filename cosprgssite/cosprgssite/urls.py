__author__ = "Jeremy Nelson"

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^committees/(?P<committee>.*)/(?P<year>\d+)/(?P<month>\d+)$',
        'cosprgssite.views.report',
        name='report'),
    url(r'^committees/(?P<committee>.*)$',
        'cosprgssite.views.committee',
        name='committee'),
    url(r'^meetings/(?P<meeting>.*)/(?P<year>\d+)/(?P<month>\d+)$',
        'cosprgssite.views.minute',
        name='minute'),
    url(r'^history/(?P<topic>.*)$',
        'cosprgssite.views.history',
        name='history'),
    url(r'^login$',
        'cosprgssite.views.login_view'),
    url(r'^logout$',
        'cosprgssite.views.logout_view'),
    url(r'^meetings/(?P<meeting>.*)$',
        'cosprgssite.views.meeting',
        name='meeting'),
    url(r"^[f|F]riends/", include("friends.urls")),
    url(r'^testimonies/(?P<testimony>.*)$',
        'cosprgssite.views.testimony',
        name='testimony'),
    url(r'^$', 'cosprgssite.views.home', name='home'),
    
    # url(r'^cosprgssite/', include('cosprgssite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
