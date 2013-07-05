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
###################################




####################################
# Functions   
####################################

def retrieveCheckins(userActions):
    checkins = list()
    for action in userActions:
        if "Checkin" == action.type:    # TODO use correct VikingSpots type for user checkin
            checkins.append(action)
    return checkins




####################################
# Test Code   
####################################

print "Testing..."

api = ApiWrapper()

userActions = api.getUserActions(5)
checkins = retrieveCheckins(userActions)

print "checkins length = %d" % len(checkins)

spotIds = list()
for action in checkins:
    spotIds.append(action.spot_id)



print "Terminating..."



