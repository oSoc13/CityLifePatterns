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
    urls = dict()



    # Constructor
    def __init__(self):
        # Read token from file
        file = open("vikingtoken")
        fileContents = file.read()
        entries = fileContents.split("=")
        self.token = entries[1]

        # Read urls from file
        file = open("urls")
        lines = file.readlines()
        for line in lines:
            if (line.endswith("\n")):
                line = line[:-2]
            pair = line.split("=")
            key = pair[0]
            value = pair[1]
            self.urls[key] = value


    # Returns array of user actions
    def getUserActions(self):
        url = self.urls["userActionRequest"]
        params = dict(
            bearer_token = self.token,
            max = 5
        )
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        userActions = jsonData["response"]["items"]
        return userActions


    # Gets spot info 
    def getSpotById(self, id):
        url = self.urls["spotByIdRequest"]


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
        
