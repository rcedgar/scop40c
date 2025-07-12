#!/bin/bash -e

MAXE=$1
MAXP=$2

if [ x$MAXP == x ] ; then
	echo $0: missing arg
	exit 1
fi

mkdir -p ../final_analysis4
cd ../final_analysis4

python ../py/final_analysis4.py \
	final_analysis4.MAXE$MAXE.MAXP$MAXP.txt \
	curated.lookup4.MAXE$MAXE.MAXP$MAXP \
	$MAXE \
	$MAXP

mkdir -p ../final_analysis
rm -f ../final_analysis/scop40c.lookup

ln -s curated.lookup4.MAXE1e-4.MAXP1e-6 ../final_analysis/scop40c.lookup
