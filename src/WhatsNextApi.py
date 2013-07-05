#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
import time                 # occurredInLast24Hours()
import datetime             # occurredInLast24Hours()
###################################


class WhatsNextApi:
    vsApi = VikingSpotsApiWrapper() 

    def retrieveCheckinsFromActions(self, userActions):
        checkins = list()
        for action in userActions:
            if "Checkin" == action.type:    # TODO use correct VikingSpots type for user checkin
                checkins.append(action)
        return checkins

    # created_on format: %Y-%m-%d %H:%M:%S
    def occurredInLast24Hours(self, checkin):
        timeInSec = time.time()
        time24HoursAgo = timeInSec - 24 * 60 * 60 * 30
        timeStr = datetime.datetime.fromtimestamp(time24HoursAgo).strftime('%Y-%m-%d %H:%M:%S')
        if timeStr < checkin.created_on:
            return True
        return False

    # Timespan specifies how far back the user actions go
    # E.g. timespan = 24 returns user actions made in the last 24 hours
    # TODO: Function retrieves a set, limited amount of user actions for now,
    #       should keep asking for more data until actions go further back 
    #       than the given timespan.
    def getDayCheckins(self):
        userActions = self.vsApi.getUserActions(20)
        checkins = self.retrieveCheckinsFromActions(userActions)
        dayCheckins = list()
        for checkin in userActions:
            if self.occurredInLast24Hours(checkin):
                dayCheckins.append(checkin)
        return dayCheckins
