
#!/user/bin/python
import sys
sys.path.insert(0, 'core')

import DBQuery

def write( spotMapping ):

    DBQuery.openConnection()
    i = 0
    for tuple in spotMapping:
        if i % 100 == 0:
            print "Writing tuple %d..." % i
        i += 1
        value=spotMapping[tuple]

        SELECT='SELECT count, COUNT( * ) AS  "Exists" FROM nextSpotCount WHERE  spotId = %s AND nextSpotId = %s' % (tuple[0],tuple[1])
        EXISTArray = DBQuery.queryDBSingleResponse( SELECT )
        if EXISTArray[1] == 1:
            totalCount = EXISTArray[0] + value
            QUERY="UPDATE nextSpotCount SET  count = '%s' WHERE spotId=%s AND nextSpotId=%s;" % (totalCount, tuple[0], tuple[1])
        else:
            QUERY= "INSERT INTO nextSpotCount VALUES (NULL ,  '%s',  '%s',  '%s');" % (tuple[0],tuple[1],value)
        returnedStuff = DBQuery.writeDB( QUERY )
        #print returnedStuff

        #print "spotID: %s | nextID: %s | count: %s " % (tuple[0], tuple[1], value)
    DBQuery.closeConnection()
    #print "ending..."
