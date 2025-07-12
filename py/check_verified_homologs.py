#!/usr/bin/python2

import sys

verified_homologs = [ "b.68.", "b.69.", "b.70.", "c.2.", "c.3.", "c.4." ]

def check_acc(acc):
	global found
	if acc in verified_homologs:
		found.add(acc)

def check(MAXE, MAXP):
	global found
	found = set()
	for line in open("../top_fps/top_fps_excludes." + MAXP + ".txt"):
		acc = line.strip()
		check_acc(acc)

	for line in open("../graphs/hmm_excludes_fold." + MAXE + ".txt"):
		acc = line.strip()
		check_acc(acc)

	N = len(verified_homologs)
	n = len(found)
	s = "MAXE %s, MAXP %s, found %d / %d" % (MAXE, MAXP, n, N)
	if n == N:
		s += " << ok"
	print(s)

for MAXE in [ "1e-4", "1e-6", "1e-8" ]:
	for MAXP in [ "1e-4", "1e-5", "1e-6" ]:
		check(MAXE, MAXP)