#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# This is the night script that is responsible for updating the WhatsNext database.
#
###################################
import WhatsNextApi
from WhatsNextApi import *
import sys
sys.path.insert(0, './core')    # Specify additional directory to load python modules from
import writeToDb
###################################

api = WhatsNextApi()
#api.goingToRun()  

print "Getting day checkins..."
checkins = api.getDayCheckins()
print "Got %d day checkins." % len(checkins)
spotIds = []
nextSpotIds = []
spotMapping = {}
i = 0   # Used to select checkins after current checkin

for checkin in checkins:
    print checkin.created_on

'''
# Build a local cache of spot mappings
print "Processing checkins..."
print "Nr of checkins = %d" % len(checkins)
for checkin in checkins:
    if i % 1000 == 0:
        print "At checkin %d" % i
    nextCheckin = api.findNextCheckin(checkin.user_id, checkins[i+1::])
    if nextCheckin is not None:
        spotId = checkin.spot_id
        nextSpotId = nextCheckin.spot_id
        if (spotId, nextSpotId) in spotMapping:
            spotMapping[(spotId, nextSpotId)] += 1
        else:
            spotMapping[(spotId, nextSpotId)] = 1
    i += 1

print "Done processing!"
'''

print "Writing to DB..."
#writeToDb.write(spotMapping)
'''
for each in spotMapping:
    print each
    print spotMapping[each]
'''
print "Done writing to DB!" 

api.runDone()
