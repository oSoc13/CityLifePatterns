#!/user/bin/python
import sys
sys.path.insert(0, 'core')

import DBQuery

def write( spotMapping ):
    DBQuery.openConnection()
    i = 0
    for tuple in spotMapping:
        if i % 1000 == 0:
            print "Writing tuple.. %d" % i
        i += 1
        value=spotMapping[tuple]

        SELECT='SELECT count, COUNT( * ) AS  "Exists" FROM nextSpotCount WHERE  spotId = %s AND nextSpotId = %s' % (tuple[0],tuple[1])
        EXISTArray = DBQuery.queryDBSingleResponse( SELECT )
        if EXISTArray[1] == 1:
            totalCount = EXISTArray[0] + value
            QUERY="UPDATE nextSpotCount SET  count = '%s' WHERE spotId=%s AND nextSpotId=%s;" % (totalCount, tuple[0], tuple[1])
            print "Updated existing row (%d,%d)" % (tuple[0], tuple[1])
        else:
            QUERY= "INSERT INTO nextSpotCount VALUES (NULL ,  '%s',  '%s',  '%s');" % (tuple[0],tuple[1],value)
        returnedStuff = DBQuery.writeDB( QUERY )
        #print returnedStuff

        #print "spotID: %s | nextID: %s | count: %s " % (tuple[0], tuple[1], value)
    DBQuery.closeConnection()
    #print "ending..."


def writeToDbNew(rows):
    DBQuery.openConnection()
    for (spotId, nextSpotId) in rows:
        key = (spotId, nextSpotId)
        values = rows[key]
        dayCount = values['dayCount']
        spotCreationDate = values['spotCreationDate']
        lastOccurrence = values['lastOccurrence']
        variance = values['variance']
        averageTimeSpent = values['averageTimeSpent']
        MspotAge = values['MspotAge']
        MtimeSpent = values['MtimeSpent']
        weightedPopularity = values['weightedPopularity']

        SELECT = "SELECT totalCount, COUNT(*) AS 'Exists' " \
                 "FROM whatsnext WHERE spotId = '%s' AND nextSpotId = '%s';" % (spotId, nextSpotId)

        
        EXISTArray = DBQuery.queryDBSingleResponse(SELECT)
        dbCount = EXISTArray[0]
        exists = EXISTArray[1]
        if exists:
            totalCount = int(dbCount) + dayCount
            print "%s = %s + %s" % (totalCount, dbCount, dayCount)
            QUERY = "UPDATE whatsnext " \
                    "SET totalCount = '%s', spotCreationDate = '%s', lastOccurrence = '%s', " \
                    "variance = '%s', averageTimeSpent = '%s', " \
                    "MspotAge = '%s', MtimeSpent = '%s', weightedPopularity = '%s' " \
                    "WHERE spotId = '%s' AND nextSpotId = '%s';" % \
                        (totalCount, spotCreationDate, lastOccurrence, variance, averageTimeSpent,
                         MspotAge, MtimeSpent, weightedPopularity,
                         spotId, nextSpotId)
        else:
            QUERY = "INSERT INTO whatsnext " \
                    "VALUES (NULL,  '%s',  '%s', '%s',  '%s', '%s', '%s', " \
                    "'%s', '%s', '%s', '%s');" %  (spotId, nextSpotId, 
                         dayCount, spotCreationDate, lastOccurrence,
                         variance, averageTimeSpent, 
                         MspotAge, MtimeSpent, weightedPopularity)
        DBQuery.writeDB(QUERY)
    DBQuery.closeConnection()
