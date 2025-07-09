#!/bin/bash -e

name=2025-05-21_complete_with_top_fps_final_analysis4
rm -rf ../runs/$name
mkdir -p ../runs/$name

date > ../runs/$name/date.txt

./clean.bash
./length_outliers.bash
./find_homologs.bash
./find_hits_different_folds.bash
./find_hits_different_sfs.bash
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
