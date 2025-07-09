#!/bin/bash -e

cd ../tbls
mkdir -p ../results

python ../py/find_hits_different_sfs.py \
	fold \
	`cat ../data/folds.txt` \
	| sort -gk1 \
	> ../results/hits_different_folds.tsv

head ../results/hits_different_folds.tsv
ls -lh ../results/hits_different_folds.tsv
