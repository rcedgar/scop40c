#!/bin/bash -e

name=2025-05-18_final_analysis2
rm -rf ../runs/$name
mkdir -p ../runs/$name

./final_analysis2.bash

cp -v ../results/* ../runs/$name

ls -lh ../runs/$name
