#!/bin/bash -e

rm -rf ../top_fps
rm -rf ../graphs
rm -rf ../final_analysis4

for MAXE in 1e-4 1e-6 1e-8
do
	echo ./build_graphs.bash MAXE=$MAXE
	./build_graphs.bash $MAXE
done

for MAXP in 1e-4 1e-5 1e-6
do
	echo ./top_fps.bash MAXP=$MAXP
	./top_fps.bash $MAXP
done

for MAXE in 1e-4 1e-6 1e-8
do
	for MAXP in 1e-4 1e-5 1e-6
	do
		echo ./final_analysis4.bash $MAXE $MAXP
		./final_analysis4.bash $MAXE $MAXP
	done
done

./final_analysis4.bash -1 -1
