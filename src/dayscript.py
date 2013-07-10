#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# This is the day script that uses nextSpot data from the database to advise probable next spots.
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import WhatsNextApi
from WhatsNextApi import *
###################################

api = WhatsNextApi()

def printNextSpots(spots):
    for (spotId,count) in topNextSpots:
        spot = api.getSpotById(spotId)
        if not spot == None:
            print "%s (count=%d)" % (spot.name, count)
        else:
            print "No access to this spot (id=%d) (count=%d)." % (spotId,count)

## Main ###########################################################

# Input
spotId = 180
nrSpots = 10
###

spot = api.getSpotById(spotId)
if spot == None:
    print "\nSpot with ID %d doesn't exist." % spotId
else:
    print "\nGetting next probable spots for spot: %s" % spot.name
    topNextSpots = api.getPopularNextSpots(spotId, nrSpots)
    nrSpotsFound = len(topNextSpots)

    if nrSpotsFound > 0:
        print "\n%d spots found." % nrSpotsFound
        printNextSpots(topNextSpots)
    else:
        print "\nNo popular next spots found."

print "\nTerminating..."
###################################################################
