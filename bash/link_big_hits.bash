#!/bin/bash -e

mkdir -p ../big_hits
cd ../big_hits

for algo in dali tm foldseek reseek
do
	ln -vs $src/null_model/big_hits/$algo.scop40 .
done
