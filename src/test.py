#!/usr/bin/python

# Author: Linsey Raymaekers
# Copyright OKFN Belgium

# Testing ApiWrapepr class

import ApiWrapper
from ApiWrapper import *

print "Testing..."

api = ApiWrapper()


'''
userActions = api.getUserActions()
print userActions[0]

userAction = UserAction("1", 1, True, 200, "UserRegistered", 1000489)
print userAction.created_on
print userAction.id
print userAction.is_first
print userAction.points
print userAction.type
print userAction.user_id
'''

api.getSpotById(382)

