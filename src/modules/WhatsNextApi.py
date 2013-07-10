#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
import DBQuery
###################################

class WhatsNextApi:
    vsApi = VikingSpotsApiWrapper() 
    lastRun = ""
    endOfCurrentRun = ""

    ## Building the database  #########################################
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

    ######

    # This function retrieves the checkins of the previous day, most recent last
    # 'Today' is determined by lastRun and endOfCurrentRun(=24 hours ahead)
    # This allows us to simulate the adding of new checkins per day
    # Note: SQL Dump has all checkins before 2012-03-12 00:00:00
    def getDayCheckins(self):
        allCheckins = self.vsApi.getUserActions(0,0)
        allCheckins = self.omitCheckinsBeforeLastRun(allCheckins)
        dayCheckins = self.omitCheckinsAfterEndOfCurrentRun(allCheckins)
        return dayCheckins

    def getAllCheckinsBeforeDate(self, date):
        allCheckins = self.vsApi.getUserActions(0,0)
        checkins = [checkin for checkin in allCheckins if checkin.created_on < date]
        return checkins

    # For each checkin, get the next checkin by same user
    # Checkins are already sorted by date (most recent last)
    def findNextCheckin(self, userId, checkins):
        for nextCheckin in checkins:
            if userId == nextCheckin.user_id:
                return nextCheckin
        return None

    # Builds a spot mapping from the given checkins based on occurrence count
    def buildSpotMapping(self, checkins):
        print "\nProcessing checkins..."
        spotIds = []
        nextSpotIds = []
        spotMapping = {}
        i = 0   # Used to select checkins after current checkin
        for checkin in checkins:
            if i % 1000 == 0:
                print "Processing checkin %d..." % i
            i += 1
            nextCheckin = self.findNextCheckin(checkin.user_id, checkins[i+1:])
            if nextCheckin is not None and not checkin.spot_id == nextCheckin.spot_id:
                spotId = checkin.spot_id
                nextSpotId = nextCheckin.spot_id
                if (spotId, nextSpotId) in spotMapping:
                    spotMapping[(spotId, nextSpotId)] += 1
                    #print "Mapping inc: (%d,%d)" % (spotId, nextSpotId)
                else:
                    spotMapping[(spotId, nextSpotId)] = 1
                    #print "New mapping: (%d,%d)" % (spotId, nextSpotId)
        print "Done processing!"
        return spotMapping
  

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



    ## Getting next spot data  ########################################

    # This function returns the nth most popular next spots from the
    # nextSpotCount database.
    # QUERY
    #   for spotId, return n spots with highest count
    # Called by API to return JSON data
    def getPopularNextSpots(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = "SELECT nextSpotId, count FROM nextSpotCount "\
                      "WHERE spotId = %d ORDER BY count DESC LIMIT 0, %d" % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        topNextSpots = []
        for row in returnedResults:
            topNextSpots.append(row)
        return topNextSpots

    # Must return string
    def getPopularNextSpotsJSON(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = "SELECT nextSpotId, count FROM nextSpotCount "\
                      "WHERE spotId = %d ORDER BY count DESC LIMIT 0, %d" % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        topNextSpots = []
        for row in returnedResults:
            topNextSpots.append(row)
        
        # TODO clean up
        JSON = "{ "
        JSON += "\"meta\": { \"code\": \"200\" }, "
        JSON += "\"response\": { " \
                "\"count\": \"%d\", " % len(topNextSpots)

        JSON += "\"spots\": [ "
        for (spotId,count) in topNextSpots:
            spotJSON = self.vsApi.getSpotByIdJSON(spotId)
            JSON += spotJSON
            JSON += ", "
        JSON = JSON[:-2]
        JSON += "] } }"
        return JSON
    ###################################################################



    ## MISC.  #########################################################
    def getSpotById(self, id):
        return self.vsApi.getSpotById(id)

    # Set the token to be used when calling the VikingSpots API
    def useToken(self, token):
        self.vsApi.token = token
    ###################################################################