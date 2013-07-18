#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import datetime
import os.path
import json
import requests     # HTTP library
import config
###################################


# Use absolute path for file reading (otherwise Django won't find the files)
modulesDir = os.path.dirname(os.path.abspath(__file__))


class VikingSpotsApiWrapper:
    # This class is a wrapper for the VikingSpots API.
    # It can be used to easily execute VikingSpots API calls.
    ##################################################################
    token = ''        # Holds the token that will be used in API calls
    __urls = {}       # Holds the URLs for all used API calls


    # Constructor
    ##############################################################
    def __init__(self):
        self.token = config.token
        self.__urls = config.urls


    # API Calls
    ##############################################################
    # API CALL: Returns array of user actions sorted by created_on
    # nrActions: number of actions to return
    # skip:      skips the x last actions
    def getUserActions(self, nrActions, skip):    
        ''' # This code calls the VikingSpots Api, but we're using a local data set
        url = self.urls['userActionRequest']
        params = dict(
            bearer_token = self.token,
            max = nrActions,
            index = skip
        )
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        '''
        jsonFile = open(os.path.join(modulesDir, 'checkInActions.json'))
        jsonData = json.load(jsonFile)
        actionsJson = jsonData['response']['items']
        userActions = []
        for action in actionsJson:
            actionObject = UserAction(action)
            userActions.append(actionObject)
        # Sort actions by date (our local data set is not sorted by created_on)
        userActions.sort(key=lambda userAction: userAction.created_on)
        return userActions

    # Returns a Spot object
    def getSpotById(self, id):
        jsonData = self.__getSpotDataAsJson(id)
        if self.__isResponseOK(jsonData):
            spotJson = jsonData['response']            # spotJson = dict
            return Spot(spotJson)
        else:
            # print 'Error: %d code ' % jsonData['meta']['code']
            return None

    # Returns spot as JSON string
    def getSpotByIdJSON(self, spotId):
        jsonData = self.__getSpotDataAsJson(spotId)
        if self.__isResponseOK(jsonData):
            spotJSON = json.dumps(jsonData['response']) # spotJSON = string
            return spotJSON
        else:
            return None

    # Sends URL to VikingSpots API and returns response as json
    def __getSpotDataAsJson(self, spotId):
        url = self.__urls['spotByIdRequest']
        params = {'bearer_token': self.token, 'spot_id': spotId}
        resp = requests.get(url, params=params, verify=False)
        return resp.json()

    # Returns spot creation data as string
    # Uses another API call which includes spot creation date
    # TODO change getSpotDataAsJson  to use importSpotByIdRequest, then it already includes the spot creation date
    def getSpotCreationDate(self, spotId):
        url = self.__urls['importSpotByIdRequest']
        params = {'bearer_token': self.token, 'spot_id': spotId}
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        if 200 == jsonData['meta']['code']:
            creationDate = jsonData['response']['created_on'] # = str
            creationDate = addLeadingZerosToDate(creationDate)
            return creationDate
        else:
            print 'VikingSpotsApiWrapper:getSpotCreationDate: meta code=%s' % jsonData['meta']['code']
            return None


    # Helper Functions
    ##############################################################
    def __isResponseOK(self, jsonData):
        return 200 == jsonData['meta']['code']


# Supporting Data Classes
##################################################################
# Classes for VikingSpots API objects
# Class members names are identical to JSON field
# TODO Should probably be moved to separate file if list becomes larger
class UserAction():
    id = 0
    created_on = ''       # Creation date of checkin
    is_first = False
    points = 0
    type = ''
    user_id = 0
    spot_id = 0

    def __init__(self, json):
        self.id = json['id']
        self.created_on = addLeadingZerosToDate(json['created_on'])
        self.is_first = json['is_first']
        self.points = json['points']
        self.type = json['type']
        self.user_id = json['user_id']
        if 'spot_id' in json:
            self.spot_id = json['spot_id']

    def toStr(self):
        print 'id: %d' % self.id
        print 'created_on: %s' % self.created_on
        print 'points: %d' % self.points
        print 'type: %s' % self.type
        print 'user_id: %d' % self.user_id
        print 'spot_id: %d' % self.spot_id

# TODO Read more spot data info from JSON (update as needed)
class Spot():
    id = 0
    ll = [0.0,0.0]         # lat,long
    name = ''
    private = False
    json = {}

    def __init__(self, json):
        self.id = json['id']
        self.ll = [json['latitude'], json['longitude']]
        self.name = json['name']
        self.private = json['private']
        self.json = json

    def toStr(self):
        print 'name: %d' % self.name
        print 'id: %d' % self.id
        print 'll: %f,%f' % (self.ll[0], self.ll[1])
        print 'private: %s' % self.private


# Not all dates from local data set have leading zeros, this prevents date comparison as string
#   if '2013-2-1 00:00:00' < '2013:11:1 00:00:00'       = False
#   if '2013-02-01 00:00:00' < '2013:11:1 00:00:00'     = True
def addLeadingZerosToDate(date):
    dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return dt.strftime('%Y-%m-%d %H:%M:%S') # Adds leading zeros


