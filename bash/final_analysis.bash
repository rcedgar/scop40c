#!/bin/bash -e

./final_analysis_.bash \
	| tee ../results/final_analysis_summary.txt

ls -lh ../results/final_analysis_summary.txt
