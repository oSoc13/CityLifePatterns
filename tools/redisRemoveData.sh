#!/bin/bash
#This script converts the UserActions.list file to a CSV file.
#We didn't use it in the end because it would have been slower and to cumbersome
i=0
cat UserActions.list | while read line

do
   # do something with $line here
   i=$((i+1))

   cleanLine=$(sed -e 's/binary //' <<<$line)
   cleanLine=$(sed -e 's/ user_id/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ model_name/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_points/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ longitude/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ action_name/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ created_on/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_is_first/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ model_instance/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ latitude/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_type/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ id/,/' <<<$cleanLine)
   cleanLine=$(sed -e 's/ extra_spot_id/,/' <<<$cleanLine)

   echo $i
   echo $cleanLine >> UserActions.svg
done
#echo $keyContent > redisUserActionKeyValues.list
