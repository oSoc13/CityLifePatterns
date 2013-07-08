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

    # TODO rewrite to "occurredSinceLastRun()
    # created_on format: %Y-%m-%d %H:%M:%S
    def occurredInLast24Hours(self, checkin):
        timeInSec = time.time()
        time24HoursAgo = timeInSec - 24 * 60 * 60 * 30
        timeStr = datetime.datetime.fromtimestamp(time24HoursAgo).strftime('%Y-%m-%d %H:%M:%S')
        if timeStr < checkin.created_on:
            return True
        return False

    # This function retrieves the checkins of the previous day, most recent last
    # TODO: Function retrieves a set, limited amount of user actions for now,
    #       should keep asking for more data until all data from last 24 hours was retrieved
    def getDayCheckins(self):
        userActions = self.vsApi.getUserActions(20) # TODO 
        checkins = self.retrieveCheckinsFromActions(userActions)
        dayCheckins = list()
        for checkin in userActions:
            if self.occurredInLast24Hours(checkin):
                dayCheckins.append(checkin)
        dayCheckins = dayCheckins[::-1]
        return dayCheckins

    def countNextSpots(self):
        return

    # For each checkin, get the next checkin by same user
    # Checkins are already sorted by date (most recent last)
    def findNextCheckin(self, checkin, checkins):
        for nextCheckin in checkins:
            if checkin.user_id == nextCheckin.user_id:
                return nextCheckin
        return None


        

