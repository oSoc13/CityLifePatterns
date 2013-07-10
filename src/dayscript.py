#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
#
# This is the day script that uses nextSpot data from the database to advise probable next spots.
#
###################################
import sys
sys.path.insert(0, './modules')    # Specify additional directory to load python modules from
import WhatsNextApi
from WhatsNextApi import *
###################################


## Main #######################################
api = WhatsNextApi()


print "\nTerminating..."
###################################################################
