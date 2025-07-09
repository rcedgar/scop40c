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
