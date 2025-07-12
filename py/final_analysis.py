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

frep = open("../results/final_analysis.txt", "w")

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

fold_clusters = set()
sf_clusters = set()

fold_cluster_names = []
sf_cluster_names = []

fold_cluster_members = []
sf_cluster_members = []

sf2cluster = {}
fold2cluster = {}

def add_homologous_fold(cluster, fold):
	fold2cluster[fold] = cluster
	if not cluster in fold_clusters:
		fold_clusters.add(cluster)
		scop_class = fold[0]
		name = scop_class + ".0%d" % (cluster+1)
		fold_cluster_names.append(name)
		fold_cluster_members.append([ ])
	fold_cluster_members[cluster].append(fold)

def add_homologous_sf(cluster, sf):
	sf2cluster[sf] = cluster
	if not cluster in sf_clusters:
		sf_clusters.add(cluster)
		flds = sf.split('.')
		name = flds[0] + '.' + flds[1] + ".0%d" % (cluster+1)
		sf_cluster_names.append(name)
		sf_cluster_members.append([ ])
	sf_cluster_members[cluster].append(sf)

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

n = len(fold_cluster_names)
assert len(fold_cluster_members) == n
for cluster in range(n):
	s = "# merged fold "
	s += fold_cluster_names[cluster]
	s += " = " + " + ".join(fold_cluster_members[cluster])
	frep.write(s + '\n')

n = len(sf_cluster_names)
assert len(sf_cluster_members) == n
for cluster in range(n):
	s = "# merged superfamily "
	s += sf_cluster_names[cluster]
	s += ' = ' + ' + '.join(sf_cluster_members[cluster])
	if not s.find(".FP") > 0:
		frep.write(s + '\n')

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

	fold_cluster = fold2cluster.get(fold)
	sf_cluster = sf2cluster.get(sf)

	if not fold_cluster is None:
		# if not sf_cluster is None:
		# 	assert False, "domain=%s/%s in fold + sf cluster" % (dom, sf)
		fold_name = fold_cluster_names[fold_cluster]
		updated_scopid = fold_name + ".00.00"
		frep.write("%s\t%s\tmerged_fold=>%s\n" % (dom, scopid, updated_scopid))
		final(dom, updated_scopid)
		continue

	if not sf_cluster is None:
		assert fold_cluster is None
		sf_name = sf_cluster_names[sf_cluster]
		updated_scopid = sf_name + ".00"
		frep.write("%s\t%s\tmerged_sf=>%s\n" % (dom, scopid, updated_scopid))
		final(dom, updated_scopid)
		continue

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
