#!/bin/bash
# sky_scan.sh
### use command line arguments to pick the correct range of sources

echo "Arguments: $1"

python /home/iwsatlas1/kuhlmann/icecube/p_value/sky_scan/sky_scan.py $1
