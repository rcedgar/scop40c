#!/bin/bash -e

mkdir -p ../pdb
mkdir -p ../foldseek
mkdir -p ../reseek
mkdir -p ../tm
mkdir -p ../pairs
mkdir -p ../png
mkdir -p ../png2
mkdir -p ../pse
mkdir -p ../rotated
mkdir -p ../fa
mkdir -p ../blastp

pdb1=$1
pdb2=$2
comment=$3

for pdb in $pdb1 $pdb2
do
	if [ ! -s ../pdb/$pdb.pdb ] ; then
		cp -v $c/int/reseek_bench/scop40pdb/pdb/$pdb  ../pdb/$pdb.pdb
	fi
done

reseek \
	-convert ../pdb/$pdb1.pdb \
	-fasta ../fa/$pdb1

reseek \
	-convert ../pdb/$pdb2.pdb \
	-fasta ../fa/$pdb2

blastp \
	-query ../fa/$pdb1 \
	-subject ../fa/$pdb2 \
	-dbsize 11211 \
	> ../blastp/$pdb1.$pdb2

echo $comment \
	> ../pairs/$pdb1.$pdb2

TMalign \
	../pdb/$pdb1.pdb \
	../pdb/$pdb2.pdb \
	> ../tm/$pdb1.$pdb2

./foldseek_align_pair.bash \
	../pdb/$pdb1.pdb \
	../pdb/$pdb2.pdb \
	../foldseek/$pdb1.$pdb2 \
	> ../foldseek/$pdb1.$pdb2.stdout \
	2> ../foldseek/$pdb1.$pdb2.stderr

ls -lh ../foldseek/$pdb1.$pdb2

$src/reseek/github_releases/reseek-v2.5-linux-x86 \
	-alignpair ../pdb/$pdb1.pdb \
	-input2 ../pdb/$pdb2.pdb \
	-aln ../reseek/$pdb1.$pdb2 \
	-output ../rotated/$pdb1.pdb

echo cmd.load\(\"../pdb/$pdb1.pdb\"\) > tmp1.pml
echo cmd.png\(\"../png/$pdb1.png\"\) >> tmp1.pml
echo 'cmd.quit()' >> tmp1.pml
/mnt/c/ProgramData/pymol/PyMOLWin.exe ./tmp1.pml
sleep 2

echo cmd.load\(\"../pdb/$pdb2.pdb\"\) > tmp2.pml
echo cmd.png\(\"../png/$pdb2.png\"\) >> tmp2.pml
echo 'cmd.quit()' >> tmp2.pml
/mnt/c/ProgramData/pymol/PyMOLWin.exe ./tmp2.pml
sleep 2

echo cmd.load\(\"../rotated/$pdb1.pdb\"\) > tmp3.pml
echo cmd.load\(\"../pdb/$pdb2.pdb\"\) >> tmp3.pml
echo cmd.save\(\"../pse/$pdb1.$pdb2.pse\"\) >> tmp3.pml
echo 'cmd.quit()' >> tmp3.pml
/mnt/c/ProgramData/pymol/PyMOLWin.exe ./tmp3.pml
sleep 2

convert ../png/$pdb1.png ../png/$pdb2.png +append ../png2/$pdb1.$pdb2.png

grep -H TM-score= ../tm/$pdb1.$pdb2
grep -H . ../foldseek/$pdb1.$pdb2
grep -H AQ ../reseek/$pdb1.$pdb2

rm -f tmp*.pml
