#/bin/bash
i=0
cat checkInActions.list3 | while read line

do
   # do something with $line here
   i=$((i+1))
   cleanLine=$(sed -e 's/user_id/{user_id:/' <<< $line)
   cleanLine=$(sed -e 's/ points/, points:/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ created_on/, created_on:/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ is_first/, is_first:/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ id/, id:/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ type/, type:/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ spot_id/, spot_id: /' <<<$cleanLine)
   cleanLine=$(sed -e 's/$/  }/' <<< $cleanLine)
   #fix the date:
   # created_on: "2012 9 28 21 35 13"
   #to:
   # created_on: "2012-9-28 21:35:13"
   cleanLine=$(sed -e 's/created_on: "\([0-9]*\) \([0-9]*\) \([0-9]*\) \([0-9]*\) \([0-9]*\) \([0-9]*\)"/created_on: "\1-\2-\3 \4:\5:\6"/' <<< $cleanLine)
   #sed 's/\(..\)\(..\)\(..\)\(..\)\(..\)/\1-\2-\3-\4-\5/'



   #echo $i
   echo $cleanLine >> checkInActions.list4
done
#echo $keyContent > redisUserActionKeyValues.list
