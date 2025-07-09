#!/bin/bash -ve

fa=../data/scop40_scopid.fa
labels=../labels/$1
seqs=../seqs/$1
aln=../alns/$1
hmm=../hmms/$1
tbl=../tbls/$1
hits=../hits/$1

mkdir -p ../labels
mkdir -p ../seqs
mkdir -p ../alns
mkdir -p ../hmms
mkdir -p ../tbls
mkdir -p ../hits

falabels $fa \
	| fgrep /$1. \
	> ../labels/$1

usearch \
	-fastx_getseqs $fa \
	-labels $labels \
	-fastaout $seqs

muscle \
	-super5 $seqs \
	-output $aln

hmmbuild $hmm $aln \
	> /dev/null

hmmsearch \
		--tblout $tbl \
		$hmm \
		$fa \
		> $hits
ls -lh $tbl
