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
    __vsApi = VikingSpotsApiWrapper()

    # Functions for getting "what's next?" spots
    ###################################################################
    #   Called by API to get spots as JSON string
    #   These function return the nth most popular next spots from the whatsnext database.
    #   Each function returns spots based on different multipliers (for testing purposes), see comment at each function.

    # Uses all weights
    def getPopularNextSpotsJSON(self, spotId, nrSpots, userToken=''):
        query = 'SELECT nextSpotId FROM whatsnext ' \
                      'WHERE spotId = %d ' \
                      'ORDER BY weightedPopularity DESC LIMIT 0, %d' % (spotId, nrSpots)
        return self.__resultsOfQueryAsJson(query, userToken)

    # Uses only the total count per spot mapping
    def getPopularNextSpotsByCountJSON(self, spotId, nrSpots, userToken=''):
        query = 'SELECT nextSpotId FROM whatsnext '\
                      'WHERE spotId = %d ORDER BY totalCount DESC LIMIT 0, %d' % (spotId, nrSpots)
        return self.__resultsOfQueryAsJson(query, userToken)

    # Uses only the spot age weight
    def getPopularNextSpotsBySpotAgeJSON(self, spotId, nrSpots, userToken=''):
        query = 'SELECT nextSpotId FROM whatsnext '\
                      'WHERE spotId = %d ORDER BY (totalCount*MspotAge) DESC LIMIT 0, %d' % (spotId, nrSpots)
        return self.__resultsOfQueryAsJson(query, userToken)

    # Uses only the time spent weight
    def getPopularNextSpotsByTimeSpentJSON(self, spotId, nrSpots, userToken=''):
        query = 'SELECT nextSpotId FROM whatsnext '\
                      'WHERE spotId = %d ORDER BY (totalCount*MtimeSpent) DESC LIMIT 0, %d' % (spotId, nrSpots)
        return self.__resultsOfQueryAsJson(query, userToken)


    # MISC.
    ###################################################################
    def getSpotById(self, id):
        return self.__vsApi.getSpotById(id)
    
    def getSpotCreationDate(self, spotId):
        return self.__vsApi.getSpotCreationDate(spotId)

    # Set the token to be used when calling the VikingSpots API
    def useToken(self, token):
        self.__vsApi.token = token

    # Helper Functions
    ###################################################################
    def __resultsOfQueryAsJson(self, query, userToken=''):
        DBQuery.openConnection();
        results = DBQuery.queryDB(query)
        DBQuery.closeConnection();

        nextSpots = []
        for row in results:
            nextSpots.append(row)
        return self.__formJsonResponse(nextSpots, userToken)

    def __formJsonResponse(self, nextSpots, userToken=''):
        nrSpots = len(nextSpots)
        JSON = '{ '
        JSON += '\"meta\": { \"code\": \"200\" }, '
        JSON += '\"response\": { '
        if nrSpots > 1:
            JSON +='\"count\": \"%d\", ' % nrSpots
            JSON += self.__formJsonSpotsArray(nextSpots, userToken)
        else:
            JSON +='\"count\": 0 '
        JSON += '} }'
        return JSON

    # TODO! This is not sorted D: FIX!
    def __formJsonSpotsArray(self, nextSpots, userToken=''):
        JSON = ''
        JSON += '\"spots\": [ '
        for spotId in nextSpots:
            spotJSON = self.__vsApi.getSpotByIdJSON(spotId, userToken)
            if spotJSON is not None:
                JSON += spotJSON
                JSON += ', '

        JSON = JSON[:-2]
        JSON += '] '
        return JSON



    # Unused functions
    ###################################################################
    #    Initial code used User Actions from VikingSpots actions, functions in this section
    #    worked with that setup and are unused now since we switched to a local data dump.
    #    Left these functions anyway for potential future use.

    # This version should run when vsApi.getUseractions() gets data from the VikingSpotsApi
    def getDayCheckins(self):
        dayCheckins = list()
        allDayCheckinsRetrieved = False
        skip = 0
        # We loop until all checkins occurring after the last run are found
        while not allDayCheckinsRetrieved:
            userActions = self.__vsApi.getUserActions(20, skip)
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

    def retrieveCheckinsFromActions(self, userActions):
        checkins = []
        for action in userActions:
            if 'Checkin' == action.type:    # TODO use correct VikingSpots type for user checkin
                checkins.append(action)
        return checkins

    def getCheckinsAfterLastRun(self, checkins):
        checkins = [checkin for checkin in checkins if self.__occurredSinceLastRun(checkin)]
        return checkins

    def containsCheckinsBeforeLastRun(self, checkins):
        for checkin in checkins:
            if checkin.created_on <= self.lastRun:
                return True
        return False

    def getAllCheckinsBeforeDate(self, date):
        allCheckins = self.__vsApi.getUserActions(0,0)
        checkins = [checkin for checkin in allCheckins if checkin.created_on < date]
        return checkins



