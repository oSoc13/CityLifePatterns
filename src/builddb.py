#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# This script fills the database with spotmappings based on certain weights
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
lastRun = "2012-01-01 00:00:00"  
endOfCurrentRun = "2014-01-01 00:00:00"

## Parameters #################################

    

## Main #######################################

print "\nGetting checkins..."
checkins = api.getAllCheckinsBeforeDate(endOfCurrentRun)
nrCheckins = len(checkins)

if nrCheckins > 0:
    print "\nGot %d checkins" % nrCheckins
    print "First checkin: %s" % checkins[0].created_on
    print "Last checkin: %s" % checkins[nrCheckins-1].created_on

    spotMapping = api.buildSpotMapping(checkins)
    if len(spotMapping) > 0:
        print "\n%d spot mappings found" % len(spotMapping)
        print "\nWriting to DB..."
        writeToDb.write(spotMapping)
        print "Done writing to DB!" 
    else:
        print "\nNo spot mappings found today."
else:
    print "\nThere were no checkins today"

print "Terminating..."
###################################################################


