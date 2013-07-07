#/bin/bash

#For each redis key (=line in redisKeys.list)
i=0
cat redisKeys.list | while read line

do
   
   i=$((i+1)) #increment counter
   key=$line #get the keynumber
   keyContent=$(redis-cli hgetall model._builtin.UserAction.item.$key) #get the key value and store as variable
   echo $i #print the counter
   echo $keyContent >>UserActions.list #add the keycontent to a file
done
