#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# This is the night script that is responsible for updating the WhatsNext database.
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import writeToDb
import WhatsNextApi
from WhatsNextApi import *
import os.path
import time                
import datetime             
import calendar
###################################

baseDir = os.path.dirname(os.path.abspath(__file__))
api = WhatsNextApi()
lastRun = ""            # End of last run (date)
endOfCurrentRun = ""

## Helper functions ###########################
# Builds a local cache of spot mappings
def processCheckins(dayCheckins):
    print "\nProcessing checkins..."
    spotIds = []
    nextSpotIds = []
    spotMapping = {}
    i = 0   # Used to select checkins after current checkin
    for checkin in dayCheckins:
        nextCheckin = api.findNextCheckin(checkin.user_id, dayCheckins[i+1::])
        if nextCheckin is not None:
            spotId = checkin.spot_id
            nextSpotId = nextCheckin.spot_id
            if (spotId, nextSpotId) in spotMapping:
                spotMapping[(spotId, nextSpotId)] += 1
                print "Mapping inc: (%d,%d)" % (spotId, nextSpotId)
            else:
                spotMapping[(spotId, nextSpotId)] = 1
                print "New mapping: (%d,%d)" % (spotId, nextSpotId)
        i += 1
    print "Done processing!"
    return spotMapping
  
# Write current time to file 'lastrun'
def nightScriptStart():
    global lastRun
    global endOfCurrentRun
    filepath = os.path.join(baseDir, "lastrun") 
    if os.path.exists(filepath):
        file = open(filepath)
        fileContents = file.read()
        entries = fileContents.split(": ")
        lastRun = entries[1]
        if (lastRun.endswith("\n")):
            lastRun = lastRun[:-1]
        date = datetime.datetime.strptime(lastRun, '%Y-%m-%d %H:%M:%S')
        endDate = date + datetime.timedelta(days=1)
        endOfCurrentRun = endDate.strftime("%Y-%m-%d %H:%M:%S")
        api.lastRun = lastRun
        api.endOfCurrentRun = endOfCurrentRun
    else:
        print "First run, will retrieve all checkin data..."
    filepath = os.path.join(baseDir, "lastrun")
    file = open(filepath, 'w')
    contents = 'Night script was last run on: ' + api.endOfCurrentRun
    file.write(contents)


# Write away info about this run if necessary
def nightScriptEnd():
    return

## Main #######################################
nightScriptStart()

print "\nLast run: %s" % lastRun
print "End of current run: %s" % endOfCurrentRun

print "\nGetting day checkins..."
dayCheckins = api.getDayCheckins()
nrCheckins = len(dayCheckins)

if nrCheckins > 0:
    print "\nGot %d day checkins" % nrCheckins
    print "First checkin:  %s" % dayCheckins[0].created_on
    print "Last checkin: %s" % dayCheckins[nrCheckins-1].created_on
    spotMapping = processCheckins(dayCheckins)
    if len(spotMapping) > 0:
        print "\n%d spot mappings found" % len(spotMapping)
        print "\nWriting to DB..."
        writeToDb.write(spotMapping)
        print "Done writing to DB!" 
    else:
        print "\nNo spot mappings found today."
else:
    print "\nThere were no checkins today"

nightScriptEnd()
print "\nTerminating..."
###################################################################


