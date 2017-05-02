import copy
import numpy as np
import random
def greed_by_classes(items, constraints, P, M, IBC, method):
	invalids = []
	classes = list(IBC.keys())
	i_list = []
	random.shuffle(classes)
	while(len(classes) > 0):
		cl = classes.pop(0)
		if cl not in invalids:
			# print "LEN" +str(len(constraints.get(cl, [])))
			for i in IBC.get(cl):
				i_list.append(i)
			for c in constraints.get(cl, []):
				invalids.append(c)
			# print "INVALIDS " + str(len(invalids))
	# print invalids[0]
	return s_g(i_list, P, M, method)

def s_g(it, P, M, method):
	i_list = []
	lb = P
	mo = M
	val = 0
	i_list.sort(key = method, reverse = True)
	while (len(it) > 0):
		i = it.pop()
		# print i
		if (not (i.buy > mo or i.weight > lb)):
			lb -= i.weight
			mo -= i.buy
			val += i.sell
			i_list.append(i)
	return (val, list(set(i_list)))
def simple_greedy(items, constraints, P, M):
	results = []
	i_list = []
	val = 0
	lb = P
	mo = M
	invalids = set()
	it = items[:]
	le = len(items)
	while (len(it) != 0):
		i = it.pop(0)
		if (i.c not in invalids and not (i.buy > mo or i.weight > lb)):
			cl = i.c
			lb -= i.weight
			mo -= i.buy
			val += i.sell
			if cl in constraints:
				invalids.update(constraints[cl])
			i_list.append(i)
	results.append((val, list(set(i_list))))
	return max(results, key = lambda x: x[0])
