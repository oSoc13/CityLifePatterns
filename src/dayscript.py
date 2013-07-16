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
    output = "{0:50} {1:10} {2:10}"
    print output.format("\nSPOT NAME", "         ID", "      COUNT\n")
    for (spotId,count) in topNextSpots:
        spot = api.getSpotById(spotId)
        if not spot == None:
            print output.format(spot.name, spot.id, count)
        else:
            print output.format("(private)", spotId, count)

## Main ###########################################################

# Input
spotId = 0
nrSpots = 10
if len(sys.argv) > 1:
    spotId = int(sys.argv[1])
else:
    spotId = 180
###

spot = api.getSpotById(spotId)
if spot == None:
    print "\nSpot with ID %d doesn't exist." % spotId
else:
    print "\nGetting next probable spots for spot: %s" % spot.name
    topNextSpots = api.getPopularNextSpots(spotId, nrSpots)
    nrSpotsFound = len(topNextSpots)

    if nrSpotsFound > 0:
        print "%d spots found." % nrSpotsFound
        printNextSpots(topNextSpots)
    else:
        print "\nNo popular next spots found."

print "\nTerminating..."
###################################################################
