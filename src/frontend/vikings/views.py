#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
###################################
import sys
sys.path.insert(0, '../../')    # Specify additional directory to load python modules from
from django.template import Template, Context
from django.http import HttpResponse
import datetime
import WhatsNextApi
from WhatsNextApi import *
###################################

api = WhatsNextApi()

def showDayCheckins(request):
    checkins = api.getDayCheckins()

    file = open('../showDayCheckins.html')
    template = Template(file.read())
    file.close()
    html = template.render(Context({'nrCheckins': len(checkins),
                                    'checkins': checkins}))
    return HttpResponse(html)
