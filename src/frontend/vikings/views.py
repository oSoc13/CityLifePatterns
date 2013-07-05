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

# This is a view function.
# A view is just a Python function that takes an HttpRequest as 
# its first parameter and returns an instance of HttpResponse.
def hello(request):
    return HttpResponse("Hello World")

def current_datetime(request):
    now = datetime.datetime.now()
    fp = open('../templatetest.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

def showDayCheckins(request):
    checkins = api.getDayCheckins()
    nrCheckins = len(checkins)

    file = open('../showDayCheckins.html')
    template = Template(file.read())
    file.close()
    html = template.render(Context({'nrCheckins': nrCheckins,
                                    'checkins': checkins}))
    return HttpResponse(html)
