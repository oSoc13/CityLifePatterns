#!/usr/bin/python

# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
# This class is a wrapper for the VikingSpots API.
#

import json
import requests     # HTTP library

class ApiWrapper:
    name = "Mobile Vikings API Wrapper"
    token = ""
    userActionRequest = "https://alpha.vikingspots.com/en/api/4/users/actions/"


    # Constructor
    def __init__(self):
        file = open("vikingtoken")
        fileContents = file.read()
        entries = fileContents.split("=")
        self.token = entries[1]


    # Returns array of user actions
    def getUserActions(self):
        url = self.userActionRequest
        params = dict(
            bearer_token = self.token,
            max = 5
        )
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        userActions = jsonData["response"]["items"]
        return userActions


class UserAction():
    created_on = ""
    id = 0
    is_first = False
    points = 0
    type = ""
    used_id = 0

    def __init__(self, created_on, id, is_first, points, type, user_id):
        self.created_on = created_on
        self.id = id
        self.is_first = is_first
        self.points = points
        self.type = type
        self.user_id = user_id
        
