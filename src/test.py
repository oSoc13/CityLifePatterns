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


baseDir = os.path.dirname(os.path.abspath(__file__))
api = WhatsNextApi(baseDir)

####################################
# Test Code   
####################################
print "Testing..."

spotId = 7
nrSpots = 10

topNextSpots = api.getTopNextSpots(spotId, nrSpots)

spot = api.getSpotById(spotId)
print "\nGetting next probable spots for spot: %s" % spot.name

print "\n%d spots found." % len(topNextSpots)
print "spot name (count)\n"
for (spotId,count) in topNextSpots:
    spot = api.getSpotById(spotId)
    if not spot == None:
        print "%s (%d)" % (spot.name, count)
    else:
        print "No access to this spot (id=%d) (%d)." % (spotId,count)


print "\nTerminating..."


