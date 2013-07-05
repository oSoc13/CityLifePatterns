#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# Testing class
#
###################################
import ApiWrapper
from ApiWrapper import *
import time                 # occurredInLast24Hours()
import datetime             # occurredInLast24Hours()
###################################


api = ApiWrapper()


####################################
# Functions   
####################################

def retrieveCheckinsFromActions(userActions):
    checkins = list()
    for action in userActions:
        if "Checkin" == action.type:    # TODO use correct VikingSpots type for user checkin
            checkins.append(action)
    return checkins

# created_on format: %Y-%m-%d %H:%M:%S
def occurredInLast24Hours(checkin):
    timeInSec = time.time()
    time24HoursAgo = timeInSec - 24 * 60 * 60
    timeStr = datetime.datetime.fromtimestamp(time24HoursAgo).strftime('%Y-%m-%d %H:%M:%S')
    if timeStr < checkin.created_on:
        return True
    return False

# Timespan specifies how far back the user actions go
# E.g. timespan = 24 returns user actions made in the last 24 hours
# TODO: Function retrieves a set, limited amount of user actions for now,
#       should keep asking for more data until actions go further back 
#       than the given timespan.
def getDayCheckins():
    userActions = api.getUserActions(20)
    checkins = retrieveCheckinsFromActions(userActions)
    dayCheckins = list()
    for checkin in checkins:
        if occurredInLast24Hours(checkin):
            dayCheckins.append(checkin)
    return dayCheckins



####################################
# Test Code   
####################################

print "Testing..."

checkins = getDayCheckins()

spotIds = list()
for action in checkins:
    spotIds.append(action.spot_id)



print "Terminating..."



