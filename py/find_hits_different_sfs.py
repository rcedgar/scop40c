#!/usr/bin/python3

import sys

sf_or_fold = sys.argv[1]
assert sf_or_fold == "sf" or sf_or_fold == "fold"

accs = sys.argv[2:]

fout1 = open("../results/hits_different_%ss.tsv" % sf_or_fold, "w")
fout2 = open("../results/different_%ss.tsv"% sf_or_fold, "w")

def get_acc(label):
	flds = label.split('/')[1].split('.')
	if sf_or_fold == "fold":
		return flds[0] + "." + flds[1]
	else:
		return flds[0] + "." + flds[1] + "." + flds[2]

def get_fold(acc):
	flds = acc.split('.')
	return flds[0] + "." + flds[1]

accpairs = set()
accpair2evalue = {}

for acc in accs:
	flds = acc.split('.')
	fold = flds[0] + '.' + flds[1]
	if sf_or_fold == "sf":
		sf = flds[0] + '.' + flds[1] + '.' + flds[2]
	else:
		assert len(flds) == 2

	fn = "../tbls/" + acc
	for line in open(fn):
		if line.startswith('#'):
			continue
		flds = line[:-1].split()
		q = flds[0]
		qacc = get_acc(q)
		if qacc == acc:
			continue
		elif qacc > acc:
			accpair = (qacc, acc)
		else:
			accpair = (acc, qacc)
		E = float(flds[4])
		if not accpair in accpairs:
			accpairs.add(accpair)
			accpair2evalue[accpair] = E
		elif E < accpair2evalue[accpair]:
			accpair2evalue[accpair] = E

		if qacc[0] != acc[0]:
			diff = "class"
		elif sf_or_fold == "sf" and get_fold(acc) == get_fold(qacc):
			diff = "SF"
		else:
			diff = "fold"

		evalue = flds[4]
		s = evalue
		s += "\t" + q
		s += "\t" + acc
		s += "\t" + diff 
		fout1.write(s + '\n')
fout1.close()

for acc1, acc2 in accpairs:
	E = accpair2evalue[(acc1, acc2)]
	s = acc1
	s += "\t" + acc2
	s += "\t%.2g" % E
	fout2.write(s + '\n')
fout2.close()