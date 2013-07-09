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

import os.path
BASE = os.path.dirname(os.path.abspath(__file__))
###################################


class WhatsNextApi:
    vsApi = VikingSpotsApiWrapper() 
    lastRun = ""            # End of last run (date)
    endOfCurrentRun = ""

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
            date = datetime.datetime.strptime(self.lastRun, '%Y-%m-%d %H:%M:%S')
            endDate = date + datetime.timedelta(days=1)
            self.endOfCurrentRun = endDate.strftime("%Y-%m-%d %H:%M:%S")
        else:
            print "First run, will retrieve all checkin data..."


    # Write current time to file 'lastrun'
    def goingToRun(self):
        filepath = os.path.join(BASE, "lastrun")
        file = open(filepath, 'w')
        ''' # This code can be used to write the current time to the file
        now = time.time()
        nowStr = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        ''' 
        # But we're reading day checkins from dates further in past (local data dump),
        # write date that is a day further than the last run
        nowStr = self.endOfCurrentRun
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

    def omitCheckinsBeforeLastRun(self, checkins):
        checkins = [checkin for checkin in checkins if self.lastRun < checkin.created_on]
        return checkins

    def omitCheckinsAfterEndOfCurrentRun(self, checkins):
        checkins = [checkin for checkin in checkins if checkin.created_on < self.endOfCurrentRun]
        return checkins
    


    # This function retrieves the checkins of the previous day, most recent last
    # 'Today' is determined by lastRun and endOfCurrentRun(=24 hours ahead)
    # This allows us to simulate the adding of new checkins per day
    # Note: SQL Dump has all checkins before 2012-03-12 00:00:00
    def getDayCheckins(self):
        allCheckins = self.vsApi.getUserActions(0,0)
        allCheckins = self.omitCheckinsBeforeLastRun(allCheckins)
        dayCheckins = self.omitCheckinsAfterEndOfCurrentRun(allCheckins)
        return dayCheckins


    # Reads all checkin data before a given date
    # Used to initialize the database with checkin data
    def getCheckinsBefore(self, date):
        allCheckins = self.vsApi.getUserActions(0,0)
        i = 0
        for checkin in allCheckins:
            if checkin.created_on >= date:
                break
            i += 1
        return allCheckins[:i]


    ''' # This version should run when vsApi.getUseractions() gets data from the VikingSpotsApi
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

    def getSpotById(self, id):
        return self.vsApi.getSpotById(id)
