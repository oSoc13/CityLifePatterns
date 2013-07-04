#!/usr/bin/python

# Author: Linsey Raymaekers
# Copyright OKFN Belgium

# Testing ApiWrapepr class

import ApiWrapper

print "Testing..."

api = ApiWrapper.ApiWrapper()

userActions = api.getUserActions()
print userActions[0]

userAction = ApiWrapper.UserAction("1", 1, True, 200, "UserRegistered", 1000489)
print userAction.type

