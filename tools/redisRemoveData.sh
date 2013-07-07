#/bin/bash
i=0
cat UserActions.list | while read line

do
   # for each UserAction, remove the variable name and change to ','
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

   echo $i  #print the counter
   echo $cleanLine >> UserActions.csv #add the "clean" csv style line to file
done
#echo $keyContent > redisUserActionKeyValues.list
