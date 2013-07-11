#!/bin/bash
#This scripts makes sure the json becomes valid by adding " before and after the atributes

i=0
cat checkInActions.json | while read line

do
   # do something with $line here
   i=$((i+1))
   cleanLine=$(sed -e 's/count/"count"/g' <<< $line)
   cleanLine=$(sed -e 's/ index/ "index"/g' <<< $cleanLine)
   cleanLine=$(sed -e 's/ items/ "items"/g' <<< $cleanLine)
   cleanLine=$(sed -e 's/user_id/"user_id"/g' <<< $cleanLine)
   cleanLine=$(sed -e 's/points/"points"/g' <<<$cleanLine)
   cleanLine=$(sed -e 's/created_on/"created_on"/g' <<<$cleanLine)
   cleanLine=$(sed -e 's/is_first/"is_first"/g' <<<$cleanLine)
   cleanLine=$(sed -e 's/ id/ "id"/g' <<<$cleanLine)
   cleanLine=$(sed -e 's/type/"type"/g' <<<$cleanLine)
   cleanLine=$(sed -e 's/spot_id/"spot_id"/g' <<<$cleanLine)
   #fix the date:
   # created_on: "2012 9 28 21 35 13"
   #to:
   # created_on: "2012-9-28 21:35:13"
   #cleanLine=$(sed -e 's/created_on: "\([0-9]*\) \([0-9]*\) \([0-9]*\) \([0-9]*\) \([0-9]*\) \([0-9]*\)"/created_on: "\1-\2-\3 \4:\5:\6"/' <<< $cleanLine)
   #sed 's/\(..\)\(..\)\(..\)\(..\)\(..\)/\1-\2-\3-\4-\5/'



   #echo $i
   echo $cleanLine > checkInActions2.json
done
#echo $keyContent > redisUserActionKeyValues.list
