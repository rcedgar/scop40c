#!/bin/bash -e

python ../py/final_analysis.py

echo
cut -f3 ../results/final_analysis.txt \
	| grep -v discarded \
	| grep -v "^#" \
	| sort \
	| uniq -c \
	| sort -nr \
	| sed "-es/^  *//" \
	| sed "-es/ /	/"

echo
cut -f3 ../results/final_analysis.txt \
    | grep discarded \
	| sort \
    | uniq -c \
    | sort -nr \
    | sed "-es/^  *//" \
    | sed "-es/ /   /"

echo
grep "^#" ../results/final_analysis.txt

N=`cat ../results/final_analysis.txt \
	| grep -v "^#" \
	| wc -l`

n=`cat ../results/final_analysis.txt \
	| grep -v discarded \
	| grep -v "^#" \
	| wc -l`

echo
echo "$n / $N domains"
