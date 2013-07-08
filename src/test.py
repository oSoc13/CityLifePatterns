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
###################################



####################################
# Test Code   
####################################
print "Testing..."

api = WhatsNextApi()
#api.writeLastRun()
dayCheckins = api.getDayCheckins()

print "printing..."
for checkin in dayCheckins:
    #checkin.toStr()
    print checkin.created_on


print "Terminating..."



