#!/bin/bash
#this script gets all user actions and dumps their keys in a list
redis-cli smembers model._builtin.UserAction.all_items > redisKeys.list
