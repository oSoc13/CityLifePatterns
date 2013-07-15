#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# Testing class
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import WhatsNextApi
from WhatsNextApi import *
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
from writeToDb import *
import time          
import math      
import datetime
import calendar
import DBQuery
###################################

api = WhatsNextApi()

# Data that should come from DB or from file 
##############################################################
oldMultipliers = { }
spotCreationDates = {}
multiplierRanges = { 'spotAge': 2, 'timeSpent': 2 }
weights = {'spotAge': 1.0, 'timeSpent': 0.0}     # Sum must be 1


# Helper functions
##############################################################
# For each checkin, get the next checkin by same user
# Checkins are already sorted by date (most recent last)
def findNextCheckin(userId, checkins, index):
    checkins = checkins[index+1:]
    return next((nextCheckin for nextCheckin in checkins if userId == nextCheckin.user_id), None)


# Returns spot age in days, relative to a given checkin date
def calculateSpotAge(checkinDate, spotCreationDate):
    if (checkinDate < spotCreationDate):
        return 0
    d1 = datetime.datetime.strptime(spotCreationDate, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(checkinDate, '%Y-%m-%d %H:%M:%S')
    return abs((d2 - d1).days)

def readVariablesFromDB(key):
    query = "SELECT totalCount, variance, averageTimeSpent, MtimeSpent FROM whatsnext " \
            "WHERE spotId = '%s' AND nextSpotId = '%s';" % (key[0], key[1])
    results = DBQuery.queryDB(query)
    if len(results) > 0:
        row = results[0]
        variables = {'totalCount': int(row[0]), 'storedAverageVariance': float(row[1]),
                'storedAverageTimeSpent': float(row[2]), 'oldMultiplier': float(row[3])}
        return variables
    else:
        return None


def doTimeSpentCalculations(key, parameters, timeSpent):
    variables = readVariablesFromDB(key)
    if variables == None:
        return

    totalCount = variables['totalCount']
    storedAverageVariance = variables['storedAverageVariance']
    storedAverageTimeSpent = variables['storedAverageTimeSpent']
    oldMultiplier = variables['oldMultiplier']
    thisMultiplier = 1

    newTotalCount = totalCount + 1
    averageTimeSpent = int(float(storedAverageTimeSpent * totalCount) + timeSpent) / newTotalCount
    sumOfSquares = (storedAverageVariance*(totalCount-1) +
                        (totalCount*storedAverageTimeSpent**2)) + (timeSpent**2)
    variance = int(float( sumOfSquares / (totalCount) ) - float( float(newTotalCount/totalCount) * averageTimeSpent **2))
 
                       
    if (storedAverageVariance != 0 and averageTimeSpent != 0):
        thisMultiplier = float( 2 * math.exp( - float(float(timeSpent - averageTimeSpent)**2 ) / 
                    ( 2 * storedAverageVariance ) ) )
    
    timeMultiplier = float(float(float(oldMultiplier*totalCount) + 
                     float(thisMultiplier)*2)/(newTotalCount+1))                    

    parameters['variance'] = variance
    parameters['averageTimeSpent'] = averageTimeSpent
    parameters['MtimeSpent'] = timeMultiplier
    return parameters


def calculateTimeSpent(checkinTime, nextCheckintime):
    if (nextCheckintime < checkinTime):
        return 0
    d1 = datetime.datetime.strptime(checkinTime, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(nextCheckintime, '%Y-%m-%d %H:%M:%S')
    return abs((d2 - d1).seconds//60)

# Multiplier and parameter calculations 
##############################################################
def calculateParameters(checkins):
    global now
    parameters = {}     # (spotId,nextSpotId) | dayCount | spotCreationDate| lastOccurrence | spotAge
    i = 0               # Used to select checkins after current checkin

    DBQuery.openConnection();
    for checkin in checkins:
        nextCheckin = findNextCheckin(checkin.user_id, checkins, i)
        i += 1
        if nextCheckin is not None and nextCheckin.spot_id != checkin.spot_id:
            spotId = checkin.spot_id
            nextSpotId = nextCheckin.spot_id
            key = (spotId,nextSpotId)
            now = nextCheckin.created_on  # In non-simulation, use current time
            timeSpent = calculateTimeSpent(checkin.created_on, nextCheckin.created_on)
            # Save the parameters
            if key in parameters:
                parameters[key]['dayCount'] += 1
                parameters[key]['lastOccurrence'] = nextCheckin.created_on
                results = doTimeSpentCalculations(key, parameters[key], timeSpent)
                if None != results:
                    parameters[key] = results
            else:
                if nextSpotId not in spotCreationDates:
                    spotCreationDates[nextSpotId] = str(api.getSpotCreationDate(spotId))
                spotAge = calculateSpotAge(nextCheckin.created_on, spotCreationDates[nextSpotId])
                parameters[key] = { 'dayCount': 1, 
                                    'spotCreationDate': spotCreationDates[nextSpotId],
                                    'lastOccurrence': nextCheckin.created_on, 
                                    'spotAge': spotAge,
                                    'variance': 0.0,
                                    'averageTimeSpent': timeSpent,
                                    'MtimeSpent': 1.0 }
    DBQuery.closeConnection();
    return parameters

# Spot ages are in days
def calculateNewSpotAgeMultiplier(parameters, oldestAge):
    spotAge = parameters['spotAge']
    if spotAge < 1:
        return 2
    # spotAge / oldestSpotAge -> normalizes range to 0-1
    # normalized * 2          -> expands range to 0-2
    multiplier = 1 / ( (float(spotAge)) / float(oldestAge) * multiplierRanges['spotAge'] )
    return multiplier
    

# Calculate new multipliers
def calculateNewMultipliers(parameters):
    newMultipliers = {} # (spotId,nextSpotId) | MspotAge | MlastOccurrence | .. timeSpentW
    creationDateOldestSpot = "2011-11-25 17:34:05" # Hardcoded, comes from spot with id=2
    oldestSpotAge = calculateSpotAge(now, creationDateOldestSpot)

    for key in parameters:
        newMultipliers[key] = {}
        newMultipliers[key]['MspotAge'] = calculateNewSpotAgeMultiplier(parameters[key], oldestSpotAge)
        newMultipliers[key]['MtimeSpent'] = parameters[key]['MtimeSpent']
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
def calculateNewWeightedPopularity(multipliers, dayCount):

    masterMultiplier = weights['spotAge'] * multipliers['MspotAge'] + \
                       weights['timeSpent'] * multipliers['MtimeSpent']

    dayPopularity = dayCount * masterMultiplier
    oldPopularity = 0  # TODO Should be read from DB
    alpha = 0.7
    beta = 0.3
    newPopularity = (alpha * oldPopularity) + (beta * dayPopularity)
    return newPopularity


# Building the spot mapping
##############################################################
# Builds a spot mapping from the given checkins:
# (spotId,nextSpotId) | dayCount | lastOccurrence | MspotAge | MtimeSpent | 
#                          int             date           float           float
def buildSpotMapping(checkins):
    # Build today's parameters
    parameters = calculateParameters(checkins)
    newMultipliers = calculateNewMultipliers(parameters)

    dbRows = {}
    weightedPopularity = {}
    for key in parameters:
        weightedPopularity[key] = {}
        weightedPopularity[key]['weightedPopularity'] = calculateNewWeightedPopularity(
                                                            newMultipliers[key], 
                                                            parameters[key]['dayCount'])
        dbRows[key] = dict(parameters[key].items() + newMultipliers[key].items() + \
                           weightedPopularity[key].items())

    return dbRows

####################################
# Main
####################################
##print "Testing..."

def main():
    api = WhatsNextApi()
    startDate = "2012-03-13 04:00:00"
    #date2 = "2012-04-01 00:00:00"

    startdt1 = datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
    dt1 = startdt1
    dt2 = dt1 + datetime.timedelta(days=1)

    nrDays = 120

    for n in range(nrDays):
        date1 = dt1.strftime("%Y-%m-%d %H:%M:%S")
        date2 = dt2.strftime("%Y-%m-%d %H:%M:%S")
        #print "======================================================="
        #print "Getting checkins of day %d..." % n
        checkins = api.getAllCheckinsBetweenDates(date1, date2)

        nrCheckins = len(checkins)
        if nrCheckins > 0:
            #print "\nGot %d checkins" % nrCheckins
            #print "First checkin: %s" % checkins[0].created_on
            #print "Last checkin: %s" % checkins[nrCheckins-1].created_on

            #### Call another function here to change what gets written to database
            spotMapping = buildSpotMapping(checkins)
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



    # TODO remove creationDateCalculation when done testing
    ##print "\nCalculated creation date %d times" % api.creationDateCalculation

    ##print "\nTerminating..."

main()
