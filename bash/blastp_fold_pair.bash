#!/bin/bash -e

mkdir -p ../blastp_fold_pair
mkdir -p ../blastp_fold_pair_alns

blastp \
	-query ../seqs/$1 \
	-subject ../seqs/$2 \
	> ../blastp_fold_pair_alns/${1}_${2}

blastp \
	-query ../seqs/$1 \
	-subject ../seqs/$2 \
	-outfmt "6 evalue qacc sacc" \
	| sort -gk1 \
	> ../blastp_fold_pair/${1}_${2}

head ../blastp_fold_pair/${1}_${2}
