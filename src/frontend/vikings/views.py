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
    checkins = api.__getDayCheckins()

    file = open('../showDayCheckins.html')
    template = Template(file.read())
    file.close()
    html = template.render(Context({'nrCheckins': len(checkins),
                                    'checkins': checkins}))
    return HttpResponse(html)


# Note: arguments passed as string
def whatsNext(request, userToken, spotId): 
    spotId = int(spotId)
    json = api.getPopularNextSpotsJSON(spotId, 10, userToken)
    response = HttpResponse(json, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



def whatsNextByCount(request, userToken, spotId): 
    spotId = int(spotId)
    json = api.getPopularNextSpotsByCountJSON(spotId, 10, userToken)
    response = HttpResponse(json, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



def whatsNextBySpotAge(request, userToken, spotId): 
    spotId = int(spotId)
    json = api.getPopularNextSpotsBySpotAgeJSON(spotId, 10, userToken)
    response = HttpResponse(json, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



def whatsNextByTimeSpent(request, userToken, spotId): 
    spotId = int(spotId)
    json = api.getPopularNextSpotsByTimeSpentJSON(spotId, 10, userToken)
    response = HttpResponse(json, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
