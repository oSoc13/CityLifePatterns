#/bin/bash
i=0
cat redisKeys.list | while read line

do
   # do something with $line here
   i=$((i+1))
   key=$line
   #echo redis-cli hgetall model._builtin.UserAction.item.$key
   keyContent=$(redis-cli hgetall model._builtin.UserAction.item.$key)
   echo $i
   echo $keyContent >> redisUserActionKeyValues.list
done
#echo $keyContent > redisUserActionKeyValues.list
