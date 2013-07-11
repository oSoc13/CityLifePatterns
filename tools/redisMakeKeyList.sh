#/bin/bash
redis-cli smembers model._builtin.UserAction.all_items > redisKeys.list
