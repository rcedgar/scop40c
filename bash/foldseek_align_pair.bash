#!/bin/bash

pdb1=$1
pdb2=$2
tsv=$3

if [ x$tsv == x ] ; then
	echo Missing arg
	exit 1
fi

tmpdir=/tmp/foldseek$RANDOM
mkdir -p $tmpdir

foldseek-v10 \
	easy-search \
	$pdb1 \
	$pdb2 \
	$tsv \
	$tmpdir \
	--exhaustive-search 1 \
	-e 9e9

ls -lh $tsv

rm -rf $tmpdir
