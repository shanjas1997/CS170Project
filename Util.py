import copy
import numpy as np
import random
def greedy(items, constraints, P, M, IBC, mean, stdev, method): #conduct the greedy algorithm on this sorted list.
	results = []
	i_list = []
	val = 0
	lb = P
	mo = M
	md = mean - stdev
	invalids = set()
	it = items[:]
	same = IBC
	# print len(it)
	le = len(items)
	# print "RUN"
	# print "TRY"
	while (len(it) != 0):
		i = it.pop(0)
		rn = random.random()
		if (i.c not in invalids and not (i.buy > mo or i.weight > lb)):
			if (rn >= .1):
				cl = i.c
				lb -= i.weight
				mo -= i.buy
				val += i.sell
				sa = same.get(cl)
				sa.sort(key = method, reverse = True)
				for x in sa:
					if (not (x.buy > mo or x.weight > lb)) and i.eff > md:
						if (x in it):
							r = random.random()
							if (r >= .1):
								it.remove(x)
								lb -= x.weight
								mo -= x.buy
								val += x.sell
								i_list.append(x)	
				if cl in constraints:
					invalids.update(constraints[cl])
				i_list.append(i)
	results.append((val, list(set(i_list))))
	invalids = set()
	it = items[1:]
	i_list = []
	# IB = copy.deepcopy(IBC)
	val = 0
	lb = P
	mo = M
	# print "RUN"
	# while (len(it) != 0):
	# 	i = it.pop(0)
	# 	# rand = np.rand
	# 	if (i.c not in invalids and not (i.buy > mo or i.weight > lb)):
	# 		cl = i.c
	# 		lb -= i.weight
	# 		mo -= i.buy
	# 		val += i.sell
	# 		sa = same.get(cl)
	# 		sa.sort(key = method, reverse = True)
	# 		for x in sa:
	# 			if (not (x.buy > mo or x.weight > lb)) and i.eff > md:
	# 				if (x in it):
	# 					it.remove(x)
	# 					lb -= x.weight
	# 					mo -= x.buy
	# 					val += x.sell
	# 					i_list.append(x)	
	# 		if cl in constraints:
	# 			invalids.update(constraints[cl])
	# 		i_list.append(i)
	# results.append((val, list(set(i_list))))
	# invalids = set()
	# it = items[le//10:]
	# i_list = []
	# # IB = copy.deepcopy(IBC)
	# val = 0
	# lb = P
	# mo = M
	# # print "RUN"
	# while (len(it) != 0):
	# 	i = it.pop(0)
	# 	if (i.c not in invalids and not (i.buy > mo or i.weight > lb)):
	# 		cl = i.c
	# 		lb -= i.weight
	# 		mo -= i.buy
	# 		val += i.sell
	# 		sa = same.get(cl)
	# 		sa.sort(key = method, reverse = True)
	# 		for x in sa:
	# 			if (not (x.buy > mo or x.weight > lb)) and i.eff > md:
	# 				if (x in it):
	# 					it.remove(x)
	# 					lb -= x.weight
	# 					mo -= x.buy
	# 					val += x.sell
	# 					i_list.append(x)
	# 		if cl in constraints:
	# 			invalids.update(constraints[cl])
	# 		i_list.append(i)
	# results.append((val, list(set(i_list))))
	return max(results, key = lambda x: x[0])
def prune(items, constraints, P, M): 
	"""prunes the list down subject to constraints. This constraint is not the same
	as the one before, but rather the dictionary list of the one from above."""
	update = []
	for i in items:
		if not (i.c in constraints or i.buy > M or i.weight > P):
			update.append(i)
	# print len(items)
	return update
def separateByClass(items):
	itemsByClass = {}
	for i in items:
		c = i.c
		if c not in itemsByClass:
		    itemsByClass[c] = [i]
		else:
			itemsByClass[c].append(i)
	# print itemsByClass
	return itemsByClass