#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# Testing class
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import WhatsNextApi
from WhatsNextApi import *
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
###################################


api = WhatsNextApi()
vsApi = VikingSpotsApiWrapper()

####################################
# Test Code   
####################################
print "Testing..."


json = api.getPopularNextSpotsJSON(180,10)
print json


'''
for (spotId,count) in spotIds:
    spot = api.getSpotById(spotId)
    print json.dumps(spot.json)
    #print type(spot.json)
    #print spot.json
'''
    

print "\nTerminating..."


