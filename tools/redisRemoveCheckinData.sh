#!/bin/bash
#This script clears out the parts that aren't returned by the CityLife API and converts the names of some atributes to those present by the API
i=0
cat checkInActions.list | while read line

do
   # do something with $line here
   i=$((i+1))

   cleanLine=$(sed -e 's/binary false//' <<<$line)
   cleanLine=$(sed -e 's/binary true//' <<<$cleanLine)
   cleanLine=$(sed -e 's/ model_name "vikingspots.Spot"//' <<< $cleanLine)
   cleanLine=$(sed -e 's/ extra_points/ points/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ longitude 0//' <<<$cleanLine)
   cleanLine=$(sed -e 's/ action_name "CheckIn"//' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_is_first/ is_first/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ model_instance\ [0-9]*//' <<<$cleanLine)
   cleanLine=$(sed -e 's/ latitude 0//' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_type/ type/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_spot_id/ spot_id/' <<<$cleanLine)

   echo $i
   echo $cleanLine >> checkInActions.list2
done
#echo $keyContent > redisUserActionKeyValues.list
