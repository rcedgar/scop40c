#!/bin/bash -e

for sf in `cat ../data/sfs.txt`
do
	./build_hmm_and_search.bash $sf
done
