#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# Testing class
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import WhatsNextApi
from WhatsNextApi import *
import VikingSpotsApiWrapper
from VikingSpotsApiWrapper import *
from writeToDb import *
import time                
import datetime
import calendar
###################################

api = WhatsNextApi()
####################################
# Test Code   
####################################
print "Testing..."

json = api.getPopularNextSpotsJSON(7, 10, '2dad11c572f4ba859608519ff3f3e4de0a6d45e5')
print json

print "\nTerminating..."


