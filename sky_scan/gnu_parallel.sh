#!/bin/bash
### Bash wrapper using parallel for running sky scans in parallel

NUM_OF_FILES=`ls -d $PWD/input_configs/* | wc -l`
#NUM_OF_FILES=1
echo $NUM_OF_FILES
for ((i=616; i<$NUM_OF_FILES; i++)); do echo $i; done | parallel --delay 2.5 --results parallel_job/ --joblog gnu.log -j64  nice -n 17 ./sky_scan.sh 


# change results thing with replaced separator s.t. only the job number will be used to create the log directories
