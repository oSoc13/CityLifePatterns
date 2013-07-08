#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import json
import requests     # HTTP library

import os.path
BASE = os.path.dirname(os.path.abspath(__file__))
###################################

# This class is a wrapper for the VikingSpots API.
class VikingSpotsApiWrapper:
    name = "Mobile Vikings API Wrapper"
    token = ""
    urls = dict()


    # Constructor
    def __init__(self):
        # Read token from file
        # file = open("vikingtoken") Doesn't work with Django, use os.path
        file = open(os.path.join(BASE, "vikingtoken"))
        fileContents = file.read()
        entries = fileContents.split("=")
        self.token = entries[1]

        # Read urls from file
        # file = open("urls") Doesn't work with Django, use os.path
        file = open(os.path.join(BASE, "urls"))
        lines = file.readlines()
        for line in lines:
            if (line.endswith("\n")):
                line = line[:-2]
            pair = line.split("=")
            key = pair[0]
            value = pair[1]
            self.urls[key] = value



    # Returns array of user actions
    # nrActions: number of actions to return
    # skip:      skips the x last actions
    def getUserActions(self, nrActions, skip):    
        url = self.urls["userActionRequest"]
        params = dict(
            bearer_token = self.token,
            max = nrActions,
            index = skip
        )
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        actionsJson = jsonData["response"]["items"]
        userActions = list()
        for action in actionsJson:
            userActions.append(UserAction(action))
        return userActions


    # Gets spot info 
    def getSpotById(self, id):
        url = self.urls["spotByIdRequest"]
        params = dict(
                bearer_token = self.token,
                spot_id = id
        )
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        spotJson = jsonData["response"]
        return Spot(spotJson)


####################################
# Data Classes 
####################################

class UserAction():
    id = 0
    created_on = ""
    is_first = False
    points = 0
    type = ""
    user_id = 0
    spot_id = 0

    def __init__(self, json):
        self.id = json["id"]
        self.created_on = json["created_on"]
        self.is_first = json["is_first"]
        self.points = json["points"]
        self.type = json["type"]
        self.user_id = json["user_id"]
        if "spot_id" in json:
            self.spot_id = json["spot_id"]

    def toStr(self):
        print "id: %d" % self.id
        print "created_on: %s" % self.created_on
        print "points: %d" % self.points
        print "type: %s" % self.type
        print "user_id: %d" % self.user_id
        print "spot_id: %d" % self.spot_id
        

# TODO Read more spot data info from JSON (update as needed)
class Spot():
    id = 0
    ll = [0.0,0.0]         # lat,long
    name = ""
    private = False

    def __init__(self, json):
        self.id = json["id"]
        self.ll = [json["latitude"], json["longitude"]]
        self.name = json["name"]
        self.private = json["private"]  

