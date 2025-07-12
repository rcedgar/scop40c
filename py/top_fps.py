#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
from read_dist import read_dist

AP = argparse.ArgumentParser()
AP.add_argument("--hits", required=True, help="Hits tsv")
AP.add_argument("--edf", required=True, help="C_score_F")
AP.add_argument("--maxprob", required=False, type=float, default=1e-4) # 1/10000
AP.add_argument("--lookup", required=False, type=str, default="../data/scop40.lookup", 
				help="Tsv with 1. domain 2. scopid e.g. a.1.2.3, default ../data/scop40.lookup")
AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score field numbers (default 1,2,3)")
AP.add_argument("--output", required=False, type=str, default="/dev/stdout", help="Output TSV")
AP.add_argument("--evalues", default=False, action="store_true")
Args = AP.parse_args()

fs = Args.fields.split(",")
if len(fs) != 3:
		assert False, "--fields must be 3 comma-separated 1-based field numbers"

fout = open(Args.output, "w")

qfldnr = int(fs[0]) - 1
tfldnr = int(fs[1]) - 1
scorefldnr = int(fs[2]) - 1

def get_sf_from_fam(fam):
	flds = fam.split('.')
	assert len(flds) == 4
	sf = flds[0] + "." + flds[1] + '.' + flds[2]
	return sf

sfs = set()
dom2sf = {}
for line in open(Args.lookup):
	flds = line[:-1].split('\t')
	dom = flds[0]
	fam = flds[1]
	sf = get_sf_from_fam(fam)
	dom2sf[dom] = sf

bin_mids, C_score_F = read_dist(Args.edf, "C_score_F")
bin_mids = np.array(bin_mids, dtype=np.float32)

def get_P(score):
	return np.interp(score, bin_mids, C_score_F)

def get_dom_from_label(label):
	label = label.replace(".pdb", "")
	n = label.find('/')
	if n > 0:
		label = label[:n]
	if label.startswith("DUPE"):
		n = label.find('_')
		label = label[n+1:]
	return label

n = 0
for line in open(Args.hits):
	flds = line[:-1].split('\t')
	score = float(flds[scorefldnr])
	if Args.evalues:
		evalue = score
		if evalue < 1e-20:
			evalue = 1e-20
		score = -math.log10(evalue)
	q = get_dom_from_label(flds[qfldnr])
	t = get_dom_from_label(flds[tfldnr])
	if q == t:
		continue
	qsf = dom2sf.get(q)
	tsf = dom2sf.get(t)
	if qsf is None or tsf is None:
		continue
	if qsf == tsf:
		continue
	P = get_P(score)
	if P > Args.maxprob:
		continue
	s = "%.4g" % P
	s += "\t" + q + "/" + str(qsf)
	s += "\t" + t + "/" + str(tsf)
	if Args.evalues:
		s += "\t%.3g" % evalue
	else:
		s += "\t%.3g" % score
	fout.write(s + '\n')
	n += 1
fout.close()
sys.stderr.write("%d %s\n" % (n, Args.hits))
