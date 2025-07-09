#!/bin/bash -e

name=2025-05-22_final_analysis4_with_length_only
rm -rf ../runs/$name
mkdir -p ../runs/$name

date > ../runs/$name/date.txt

./parameter_sweep.bash

for x in \
	final_analysis4 \
	graphs \
	length_outliers \
	results \
	short_domains \
	top_fps
do
	cp -vr ../$x ../runs/$name
done

date >> ../runs/$name/date.txt

ls -lh ../runs/$name
