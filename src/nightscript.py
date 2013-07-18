#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# This is the night script that is responsible for updating the WhatsNext database on a daily basis.
# It reads the date the script was last run from the file 'lastrun' and processes all checkins  up to
# 24 hours after this date.
#
# The length of time spanned by the processing can be passed to the main function.
#
# The file 'lastrun' is expected to be in same directory as this file.
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import writeToDb
import DatabaseBuilder
from DatabaseBuilder import *
import os.path
import time                
import datetime             
import calendar
###################################

baseDir = os.path.dirname(os.path.abspath(__file__))
dbBuilder = DatabaseBuilder()
# Main
###################################################################
def main():
    nightScriptStart()
    print '\nLast run: %s' % dbBuilder.lastRun
    print 'End of current run: %s' % dbBuilder.endOfCurrentRun
    print '\nGetting day checkins...'
    dayCheckins = dbBuilder.getDayCheckins()
    nrCheckins = len(dayCheckins)

    if nrCheckins > 0:
        print '\nGot %d day checkins' % nrCheckins
        print 'First checkin:  %s' % dayCheckins[0].created_on
        print 'Last checkin: %s' % dayCheckins[nrCheckins-1].created_on
        spotMapping = dbBuilder.buildSpotMapping(dayCheckins)
        if len(spotMapping) > 0:
            print '\n%d spot mappings found' % len(spotMapping)
            print '\nWriting to DB...'
            writeToDb.writeToDbNew(spotMapping)
            print 'Done writing to DB!'
        else:
            print '\nNo spot mappings found today.'
    else:
        print '\nThere were no checkins today'
    nightScriptEnd()



# Helper Functions
###################################################################
# Write current time to file 'lastrun' and
# TODO should check for proper format in 'lastrun' file - error handling
def nightScriptStart():
    initializeStartAndEndTimes()
    writeLastRunToFile()

# Reads date of last run and calculates end of current run (= 24 hours ahead)
def initializeStartAndEndTimes():
    filepath = os.path.join(baseDir, 'lastrun')
    if os.path.exists(filepath):
        file = open(filepath)
        fileContents = file.read()
        entries = fileContents.split(': ')
        lastRun = entries[1]
        if (lastRun.endswith('\n')):
            lastRun = lastRun[:-1]

        # Calculate end of current run
        date = datetime.datetime.strptime(lastRun, '%Y-%m-%d %H:%M:%S')
        endDate = date + datetime.timedelta(days=1)
        endOfCurrentRun = endDate.strftime('%Y-%m-%d %H:%M:%S')

        dbBuilder.lastRun = lastRun
        dbBuilder.endOfCurrentRun = endOfCurrentRun
    else:
        print 'No file \'lastrun\' found.'

# Updates 'lastrun' file with end of current run
def writeLastRunToFile():
    filepath = os.path.join(baseDir, 'lastrun')
    file = open(filepath, 'w')
    contents = 'Night script was last run on: ' + dbBuilder.endOfCurrentRun
    file.write(contents)

# TODO Write away info about this run as necessary
def nightScriptEnd():
    print '\nTerminating...'
    return


main()

