#!/bin/bash -e

MAXP=$1

if [ x$MAXP == x ] ; then
	echo $0: missing arg
	exit 1
fi

mkdir -p ../top_fps

python ../py/top_fps.py \
	--hits ../big_hits/foldseek.scop40 \
	--edf ../edf/scop40.foldseek \
	--maxprob $MAXP \
	--evalues \
	| sort -gk1 \
	> ../top_fps/foldseek.$MAXP
