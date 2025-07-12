#!/usr/bin/python3

import sys

MIN_MEDIAN = 80

fn = "../short_domains/lengths.tsv"

label2length = {}
sfs = set()
sf2lengths = {}
sf2labels = {}

def get_sf_from_label(label):
	flds = label.split('/')[1].split('.')
	return flds[0] + '.' + flds[1] + '.' + flds[2]

for line in open(fn):
	flds = line[:-1].split('\t')
	assert len(flds) == 2
	label = flds[0]
	length = int(flds[1])
	label2length[label] = length
	sf = get_sf_from_label(label)
	if not sf in sfs:
		sfs.add(sf)
		sf2lengths[sf] = []
		sf2labels[sf] = []
	sf2lengths[sf].append(length)
	sf2labels[sf].append(label)

for sf in sfs:
	labels = sf2labels[sf]
	lengths = sf2lengths[sf]
	n = len(labels)
	assert len(lengths) == n
	lengths.sort()
	median_length = lengths[n//2]
	if median_length < MIN_MEDIAN:
		s = "superfamily"
		s += "\t" + sf
		s += "\tmedian=%d<%d" % (median_length, MIN_MEDIAN)
		print(s)
		continue
	for i in range(n):
		length = lengths[i]
		if length < median_length/2:
			s = "domain"
			s += "\t" + labels[i]
			s += "\t%d" % length
			s += "\t%d" % median_length
			s += "\toutlier"
			print(s)
