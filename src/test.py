#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# Testing class
#
###################################
import WhatsNextApi
from WhatsNextApi import *
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
###################################



####################################
# Test Code   
####################################
print "Testing..."

'''
api = WhatsNextApi()
#api.writeLastRun()
dayCheckins = api.getDayCheckins()
print "nr day checkins %d" % len(dayCheckins)

print "printing..."
for checkin in dayCheckins:
    print checkin.created_on
'''
api = VikingSpotsApiWrapper()
checkins = api.getUserActions(0,0)
print checkins[0].created_on




print "Terminating..."



