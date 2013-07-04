#!/usr/bin/python
# -*- coding: utf-8 -*-
import DBQuery

def getAllCountedSpots():
    returnedResults = DBQuery.queryDB( "SELECT DISTINCT spotId FROM nextSpotCount" )
    allTheCountedSpotsArray = []
    
    for row in returnedResults:
                allTheCountedSpotsArray.append(row[0])
    return allTheCountedSpotsArray


def getNextSpots( spotId ):
    queryString = "SELECT nextSpotId, count FROM nextSpotCount WHERE spotId = %s ORDER BY count DESC LIMIT 0, 5" % spotId
    returnedResults = DBQuery.queryDB( queryString )
    spotArray = [ spotId ]
    
    for row in returnedResults:
                spotArray.append(row[0])
    return spotArray
    

def mostCheckedNextSpotList( nextSpotsArray ):

    queryString = "INSERT INTO  nextSpots VALUES ( '%s', '%s',  '%s',  '%s',  '%s',  '%s' );" % (nextSpotsArray[0], nextSpotsArray[1], nextSpotsArray[2],  nextSpotsArray[3], nextSpotsArray[4], nextSpotsArray[5])
    
    returnedResults = DBQuery.writeDB( queryString )
    return returnedResults
