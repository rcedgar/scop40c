#!/bin/bash -e

python ../py/final_analysis2.py

cut -f3 ../results/final_analysis2.txt \
	| sort \
	| uniq -c \
	| sort -n \
	| tee ../results/final_analysis2_summary.txt
