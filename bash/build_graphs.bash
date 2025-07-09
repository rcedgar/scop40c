#!/bin/bash -e

MAXE=$1

if [ x$MAXE == x ] ; then
	echo $0: Missing arg
	exit 1
fi

mkdir -p ../graphs

echo === SF ===
python ../py/build_graph.py sf $MAXE \
	../graphs/graph_sf.$MAXE.txt \
	../graphs/hmm_excludes_sf.$MAXE.txt

echo
echo === Fold ===
python ../py/build_graph.py fold $MAXE \
	../graphs/graph_fold.$MAXE.txt \
	../graphs/hmm_excludes_fold.$MAXE.txt
