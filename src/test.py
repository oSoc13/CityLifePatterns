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

api = WhatsNextApi()
api.goingToRun()
dayCheckins = api.getDayCheckins()
nrCheckins = len(dayCheckins)
print "nr day checkins %d" % nrCheckins

#print "printing..."
#for checkin in dayCheckins:
    #print checkin.created_on

if nrCheckins > 0:
    print "first checkin: %s" % dayCheckins[0].created_on
    print "last checkin: %s" % dayCheckins[len(dayCheckins)-1].created_on



print "Terminating..."



