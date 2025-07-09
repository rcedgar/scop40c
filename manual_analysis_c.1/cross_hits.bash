for n in `seq 1 6`
do
	echo === $n ===
	cut "-d " -f1 search.$n.tbl | grep -v "^#" | fgrep -v "c.$n." > cross.$n.hits
	grep -Ff cross.$n.hits search.$n.tbl
done | tee cross_hits_report.txt
