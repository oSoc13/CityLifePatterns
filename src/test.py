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
checkins = api.getDayCheckins()
print len(checkins)

spotIds = list()
for action in checkins:
    spotIds.append(action.spot_id)



print "Terminating..."



