#!/usr/bin/python3

import sys

sf_or_fold = sys.argv[1]
MAXE = float(sys.argv[2])
graphfn = sys.argv[3]
excludesfn = sys.argv[4]

fgraph = open(graphfn, "w")
fex = open(excludesfn, "w")

excludes = set()

'''
# sort -gk3 ../results/different_sfs.tsv  | head | columns.py
c.10.3  c.10.2    1e-22
b.68.9  b.68.5  1.1e-15
 c.4.1   c.3.1  3.5e-13
b.69.2  b.68.6  5.6e-12
 c.1.4   c.1.2  1.9e-10
 c.1.4  c.1.10  3.8e-10
b.68.9  b.68.6    9e-10
 c.4.1   c.2.1  1.1e-09
 c.1.3   c.1.2  3.2e-09
 c.1.5   c.1.4  6.7e-09
'''

sfs = set()
graph = {}

edges = []
evalues = []

def add_sf(sf):
	if not sf in sfs:
		sfs.add(sf)
		graph[sf] = []

def add_edge(sf1, sf2, evalue):
	evalues.append(evalue)
	edges.append((sf1, sf2, evalue))
	if evalue <= MAXE:
		excludes.add(sf1)
		excludes.add(sf2)
		add_sf(sf1)
		add_sf(sf2)
		graph[sf1].append(sf2)
		graph[sf2].append(sf1)

fn = "../results/different_%ss.tsv" % sf_or_fold
for line in open(fn):
	flds = line[:-1].split('\t')
	sf1 = flds[0]
	sf2 = flds[1]
	E = float(flds[2])
	add_edge(sf1, sf2, E)
	add_edge(sf2, sf1, E)

# gemini prompt: please write a python function, input is an undirected graph represented as a dictionary where the key is the source edge label and the value is the destination edge label. Return a list of connected components, each component is a list of labels. 
def find_connected_components(graph):
	"""
	Finds the connected components of an undirected graph.

	Args:
		graph (dict): An undirected graph represented as a dictionary where the
					  key is a node label and the value is a list of its neighbors.

	Returns:
		list: A list of connected components, where each component is a list of node labels.
	"""
	visited = set()
	components = []
	nodes = set(graph.keys())
	for neighbors in graph.values():
		nodes.update(neighbors)

	for node in nodes:
		if node not in visited:
			component = []
			stack = [node]
			visited.add(node)
			while stack:
				current_node = stack.pop()
				component.append(current_node)
				neighbors = graph.get(current_node, []) + [n for n, adj in graph.items() if current_node in adj]
				for neighbor in neighbors:
					if neighbor not in visited:
						visited.add(neighbor)
						stack.append(neighbor)
			components.append(sorted(component))
	return components

ccs = find_connected_components(graph)
n = len(ccs)
if 0:
	for i in range(n):
		cc = ccs[i]
		print(i, cc)

def in_same_cc(sf1, sf2):
	for i in range(n):
		cc = ccs[i]
		if sf1 in cc and sf2 in cc:
			return True
	return False

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return 

order = sorted(range(len(evalues)), key=evalues.__getitem__)

n = len(ccs)
for i in range(n):
	cc = ccs[i]
	s = "Cluster%d" % i
	k = len(cc)
	s += "\tsize=%d" % k
	for sf in cc:
		s += "\t" + sf
	fgraph.write(s + '\n')

	for k in order:
		sf1, sf2, evalue = edges[k]
		if sf1 > sf2 and sf1 in cc and sf2 in cc:
			s = "hit"
			s += "\t" + sf1
			s += "\t" + sf2
			s += "\t%.2g" % evalue
			if evalue <= MAXE:
				s += "\tbuild"
			else:
				s += "\tadd"
			fgraph.write(s + '\n')

fgraph.close()

for sf in sorted(excludes):
	fex.write(sf + '.\n')
fex.close()
