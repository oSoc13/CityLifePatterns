from django.conf.urls.defaults import *

# View imports
from vikings.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    # \d+ : any digit,
    # ()  : make variable available in view

    #url(r'^api/checkins/day/$', showDayCheckins),

    # e.g. ../api/239zajze23/whatsnext/180/
    url(r'^api/(?P<userToken>[a-zA-Z\d+]*)/whatsnext/(?P<spotId>\d+)/$', whatsNext)         

    # Example:
    # (r'^vikings/', include('vikings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
