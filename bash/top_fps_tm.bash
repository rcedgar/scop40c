#!/bin/bash -e

MAXP=$1

if [ x$MAXP == x ] ; then
	echo $0: missing arg
	exit 1
fi

mkdir -p ../top_fps

python ../py/top_fps.py \
	--hits ../big_hits/tm.scop40 \
	--edf ../edf/scop40.tm \
	--maxprob $MAXP \
	| sort -gk1 \
	> ../top_fps/tm.$MAXP
