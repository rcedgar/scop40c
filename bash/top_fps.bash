#!/bin/bash -e


MAXP=$1

if [ x$MAXP == x ] ; then
	echo $0: missing arg
	exit 1
fi

./top_fps_dali.bash $MAXP
./top_fps_foldseek.bash $MAXP
./top_fps_reseek.bash $MAXP
./top_fps_tm.bash $MAXP

python ../py/top_fps_report.py \
	../top_fps/top_fps_report.$MAXP.tsv \
	../top_fps/top_fps_excludes.$MAXP.txt \
	../top_fps/top_fps_stats.$MAXP.txt \
	$MAXP
