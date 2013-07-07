#/bin/bash

# Get all redis UserActions
redis-cli smembers model._builtin.UserAction.all_items > redisKeys.list
