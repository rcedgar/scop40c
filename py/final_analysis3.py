#!/usr/bin/python2

import sys

reportfn = sys.argv[1]
lookupfn = sys.argv[2]

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
name2excludes["manual"] = set( [ line.strip() for line in open("../data/manual_excludes.txt")] )
name2excludes["consensus"] = set( [ line.strip() for line in open("../top_fps/excludes.txt")] )
name2excludes["length"] = set( [ line.strip() for line in open("../results/length_excludes.txt")] )
name2excludes["hmm"] = set( [ line.strip() for line in open("../results/hmm_excludes_fold.txt")] )
name2excludes["hmm"] |= set( [ line.strip() for line in open("../results/hmm_excludes_sf.txt")] )

# Exclude by domain identifier
short_domains = set( [ line.strip() for line in open("../results/length_excludes.txt")] )

short_domains = set()
for line in open("../results/length_outliers.tsv"):
	flds = line[:-1].split('\t')
	if flds[0] == "domain":
		short_domains.add(flds[1].split('/')[0])

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
