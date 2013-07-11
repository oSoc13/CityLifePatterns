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
from datetime import datetime
###################################


api = WhatsNextApi()

# For each checkin, get the next checkin by same user
# Checkins are already sorted by date (most recent last)
def findNextCheckin(userId, checkins):
    for nextCheckin in checkins:
        if userId == nextCheckin.user_id:
            return nextCheckin
    return None

def isValidCheckin(nextCheckin, checkinId):
    return nextCheckin is not None and not checkinId == nextCheckin.spot_id


# Returns spot age in days, relative to a given checkin date
def calculateSpotAge(checkinDate, spotId):
    spotCreationDate = str(api.getSpotCreationDate(spotId))
    if (checkinDate < spotCreationDate):
        return 0
    d1 = datetime.strptime(checkinDate, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(spotCreationDate, '%Y-%m-%d %H:%M:%S')
    return abs((d2 - d1).days)


# Builds a spot mapping from the given checkins based on occurrence count
#
#
# age of spot   = checkin time - spot creation time
# 
# spotPopularity
#
# 
#
# spotMapping:      spotId | nextSpotId | occurenceCount | weightedPopularity
def buildSpotMapping(checkins):
    print "\nProcessing checkins..."
    spotIds = []
    nextSpotIds = []
    spotMapping = {}
    spotCreationDates = {}
    i = 0   # Used to select checkins after current checkin

    for checkin in checkins:
        nextCheckin = findNextCheckin(checkin.user_id, checkins[i+1:])
        if isValidCheckin(nextCheckin, checkin.id):
            spotId = checkin.spot_id
            nextSpotId = nextCheckin.spot_id

            
            if spotId not in spotCreationDates:
                spotCreationDates[spotId] = calculateSpotAge(nextCheckin.created_on, nextSpotId)

            if (spotId, nextSpotId) in spotMapping:
                spotMapping[(spotId, nextSpotId)] += 1
                #print "Mapping inc: (%d,%d)" % (spotId, nextSpotId)
            else:
                spotMapping[(spotId, nextSpotId)] = 1
                #print "New mapping: (%d,%d)" % (spotId, nextSpotId)
        i += 1

    print "Done processing!"
    return spotMapping

####################################
# Test Code   
####################################
print "Testing..."

api = WhatsNextApi()
endOfCurrentRun = "2012-04-20 00:00:00"

print "\nGetting checkins..."
checkins = api.getAllCheckinsBeforeDate(endOfCurrentRun)
nrCheckins = len(checkins)

print "\nGot %d checkins" % nrCheckins
print "First checkin: %s" % checkins[0].created_on
print "Last checkin: %s" % checkins[nrCheckins-1].created_on

#### Call another function here to change what gets written to database
spotMapping = buildSpotMapping(checkins)
####



print "\nTerminating..."


