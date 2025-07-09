#!/bin/bash -e

name=2025-05-18_final_analysis
rm -rf ../runs/$name
mkdir -p ../runs/$name

./final_analysis.bash

cp -v ../results/* ../runs/$name

ls -lh ../runs/$name
