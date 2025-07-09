#!/bin/bash -e

mkdir -p ../pdb

pdb=$1

if [ ! -s ../pdb/$pdb.pdb ] ; then
	cp -v $c/int/reseek_bench/scop40pdb/pdb/$pdb.pdb  ../pdb/$pdb.pdb
fi
