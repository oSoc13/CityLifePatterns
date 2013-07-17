#!/usr/bin/python
#
# Author: Linsey Raymaekers
# Copyright OKFN Belgium
# 
###################################
import json
import requests     # HTTP library
import datetime
import os.path
###################################


# Use absolute path for file reading (otherwise Django won't find the files)
modulesDir = os.path.dirname(os.path.abspath(__file__))


class VikingSpotsApiWrapper:
    # This class is a wrapper for the VikingSpots API.
    # It can be used to easily execute VikingSpots API calls.
    ##################################################################
    __token = ''      # Holds the token that will be used in API calls
    __urls = {}       # Holds the URL for all used API calls


    # Constructor
    ##############################################################
    def __init__(self):
        self.__readTokenFromFile()
        self.__readUrlsFromFile()

    def __readTokenFromFile(self):
        file = open(os.path.join(modulesDir, 'vikingtoken'))
        fileContents = file.read()
        entries = fileContents.split('=')
        self.__token = self.__removeNewLine(entries[1])

    def __readUrlsFromFile(self):
        file = open(os.path.join(modulesDir, 'urls'))
        lines = file.readlines()
        for line in lines:
            line = self.__removeNewLine(line)
            pair = line.split('=')
            key = pair[0]
            value = pair[1]
            self.__urls[key] = value

    def __removeNewLine(self, str):
        if str.endswith('\n'):
            return str[:-1]


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
        userActions = list()
        for action in actionsJson:
            actionObject = UserAction(action)
            actionObject.__created_on = self.__addLeadingZerosToDate(actionObject.__created_on)
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
        params = {'bearer_token': self.__token, 'spot_id': spotId}
        resp = requests.get(url, params=params, verify=False)
        return resp.json()

    # Returns spot creation data as string
    # Uses another API call which includes spot creation date
    # TODO getSpotDataAsJson should be changed to use importSpotByIdRequest,
    # then it already includes the spot creation date
    def getSpotCreationDate(self, spotId):
        url = self.__urls['importSpotByIdRequest']
        params = {'bearer_token': self.__token, 'spot_id': spotId}
        resp = requests.get(url, params=params, verify=False)
        jsonData = resp.json()
        if 200 == jsonData['meta']['code']:
            return jsonData['response']['created_on']
        else:
            print 'VikingSpotsApiWrapper:getSpotCreationDate: meta code=%s' % jsonData['meta']['code']


    # Helper Functions
    ##############################################################
    # Not all dates from local data set have leading zeros, this prevents date comparison as string
    #   if '2013-2-1 00:00:00' < '2013:11:1 00:00:00'       = False
    #   if '2013-02-01 00:00:00' < '2013:11:1 00:00:00'     = True
    def __addLeadingZerosToDate(self, date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d %H:%M:%S') # Adds leading zeros

    def __isResponseOK(self, jsonData):
        return 200 == jsonData['meta']['code']


# Supporting Data Classes
##################################################################
# Classes for VikingSpots API objects
# Class members names are identical to JSON field
# TODO Should probably be moved to separate file if list becomes larger
class UserAction():
    __id = 0
    __created_on = ''
    __is_first = False
    __points = 0
    __type = ''
    __user_id = 0
    __spot_id = 0

    def __init__(self, json):
        self.__id = json['id']
        self.__created_on = json['created_on']
        self.__is_first = json['is_first']
        self.__points = json['points']
        self.__type = json['type']
        self.__user_id = json['user_id']
        if 'spot_id' in json:
            self.__spot_id = json['spot_id']

    def toStr(self):
        print 'id: %d' % self.__id
        print 'created_on: %s' % self.__created_on
        print 'points: %d' % self.__points
        print 'type: %s' % self.__type
        print 'user_id: %d' % self.__user_id
        print 'spot_id: %d' % self.__spot_id
        

# TODO Read more spot data info from JSON (update as needed)
class Spot():
    __id = 0
    __ll = [0.0,0.0]         # lat,long
    __name = ''
    __private = False
    __json = {}
    __creationDate = ''

    def __init__(self, json):
        self.__id = json['id']
        self.__ll = [json['latitude'], json['longitude']]
        self.__name = json['name']
        self.__private = json['private']
        self.__json = json

    def toStr(self):
        print 'name: %d' % self.__name
        print 'id: %d' % self.__id
        print 'll: %f,%f' % (self.__ll[0], self.__ll[1])
        print 'private: %s' % self.__private

