#!/usr/bin/python2

import sys

doms = set()
dom2scopid = {}
for line in open("../data/scop40.lookup"):
	flds = line[:-1].split('\t')
	dom = flds[0]
	assert not dom in doms
	doms.add(dom)
	scopid = flds[1]
	dom2scopid[dom] = scopid

'''
./blastp_sf_pair.bash d.68.3 b.3.7
Query  1   GSSHHHHHHSSGLVPRGSHMA  21
           GSSHHHHHHSSGLVPRGSHMA
Sbjct  1   GSSHHHHHHSSGLVPRGSHMA  21
'''

# b.3.7 and d.68.3 share a short conserved motif (above)
FP_homologous_sfs = [ "b.3.7", "d.68.3" ]

frep = open("../results/final_analysis2.txt", "w")

'''
# head ../results/length_outliers.tsv  | columns.py
superfamily            d.230.4  median=52<80
superfamily              d.9.1  median=67<80
	 domain   d2h2za_/b.47.1.4            14  220  outlier
	 domain   d1kk8a2/c.37.1.9            94  216  outlier
superfamily             d.40.1  median=63<80
superfamily             g.23.1  median=74<80
	 domain  d2c3fa1/b.108.1.5            21  150  outlier
	 domain  d1k28a2/b.108.1.2            46  150  outlier
superfamily            f.23.31  median=37<80
superfamily              g.8.1  median=59<80
'''

short_sfs = set()
short_domains = set()
for line in open("../results/length_outliers.tsv"):
	flds = line[:-1].split('\t')
	if flds[0] == "superfamily":
		short_sfs.add(flds[1])
	elif flds[0] == "domain":
		short_domains.add(flds[1].split('/')[0])
	else:
		assert False, "line='%s'" % line.strip()

cluster_sfs = set()
cluster_folds = set()

def add_homologous_fold(cluster, fold):
	cluster_folds.add(fold)

def add_homologous_sf(cluster, sf):
	cluster_sfs.add(sf)

for line in open("../results/graph_fold.txt"):
	line = line.strip()
	if len(line) == 0:
		continue
	elif line.startswith("hit"):
		pass
	elif line.startswith("Cluster"):
		flds = line.split('\t')
		assert flds[0].startswith("Cluster")
		cluster = int(flds[0].replace("Cluster", ""))
		assert flds[1].startswith("size=")
		size = int(flds[1].split('=')[1])
		assert len(flds) == size + 2
		for i in range(size):
			add_homologous_fold(cluster, flds[2+i])
	else:
		assert False, "line='%s'" % line

for line in open("../results/graph_sf.txt"):
	line = line.strip()
	if len(line) == 0:
		continue
	elif line.startswith("hit"):
		pass
	elif line.startswith("Cluster"):
		flds = line.split('\t')
		assert flds[0].startswith("Cluster")
		cluster = int(flds[0].replace("Cluster", ""))
		assert flds[1].startswith("size=")
		size = int(flds[1].split('=')[1])
		assert len(flds) == size + 2
		for i in range(size):
			sf = flds[2+i]
			if sf in FP_homologous_sfs:
				sf = sf + ".FP" # quick hack to exclude
			add_homologous_sf(cluster, sf)
	else:
		assert False, "line='%s'" % line

scopids = set()
scopid2doms = {}
def final(dom, scopid):
	if not scopid in scopids:
		scopids.add(scopid)
		scopid2doms[scopid] = []
	scopid2doms[scopid].append(dom)

for dom in doms:
	scopid = dom2scopid[dom]
	flds = scopid.split('.')
	assert len(flds) == 4
	fold = flds[0] + '.' + flds[1]
	sf = fold + '.' + flds[2]

	if dom in short_domains:
		frep.write("%s\t%s\tdiscarded_short_domain\n" % (dom, scopid))
		continue

	if sf in short_sfs:
		frep.write("%s\t%s\tdiscarded_short_superfamily\n" % (dom, scopid))
		continue

	if fold in cluster_folds:
		frep.write("%s\t%s\tdiscarded_fold_cluster\n" % (dom, scopid))

	if sf in cluster_sfs:
		frep.write("%s\t%s\tdiscarded_superfamily_cluster\n" % (dom, scopid))

	frep.write("%s\t%s\tunchanged\n" % (dom, scopid))
	final(dom, scopid)

frep.close()

flookup = open("../results/scop40c.lookup", "w")
scopids = sorted(list(scopid2doms.keys()))
for scopid in scopids:
	doms = sorted(scopid2doms[scopid])
	for dom in doms:
		flookup.write(dom + '\t' + scopid + '\n')
flookup.close()
