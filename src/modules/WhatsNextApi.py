#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
import DBQuery
import time                
import datetime             
import calendar

import os.path
###################################

modulesDir = os.path.dirname(os.path.abspath(__file__))

class WhatsNextApi:
    vsApi = VikingSpotsApiWrapper() 
    lastRun = ""            # End of last run (date)
    endOfCurrentRun = ""


    ## Initialize  ####################################################
    def __init__(self, baseDir):
        filepath = os.path.join(baseDir, "lastrun")
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
    ###################################################################


    ## NIGHT SCRIPT  ##################################################
    ##################### Private functions ###########################
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

    ##################### Public functions ##########################
    # This function retrieves the checkins of the previous day, most recent last
    # 'Today' is determined by lastRun and endOfCurrentRun(=24 hours ahead)
    # This allows us to simulate the adding of new checkins per day
    # Note: SQL Dump has all checkins before 2012-03-12 00:00:00
    def getDayCheckins(self):
        allCheckins = self.vsApi.getUserActions(0,0)
        allCheckins = self.omitCheckinsBeforeLastRun(allCheckins)
        dayCheckins = self.omitCheckinsAfterEndOfCurrentRun(allCheckins)
        return dayCheckins

    # For each checkin, get the next checkin by same user
    # Checkins are already sorted by date (most recent last)
    def findNextCheckin(self, userId, checkins):
        for nextCheckin in checkins:
            if userId == nextCheckin.user_id:
                return nextCheckin
        return None

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
    ###################################################################



    ## DAY SCRIPT  ####################################################
    # This function returns the nth most popular next spots from the
    # nextSpotCount database.
    # QUERY
    #   for spotId, return n spots with highest count
    def getTopNextSpots(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = "SELECT nextSpotId, count FROM nextSpotCount "\
                      "WHERE spotId = %d ORDER BY count DESC LIMIT 0, %d" % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();


        topNextSpots = []
        for row in returnedResults:
            topNextSpots.append(row)
        return topNextSpots
    ###################################################################



    ## MISC.  #########################################################
    def getSpotById(self, id):
        return self.vsApi.getSpotById(id)
    ###################################################################
