#!/bin/bash -e

for x in `cat ../data/folds.txt`
do
	./build_hmm_and_search.bash $x
done
