#!/bin/bash -e

for n in 1 2 3 4 5 6
do
	fgrep -w c.$n $src/scopn2/data/scop40.lookup \
		| cut -f1 \
		> c.$n.labels

	usearch \
		-fastx_getseqs $c/int/reseek_bench/data/scop40_scopid.fa \
		-labels c.$n.labels \
		-label_prefix_match \
		-fastaout c.$n.fa
	
	muscle -super5 c.$n.fa -output c.$n.afa

	hmmbuild c.$n.hmm c.$n.afa

	hmmsearch \
		--tblout search.$n.tbl \
		c.$n.hmm \
		$c/int/reseek_bench/data/scop40_scopid.fa \
		> search.$n.txt

	ls -lh search.$n.t*
done
