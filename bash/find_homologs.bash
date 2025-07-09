#!/bin/bash -e

rm -rf ../tbls
rm -rf ../alns

mkdir -p ../tbls
mkdir -p ../alns

./find_fold_homologs.bash
./find_sf_homologs.bash
