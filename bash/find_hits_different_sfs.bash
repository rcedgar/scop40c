#!/bin/bash -e

cd ../tbls
mkdir -p ../results

python ../py/find_hits_different_sfs.py \
	sf \
	`cat ../data/sfs.txt` \
	| sort -gk1 \
	> ../results/hits_different_sfs.tsv

head ../results/hits_different_sfs.tsv
ls -lh ../results/hits_different_sfs.tsv
