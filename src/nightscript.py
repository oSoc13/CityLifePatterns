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
###################################

api = WhatsNextApi()
#api.goingToRun()  

checkins = api.getDayCheckins()
spotIds = []
nextSpotIds = []
spotMapping = {}
i = 0   # Used to select checkins after current checkin

# Build a local cache of spot mappings
for checkin in checkins:
    nextCheckin = api.findNextCheckin(checkin.user_id, checkins[i+1::])
    if nextCheckin is not None:
        spotId = checkin.spot_id
        nextSpotId = nextCheckin.spot_id
        if (spotId, nextSpotId) in spotMapping:
            spotMapping[(spotId, nextSpotId)] += 1
        else:
            spotMapping[(spotId, nextSpotId)] = 1
    i += 1


# TODO write data to database
for each in spotMapping:
    print each
    print spotMapping[each]

api.runDone()
