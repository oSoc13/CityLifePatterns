from django.conf.urls.defaults import *

# View imports
from vikings.views import hello
from vikings.views import current_datetime

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^hello/$', hello),
    url(r'^time/$', current_datetime)

    # Example:
    # (r'^vikings/', include('vikings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
