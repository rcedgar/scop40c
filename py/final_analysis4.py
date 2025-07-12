#!/usr/bin/python2

import sys

reportfn = sys.argv[1]
lookupfn = sys.argv[2]
MAXE = sys.argv[3]
MAXP = sys.argv[4]

length_only = False
if MAXE == "-1" and MAXP == "-1":
	length_only = True

doms = set()
dom2scopid = {}
for line in open("../data/scop40.lookup"):
	flds = line[:-1].split('\t')
	dom = flds[0]
	assert not dom in doms
	doms.add(dom)
	scopid = flds[1]
	dom2scopid[dom] = scopid

# Exclude by SCOP classification
name2excludes = {}

#######################################################################################################
# manual excludes not needed
#######################################################################################################
# # for x in `cat ../data/manual_excludes.txt`; do echo $x `grep -c $x *exclud*.txt | grep -v :0`; done
# c.1. hmm_excludes_sf.txt:8
# b.1. length_excludes.txt:9
# b.68. hmm_excludes_sf.txt:3
# b.69. hmm_excludes_sf.txt:2
# name2excludes["manual"] = set( [ line.strip() for line in open("../data/manual_excludes.txt")] )
#######################################################################################################

if not length_only:
	name2excludes["consensus"] = set( [ line.strip() for line in open("../top_fps/top_fps_excludes." + MAXP + ".txt")] )
	name2excludes["hmm"] = set( [ line.strip() for line in open("../graphs/hmm_excludes_fold." + MAXE + ".txt")] )
	name2excludes["hmm"] |= set( [ line.strip() for line in open("../graphs/hmm_excludes_sf." + MAXE + ".txt")] )

name2excludes["length"] = set()
short_domains = set()
for line in open("../length_outliers/length_outliers.tsv"):
	flds = line[:-1].split('\t')
	if flds[0] == "domain":
		short_domains.add(flds[1])
	elif flds[0] == "superfamily":
		name2excludes["length"].add(flds[1])

def include_why(dom, scopid):
	flds = scopid.split('.')
	assert len(flds) == 4
	fold_dot = flds[0] + '.' + flds[1] + '.'
	sf_dot =  fold_dot + flds[2] + '.'
	for name in list(name2excludes.keys()):
		excludes = name2excludes[name]
		for x in excludes:
			if fold_dot.startswith(x) or sf_dot.startswith(x):
				return False, "discard_" + name
	if dom in short_domains:
		return False, "short_domain"
	return True, "include"

keep_scopids = set()
keep_scopid2doms = {}
def keep(dom, scopid):
	if not scopid in keep_scopids:
		keep_scopids.add(scopid)
		keep_scopid2doms[scopid] = set()
	keep_scopid2doms[scopid].add(dom)

with open(reportfn, "w") as frep:
	for dom in doms:
		scopid = dom2scopid[dom]
		include, why = include_why(dom, scopid)
		frep.write("%s\t%s\t%s\n" % (dom, scopid, why))
		if include:
			keep(dom, scopid)

with open(lookupfn, "w") as flookup:
	keep_scopids = sorted(list(keep_scopid2doms.keys()))
	for scopid in keep_scopids:
		keep_doms = sorted(keep_scopid2doms[scopid])
		for keep_dom in keep_doms:
			flookup.write(keep_dom + '\t' + scopid + '\n')
