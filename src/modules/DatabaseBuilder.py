#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# Testing class
#
###################################
import sys
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
import writeToDb
from writeToDb import *
import math
import datetime
import DBQuery
###################################

class DatabaseBuilder():
    lastRun = ''
    endOfCurrentRun = ''

    __vsApi = VikingSpotsApiWrapper()

    # Data that should come from DB or from file
    __oldMultipliers = {}
    __spotCreationDates = {}

    # Settings
    __multiplierRanges = {'spotAge': 2, 'timeSpent': 2}
    __weights = {'spotAge': 0.3, 'timeSpent': 0.7}     # Sum must be 1

    # The build functions
    ##############################################################
    # This function builds the entire database from scratch.
    # It starts with the first checkin in the data dump and processes
    # all checkins on a per-day basis
    def buildFromScratch(self):
        startDate = "2012-03-13 04:00:00"
        #endDate = "2014-04-01 00:00:00"

        startdt1 = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        dt1 = startdt1
        dt2 = dt1 + datetime.timedelta(days=1)

        # TODO remove truncate when final version of db is made
        DBQuery.openConnection();
        DBQuery.queryDB("TRUNCATE whatsnext;")
        DBQuery.closeConnection();

        # TODO change this so it spans all checkins
        nrDays = 120
        for n in range(nrDays):
            date1 = dt1.strftime("%Y-%m-%d %H:%M:%S")
            date2 = dt2.strftime("%Y-%m-%d %H:%M:%S")
            #print "======================================================="
            #print "Getting checkins of day %d..." % n
            checkins = self.__getAllCheckinsBetweenDates(date1, date2)

            nrCheckins = len(checkins)
            if nrCheckins > 0:
                #print "\nGot %d checkins" % nrCheckins
                #print "First checkin: %s" % checkins[0].created_on
                #print "Last checkin: %s" % checkins[nrCheckins-1].created_on

                #### Call another function here to change what gets written to database
                spotMapping = self.buildSpotMapping(checkins)
                ####
                if len(spotMapping) > 1:
                    #print "\nFound %d spot mapping(s) today! \o/" % len(spotMapping)
                    #print "\nWriting to DB..."
                    writeToDbNew(spotMapping)
                    #print "Done writing to DB..."
                    #else:
                    #print "\nDidn't find any spot mappings today... :("
                    #else:
                    #print "No checkins today, moving on..."

            dt1 = dt2
            dt2 = dt1 + datetime.timedelta(days=1)
            #print "\nTerminating..."

    def updateSinceLastRun(self):
        # TODO Put night script contents here
        return

    # Building the spot mapping
    ##############################################################
    # Builds a spot mapping from the given checkins:
    # (spotId,nextSpotId) | dayCount | lastOccurrence | MspotAge | MtimeSpent |
    #                          int             date           float           float
    # TODO make private when night script contents are in this file
    def buildSpotMapping(self, checkins):
        # Build today's parameters
        parameters = self.__calculateParameters(checkins)
        newMultipliers = self.__calculateNewMultipliers(parameters)

        dbRows = {}
        weightedPopularity = {}
        DBQuery.openConnection();
        for key in parameters:
            weightedPopularity[key] = {}
            weightedPopularity[key]['weightedPopularity'] = self.__calculateNewWeightedPopularity(
                newMultipliers[key],
                parameters[key]['dayCount'],key)
            parameters[key].pop('variance', None)
            parameters[key].pop('averageTimeSpent', None)
            parameters[key].pop('MtimeSpent', None)
            dbRows[key] = dict(parameters[key].items() + newMultipliers[key].items() + \
                               weightedPopularity[key].items())
        DBQuery.closeConnection();
        return dbRows

    # Multiplier and parameter calculations
    ##############################################################
    def __calculateParameters(self, checkins):
        global now
        parameters = {}     # (spotId,nextSpotId) | dayCount | spotCreationDate| lastOccurrence | spotAge
        i = 0               # Used to select checkins after current checkin

        DBQuery.openConnection();
        for checkin in checkins:
            nextCheckin = self.__findNextCheckin(checkin.user_id, checkins, i)
            i += 1
            if nextCheckin is not None and nextCheckin.spot_id != checkin.spot_id:
                spotId = checkin.spot_id
                nextSpotId = nextCheckin.spot_id
                key = (spotId,nextSpotId)
                now = nextCheckin.created_on  # In non-simulation, use current time
                timeSpent = self.__calculateTimeSpent(checkin.created_on, nextCheckin.created_on)
                # Save the parameters
                if key in parameters:
                    storedCount =  parameters[key]['dayCount']
                    parameters[key]['dayCount'] += 1
                    newCount = parameters[key]['dayCount']

                    storedAverageVariance = parameters[key]['variance']
                    storedAverageTimeSpent = parameters[key]['averageTimeSpent']
                    oldMultiplier = parameters[key]['MtimeSpent']

                    parameters[key]['lastOccurrence'] = nextCheckin.created_on

                    averageTimeSpent = int(float(storedAverageTimeSpent * storedCount) + timeSpent) / newCount
                    sumOfSquares = (storedAverageVariance*(storedCount-1)+(storedCount*storedAverageTimeSpent*storedAverageTimeSpent))+(timeSpent*timeSpent)
                    variance = int(float( sumOfSquares / (storedCount) ) - float( float(newCount/storedCount) * averageTimeSpent * averageTimeSpent ))


                    if(storedAverageVariance != 0 and averageTimeSpent != 0):
                        thisMultiplier = float( 2 * math.exp( - float(float(timeSpent - averageTimeSpent)**2 ) / ( 2 * storedAverageVariance ) ) )
                    else:
                        thisMultiplier = 1

                    timeMultiplier = float(float(float(oldMultiplier*storedCount) + float(thisMultiplier)*2)/(newCount+1))
                    parameters[key]["variance"] = variance
                    parameters[key]["averageTimeSpent"] = averageTimeSpent
                    parameters[key]["MtimeSpent"] = timeMultiplier

                else:
                    if nextSpotId not in self.__spotCreationDates:
                        self.__spotCreationDates[nextSpotId] = str(self.__vsApi.getSpotCreationDate(spotId))
                    spotAge = self.__calculateSpotAge(nextCheckin.created_on, self.__spotCreationDates[nextSpotId])
                    parameters[key] = { 'dayCount': 1,
                                        'spotCreationDate': self.__spotCreationDates[nextSpotId],
                                        'lastOccurrence': nextCheckin.created_on,
                                        'spotAge': spotAge,
                                        'variance': 0.0,
                                        'averageTimeSpent': timeSpent,
                                        'MtimeSpent': 1.0 }
        DBQuery.closeConnection();
        return parameters

    # This function retrieves the checkins of the previous day, most recent last
    # 'Today' is determined by lastRun and endOfCurrentRun(=24 hours ahead)
    # This allows us to simulate the adding of new checkins per day
    # Note: SQL Dump has all checkins before 2012-03-12 00:00:00
    def getDayCheckins(self):
        return self.__getAllCheckinsBetweenDates(self.lastRun, self.endOfCurrentRun)

    # TODO upgrade performance, currently ALL checkins are read from data dump at each call
    def __getAllCheckinsBetweenDates(self, date1, date2):
        checkins = self.__vsApi.getUserActions(0,0)
        checkins = self.__omitCheckinsBeforeDate(checkins, date1)
        checkins = self.__omitCheckinsAfterDate(checkins, date2)
        return checkins

    # Spot ages are in days
    def __calculateNewSpotAgeMultiplier(self, parameters, oldestAge):
        spotAge = parameters['spotAge']
        if spotAge < 1:
            return 2
        # spotAge / oldestSpotAge -> normalizes range to 0-1
        # normalized * 2          -> expands range to 0-2
        
        multiplier = (((float(oldestAge)-float(spotAge)) / float(oldestAge))* self.__multiplierRanges['spotAge'] )
        return multiplier

    # Calculate new multipliers
    def __calculateNewMultipliers(self, parameters):
        newMultipliers = {} # (spotId,nextSpotId) | MspotAge | MlastOccurrence | .. timeSpentW
        creationDateOldestSpot = "2011-11-25 17:34:05" # Hardcoded, comes from spot with id=2
        oldestSpotAge = self.__calculateSpotAge(now, creationDateOldestSpot)

        DBQuery.openConnection();
        for key in parameters:
            newMultipliers[key] = {}
            newMultipliers[key]['MspotAge'] = self.__calculateNewSpotAgeMultiplier(parameters[key], oldestSpotAge)

            variables = self.__readVariablesFromDB(key)
            if variables != None:
                databaseCount = variables['totalCount']
                storedAverageVariance = variables['storedAverageVariance']
                storedAverageTimeSpent = variables['storedAverageTimeSpent']
                storedMultiplier = variables['oldMultiplier']
                dayCount = parameters[key]['dayCount']
                dayAverageTimeSpent = parameters[key]['averageTimeSpent']
                dayAverageVariance = parameters[key]['variance']
                dayMultiplier = parameters[key]['MtimeSpent']

                totalCount = databaseCount + dayCount

                averageTimeSpent = int(float(storedAverageTimeSpent * databaseCount) + (dayAverageTimeSpent * dayCount) ) / totalCount
                sumOfSquares = (storedAverageVariance*(databaseCount-1)+(databaseCount*storedAverageTimeSpent**2))+(dayAverageVariance*(dayCount-1)+(dayCount*dayAverageTimeSpent**2))
                variance = int(float( sumOfSquares / (totalCount - 1) ) - float( float(totalCount/(totalCount-1)) * averageTimeSpent **2 ))

                timeMultiplier = float(float(float(storedMultiplier*databaseCount) + float(dayMultiplier*dayCount)*2)/(totalCount+dayCount))
                newMultipliers[key]["variance"] = variance
                newMultipliers[key]["averageTimeSpent"] = averageTimeSpent
                newMultipliers[key]["MtimeSpent"] = timeMultiplier
            else:
                newMultipliers[key]["variance"] = parameters[key]['variance']
                newMultipliers[key]["averageTimeSpent"] = parameters[key]['averageTimeSpent']
                newMultipliers[key]["MtimeSpent"] = parameters[key]['MtimeSpent']
        DBQuery.closeConnection();
        return newMultipliers

    # New popularity calculation
    ##############################################################
    # This function is reponsible for calculating the new weighted popularity
    # of this spot-nextSpot occurence
    #
    # weightedPopularity (0.0-2.0..)
    #
    #  x) Takes into account spot age
    #  x) Uses 'last checkindate' to gauge popularity, this should be optimized
    #   ) Gives new/young spots popularity boost
    #
    def __calculateNewWeightedPopularity(self, multipliers, dayCount,key):

        masterMultiplier = self.__weights['spotAge'] * multipliers['MspotAge'] + \
                           self.__weights['timeSpent'] * multipliers['MtimeSpent']
        
        dayPopularity = dayCount * masterMultiplier
        print "daypop: %s | dayCount: %s" % (dayPopularity, dayCount);
        variables = self.__readVariablesFromDB(key)
        if variables != None:
            oldPopularity = variables['weightedPopularity']
            databaseCount = variables['totalCount']
        else:
            oldPopularity = 1  # TODO Should be read from DB
            databaseCount = 0
        alpha = 0.7 / 1.7
        beta = 1 / 1.7
        
        #newPopularity = alpha * oldPopularity + beta * dayPopularity
        oldPopularity = databaseCount * oldPopularity        
        newPopularity = (alpha * oldPopularity) + (beta * dayPopularity)
        
        #now map this popularity from 0 to 100
        DBQuery.openConnection();
        query = "SELECT sum(totalCount) FROM whatsnext WHERE spotId = %s" % key[0]
        results = DBQuery.queryDB(query)
        print results
        DBQuery.closeConnection();
        if len(results)> 0:
            row = results[0]
            if row[0] != "None":
                print row[0]
                dbSpotCount = int(row[0])
            else:
                dbSpotCount = 0
        else:
            dbSpotCount = 0
        
        mappedNewPopularity = newPopularity / (dbSpotCount* dayCount)* 100
        newPopularity = mappedNewPopularity
        
        print "oldpop: %s | daypop: %s | newpop: %s" % (oldPopularity, dayPopularity, newPopularity)
        return newPopularity

    # Helper functions
    ##############################################################
    # Get the next checkin by same user
    # Assumption: checkins are already sorted by date (most recent last)
    def __findNextCheckin(self, userId, checkins, index):
        checkins = checkins[index+1:]
        return next((nextCheckin for nextCheckin in checkins if userId == nextCheckin.user_id), None)

    # Returns spot age in days, relative to a given checkin date
    def __calculateSpotAge(self, checkinDate, spotCreationDate):
        if (checkinDate < spotCreationDate):
            return 0
        d1 = datetime.datetime.strptime(spotCreationDate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.strptime(checkinDate, '%Y-%m-%d %H:%M:%S')
        return abs((d2 - d1).days)

    def __calculateTimeSpent(self, checkinTime, nextCheckintime):
        if (nextCheckintime < checkinTime):
            return 0
        d1 = datetime.datetime.strptime(checkinTime, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.strptime(nextCheckintime, '%Y-%m-%d %H:%M:%S')
        return abs((d2 - d1).seconds//60)

    def __readVariablesFromDB(self, key):
        query = "SELECT totalCount, variance, averageTimeSpent, MtimeSpent, weightedPopularity FROM whatsnext " \
                "WHERE spotId = '%s' AND nextSpotId = '%s';" % (key[0], key[1])
        
        results = DBQuery.queryDB(query)

        if len(results) > 0:
            row = results[0]
            variables = {'totalCount': int(row[0]), 'storedAverageVariance': float(row[1]),
                         'storedAverageTimeSpent': float(row[2]), 'oldMultiplier': float(row[3]), 'weightedPopularity': float(row[4])}
            return variables
        else:
            return None

    def __occurredSinceLastRun(self, checkin):
        if self.lastRun < checkin.created_on:
            return True
        return False

    def __omitCheckinsBeforeDate(self, checkins, date):
        checkins = [checkin for checkin in checkins if date < checkin.created_on]
        return checkins

    def __omitCheckinsAfterDate(self, checkins, date):
        checkins = [checkin for checkin in checkins if checkin.created_on < date]
        return checkins


dbBuilder = DatabaseBuilder()

# Uncomment if you want to refill the database
dbBuilder.buildFromScratch()

# Uncomment if you want to update since last day's checkins
#dbBuilder.updateSinceLastRun
