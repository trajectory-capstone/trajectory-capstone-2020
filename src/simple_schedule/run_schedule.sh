#!/bin/sh
filename=$1
rm -rf sample_sch.csv
op="output-metric_"
metric=$2
sep="_"
while IFS= read -r line; do
echo "test"
sample=$(echo $line | cut -d " " -f2)
dir_name=$(echo $line | cut -d " " -f1)
echo "$line" >> sample_sch.csv
./main
mkdir -p ./outputs/$dir_name/$metric/
mv  $op$metric outputs/$dir_name/$metric/$op$metric$sep$sample
rm -rf sample_sch.csv
done < $filename
