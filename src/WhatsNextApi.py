#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
import time                
import datetime             
import calendar
###################################


class WhatsNextApi:
    vsApi = VikingSpotsApiWrapper() 
    lastRun = ""

    ## Initialize and breakdown #######################################
    def __init__(self):
        filepath = os.path.join(BASE, "lastrun")
        if os.path.exists(filepath):
            file = open(filepath)
            fileContents = file.read()
            entries = fileContents.split(": ")
            self.lastRun = entries[1]
            if (self.lastRun.endswith("\n")):
                self.lastRun = self.lastRun[:-1]
        else:
            print "First run, will retrieve all checkin data..."


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


    ###################################################################
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

    def getCheckinsAfterLastRun(self, checkins):
        checkins = [checkin for checkin in checkins if self.occurredSinceLastRun(checkin)]
        return checkins 

    def containsCheckinsBeforeLastRun(self, checkins):
        for checkin in checkins:
            if checkin.created_on <= self.lastRun:
                return True
        return False


    # This function retrieves the checkins of the previous day, most recent last
    # TODO when we're on a first run (lastRun == ""), get _all_ checkins
    # This version runs when using local checkin data

    # TODO
    def getDayCheckins(self):
        dayCheckins = list()
        allDayCheckinsRetrieved = False
        allCheckins = self.vsApi.getUserActions(0,0)
        end = len(allCheckins)
        start = end - 20
        # We loop until all checkins occurring after the last run are found
        while not allDayCheckinsRetrieved: 
            checkins = allCheckins[start::end]
            if self.containsCheckinsBeforeLastRun(checkins):
                allDayCheckinsRetrieved = True
                checkins = self.getCheckinsAfterLastRun(checkins)
            for checkin in checkins: 
                dayCheckins.append(checkin)
            start -= 20
            end -= 20

        dayCheckins = dayCheckins[::-1]
        return dayCheckins

    ''' # This version should when vsApi.getUseractions() gets data from VikingSpotsApi
    def getDayCheckins(self):
        dayCheckins = list()
        allDayCheckinsRetrieved = False
        skip = 0
        # We loop until all checkins occurring after the last run are found
        while not allDayCheckinsRetrieved: 
            userActions = self.vsApi.getUserActions(20, skip) 
            skip += len(userActions)
            #checkins = self.retrieveCheckinsFromActions(userActions)
            checkins = userActions # TODO change to 'checkins' when working with real data
            if self.containsCheckinsBeforeLastRun(checkins):
                allDayCheckinsRetrieved = True
                checkins = self.getCheckinsAfterLastRun(checkins)
            for checkin in checkins: 
                dayCheckins.append(checkin)
        dayCheckins = dayCheckins[::-1]
        return dayCheckins
    '''


    # For each checkin, get the next checkin by same user
    # Checkins are already sorted by date (most recent last)
    def findNextCheckin(self, userId, checkins):
        for nextCheckin in checkins:
            if userId == nextCheckin.user_id:
                return nextCheckin
        return None
