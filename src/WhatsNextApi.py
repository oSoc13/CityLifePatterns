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
    lastRun = ""

    # TODO test what happens when file doens't exist
    def __init__(self):
        file = open(os.path.join(BASE, "lastrun"))
        fileContents = file.read()
        entries = fileContents.split(": ")
        self.lastRun = entries[1]


    def retrieveCheckinsFromActions(self, userActions):
        checkins = list()
        for action in userActions:
            if "Checkin" == action.type:    # TODO use correct VikingSpots type for user checkin
                checkins.append(action)
        return checkins


    def occurredSinceLastRun(self, checkin):
        if self.lastRun < checkin.created_on:
            return True
        return False


    # This function retrieves the checkins of the previous day, most recent last
    # TODO: Function retrieves a set, limited amount of user actions for now,
    #       should keep asking for more data until all data since last run was retrieved
    def getDayCheckins(self):
        userActions = self.vsApi.getUserActions(20) # TODO 
        checkins = self.retrieveCheckinsFromActions(userActions)
        dayCheckins = list()
        for checkin in userActions:
            if self.occurredSinceLastRun(checkin):
                dayCheckins.append(checkin)
        dayCheckins = dayCheckins[::-1]
        return dayCheckins


    # For each checkin, get the next checkin by same user
    # Checkins are already sorted by date (most recent last)
    def findNextCheckin(self, userId, checkins):
        for nextCheckin in checkins:
            if userId == nextCheckin.user_id:
                return nextCheckin
        return None


    # Write current time to file 'lastrun'
    def goingToRun(self):
        file = open('lastrun','w')
        now = time.time()
        nowStr = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        contents = 'Night script was last run on: ' + nowStr
        file.write(contents)

    def runDone(self):
        # TODO write away info about this run if needed
        return

