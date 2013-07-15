#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
###################################
import sys
sys.path.insert(0, '../../modules')    # Specify additional directory to load python modules from
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


# Note: arguments passed as string
def whatsNext(request, userToken, spotId): 
    spotId = int(spotId)
    api.useToken(userToken)
    json = api.getPopularNextSpotsJSON(spotId, 10)
    return HttpResponse(json, content_type="application/json")


def whatsNextByCount(request, userToken, spotId): 
    spotId = int(spotId)
    api.useToken(userToken)
    json = api.getPopularNextSpotsByCountJSON(spotId, 10)
    return HttpResponse(json, content_type="application/json")


def whatsNextBySpotAge(request, userToken, spotId): 
    spotId = int(spotId)
    api.useToken(userToken)
    json = api.getPopularNextSpotsBySpotAgeJSON(spotId, 10)
    return HttpResponse(json, content_type="application/json")


def whatsNextByTimeSpent(request, userToken, spotId): 
    spotId = int(spotId)
    api.useToken(userToken)
    json = api.getPopularNextSpotsByTimeSpentJSON(spotId, 10)
    return HttpResponse(json, content_type="application/json")
