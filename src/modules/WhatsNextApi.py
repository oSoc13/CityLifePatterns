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
    # This function returns the nth most popular next spots from the
    # nextSpotCount database.
    # QUERY
    #   for spotId, return n spots with highest count
    # Called by API to return JSON data
    def getPopularNextSpots(self, spotId, nrSpots):
        queryString = 'SELECT nextSpotId, count FROM nextSpotCount '\
                      'WHERE spotId = %d ORDER BY count DESC LIMIT 0, %d' % (spotId, nrSpots)
        DBQuery.openConnection();
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        topNextSpots = []
        for row in returnedResults:
            topNextSpots.append(row)
        return topNextSpots

    # Must return string
    def getPopularNextSpotsJSON(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = 'SELECT nextSpotId, totalCount FROM whatsnext ' \
                      'WHERE spotId = %d ' \
                      'ORDER BY weightedPopularity DESC LIMIT 0, %d' % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        nextSpots = []
        for row in returnedResults:
            nextSpots.append(row)
        return self.__formJsonResponse(nextSpots)

    # Must return string
    def getPopularNextSpotsByCountJSON(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = 'SELECT nextSpotId, count FROM nextSpotCount '\
                      'WHERE spotId = %d ORDER BY count DESC LIMIT 0, %d' % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        nextSpots = []
        for row in returnedResults:
            nextSpots.append(row)
        return self.__formJsonResponse(nextSpots)

    # Must return string
    def getPopularNextSpotsBySpotAgeJSON(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = 'SELECT nextSpotId, totalCount FROM whatsnext '\
                      'WHERE spotId = %d ORDER BY (totalCount*MspotAge) DESC LIMIT 0, %d' % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        nextSpots = []
        for row in returnedResults:
            nextSpots.append(row)
        return self.__formJsonResponse(nextSpots)

    # Must return string
    def getPopularNextSpotsBySpotAgeJSON(self, spotId, nrSpots):
        DBQuery.openConnection();
        queryString = 'SELECT nextSpotId, totalCount FROM whatsnext '\
                      'WHERE spotId = %d ORDER BY (totalCount*MtimeSpent) DESC LIMIT 0, %d' % (spotId, nrSpots)
        returnedResults = DBQuery.queryDB(queryString)
        DBQuery.closeConnection();

        nextSpots = []
        for row in returnedResults:
            nextSpots.append(row)
        return self.__formJsonResponse(nextSpots)


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
    # TODO! This is not sorted D: FIX!
    def __formJsonSpotsArray(self, nextSpots):
        JSON = ''
        JSON += '\'spots\': [ '
        for (spotId,count) in nextSpots:
            spotJSON = self.__vsApi.getSpotByIdJSON(spotId)
            if spotJSON is not None:
                JSON += spotJSON
                JSON += ', '
        JSON = JSON[:-2]
        JSON += '] '
        return JSON

    def __formJsonResponse(self, nextSpots):
        nrSpots = len(nextSpots)
        JSON = '{ '
        JSON += '\'meta\': { \'code\': \'200\' }, '
        JSON += '\'response\': { '
        if nrSpots > 1:
            JSON +='\'count\': \'%d\', ' % nrSpots
            JSON += self.__formJsonSpotsArray(nextSpots)
        else:
            JSON +='\'count\': 0 '
        JSON += '} }'
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



