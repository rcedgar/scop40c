#!/bin/bash -e

rm -rf ../length_outliers
mkdir -p ../length_outliers

python ../py/length_outliers.py \
	> ../length_outliers/length_outliers.tsv
