#!/bin/bash -e

name=2025-05-18_find_sf_homologs_and_short_domains
rm -rf ../runs/$name
mkdir -p ../runs/$name

date > ../runs/$name/date.txt

./clean.bash
./length_outliers.bash
./find_homologs.bash
./find_hits_different_folds.bash
./find_hits_different_sfs.bash
./build_graphs.bash

cp -v ../results/* ../runs/$name

date >> ../runs/$name/date.txt

ls -lh ../runs/$name
cat ../runs/$name/date.txt
