#!/usr/bin/python3

import sys

# 0.8741  d1a04a2/c.23.1  d1ccwa_/c.23.6
# 0.7825  d1a04a2/c.23.1  d7reqa2/c.23.6
# 0.66    d1a04a2/c.23.1  d1xrsb1/c.23.6

MIN_AGREE = 3
### MIN_MEANP = 0.8
algos = [ "dali", "tm", "foldseek", "reseek" ]

tsvfn = sys.argv[1]
excludesfn = sys.argv[2]
statsfn = sys.argv[3]
MAXP = sys.argv[4]

ftsv = open(tsvfn, "w")
fex = open(excludesfn, "w")
fstats = open(statsfn, "w")

def get_pair(q, t):
	if q > t:
		return (q, t)
	else:
		return (t, q)

all_pairs = set()

def read_hits(algo, fn):
	pairs = set()
	pair2tophit = {}
	for line in open(fn):
		flds = line[:-1].split('\t')
		P = float(flds[0])
		q = flds[1]
		t = flds[2]
		qsf = q.split('/')[1]
		tsf = t.split('/')[1]
		pair = get_pair(qsf, tsf)
		all_pairs.add(pair)
		if not pair in pairs:
			pairs.add(pair)
			pair2tophit[pair] = (None, None, None)
		topP, topq, topt = pair2tophit[pair]
		if topP is None or P < topP:
			pair2tophit[pair] = (P, q, t)
	return pair2tophit

algo2pair2tophit = {}
for algo in algos:
	algo2pair2tophit[algo] = read_hits(algo, "../top_fps/" + algo + "." + MAXP)

pair_algos_set = set()
algos2n = {}
algo2n = {}
for algo in algos:
	algo2n[algo] = 0

records = []
sumPs = []
for pair in all_pairs:
	s = pair[0]
	s += "\t" + pair[1]
	n = 0
	qs = []
	ts = []
	Ps = []
	pair_algos = []
	sumP = 0
	for algo in algos:
		try:
			topP, topq, topt = algo2pair2tophit[algo][pair]
			sumP += topP
			n += 1
			Ps.append(topP)
			qs.append(topq)
			ts.append(topt)
			pair_algos.append(algo)
			algo2n[algo] += 1
		except:
			Ps.append(None)
			qs.append(None)
			ts.append(None)
	if n < MIN_AGREE:
		continue
	sumPs.append(sumP)
	records.append((pair[0], pair[1], Ps, qs, ts))
	pair_algos = tuple(pair_algos)
	if not pair_algos in pair_algos_set:
		pair_algos_set.add(pair_algos)
		algos2n[pair_algos] = 1
	else:
		algos2n[pair_algos] += 1

for pair_algos in pair_algos_set:
	fstats.write(str(algos2n[pair_algos]) + " " + str(pair_algos) + "\n")
fstats.write(str(algo2n) + '\n')

fstats.write("%d records\n" % len(records))

def argsort(seq, rev):
    return sorted(range(len(seq)), key=seq.__getitem__, reverse=rev)

def prob2str(P):
	if P is None:
		return "."
	else:
		return "%.3g" % P

order = argsort(sumPs, True)
s = "Sum"
for algo in algos:
	s += "\t" + algo
s += "\tSF1"
s += "\tSF2"
s += "\tSF/fold"
s += "\tTop hits"
ftsv.write(s + '\n')

def get_fold(sf):
	flds = sf.split('.')
	return flds[0] + "." + flds[1]

excludes = set()
for k in order:
	sumP = sumPs[k]
	qsf, tsf, Ps, qs, ts = records[k]
	assert len(Ps) == 4
	assert len(qs) == 4
	assert len(ts) == 4

	s = "%.3e" % sumP
	consensus = 0
	for i in range(4):
		P = Ps[i]
		if not P is None:
			consensus += 1
		s += "\t" + prob2str(P)
	s += "\t" + qsf
	s += "\t" + tsf

	qfold = get_fold(qsf)
	tfold = get_fold(tsf)
	if qfold == tfold:
		s += "\tSF"
		excludes.add(qsf)
		excludes.add(tsf)
	else:
		s += "\tfold"
		excludes.add(qfold)
		excludes.add(tfold)

	q0 = None
	t0 = None
	for i in range(4):
		q = qs[i]
		t = ts[i]
		if q is None:
			continue
		if q0 is None:
			q0 = q
			t0 = t
			s += "\t%s" % q.split('/')[0]
			s += ",%s" % t.split('/')[0]
		elif q != q0 or t != t0:
			s += "\t%s" % q.split('/')[0]
			s += ",%s" % t.split('/')[0]
	ftsv.write(s + '\n')

ftsv.close()

for x in sorted(excludes):
	x = x + '.'
	for x2 in excludes:
		x2 = x2 + '.'
		if x2.startswith(x) and len(x) < len(x2):
			fstats.write("enclosed %s %s\n" % (x, x2))
			continue
	fex.write(x + '\n')
fex.close()
fstats.write("%d excludes %s\n" % (len(excludes), excludesfn))