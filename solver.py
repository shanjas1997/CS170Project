#!/usr/bin/env python

from __future__ import division
import argparse
from Item import Item
import Util
import numpy as np
import math
# import gurobipy as gp
# from pulp import *
"""
===============================================================================
Please complete the following function.
===============================================================================
"""

def solve(P, M, N, C, items, constraints):
    """
    Write your amazing algorithm here.

    Return: a list of strings, corresponding to item names.
    """
    """Here I will do the greedy algorithm. My algorithm will be done in the form that I will take the max of using 6 different sorting methods.
    First, let us make an incompatability dictionary to make things easier to look at"""
    # print "HIII"
    # M = Model("PLEASE LET THIS SHIT WORK")
    # M.addvar("x")
    # M.addconstr("")
    # M.setObj()
    incompatabilities = {}
    count = 0
    for constraint in constraints:
        #print count
        count += 1
        for c in constraint:
            if c not in incompatabilities:
                incompatabilities[c] = constraint
            else:
                incompatabilities[c].update(constraint)
            

    for c in incompatabilities:
        l = list(incompatabilities[c])
        l.remove(c)
        incompatabilities[c] = l
    # a = list(incompatabilities[170])
    # a.sort()
    # print a
    # print "OTHER"
    # b = list(incompatabilities[632])
    # b.sort()
    # print b
    # print "HELLO?"
    "finished making our incompatability list"

    """Pre-Processing"""
    # print len(items)
    STD_VALS = []
    for i in items:
        STD_VALS.append(i.eff/max(0.00001, len(incompatabilities.get(i.c, [1]))))
    stdev = np.std(STD_VALS)    
    mean = np.mean(STD_VALS)
    threshold = (mean - 1.6 * stdev)
    y = [i for i in items if ((i.eff/max(0.00001, len(incompatabilities.get(i.c, [1])))) > threshold and i.sell > i.buy)]
    items = y[:]
    prices = {}
    ibc = {}
    for i in items:
        if i.c not in prices:
            prices[i.c] = (i.sell - i.buy)
        else:
            prices[i.c] = prices[i.c] + (i.sell - i.buy)
        if i.c not in ibc:
            ibc[i.c] = [i]
        else:
            ibc[i.c].append(i)

    # print len(items)
    "We will store all our greedy stuff as tuples, to see what is best."
    solutions = []
    methods = []
    # methods.append(lambda x: prices.get(x.c, (x.buy - x.sell)) * x.sell / max(0.0001, x.buy) / (0.2 * max(1, len(incompatabilities.get(x.c, []))))) #sell / buy
    # methods.append(lambda x: prices.get(x.c, (x.buy - x.sell)) *((x.sell - x.buy) / max(0.0001, x.weight) / (0.2 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell - buy / weight)
    # methods.append(lambda x: prices.get(x.c, (i.buy - x.sell))* (x.sell / max(0.0001, (x.weight * x.buy)) / (0.2 * max(1, len(incompatabilities.get(x.c, []))))))
    # methods.append(lambda x: prices.get(x.c, (i.buy - x.sell))* (x.sell/ max(0.0001, (x.buy + x.weight)) / (0.2 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell / (buy + weight))
    # methods.append(lambda x: prices.get(x.c, (i.buy - x.sell))* x.sell / max(0.0001, x.weight) / (0.2 * max(1, len(incompatabilities.get(x.c, []))))) #sell / weight
    # # methods.append(lambda x: x.sell / max(0.0001, x.buy) / (0.6 * max(1, len(incompatabilities.get(x.c, []))))) #sell / buy
    # # methods.append(lambda x: ((x.sell - x.buy) / max(0.0001, x.weight) / (0.6 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell - buy / weight)
    # # methods.append(lambda x: (x.sell / max(0.0001, (x.weight * x.buy)) / (0.6 * max(1, len(incompatabilities.get(x.c, []))))))
    # # methods.append(lambda x: (x.sell/ max(0.0001, (x.buy + x.weight)) / (0.6 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell / (buy + weight))
    # # methods.append(lambda x: x.sell / max(0.0001, x.weight) / (0.6 * max(1, len(incompatabilities.get(x.c, []))))) #sell / weight
    # methods.append(lambda x: prices.get(x.c, (x.buy - x.sell)) * x.sell / max(0.0001, x.buy) / max(1, len(incompatabilities.get(x.c, [])))) #sell / buy
    # methods.append(lambda x: prices.get(x.c, (x.buy - x.sell)) * ((x.sell - x.buy) / max(1, len(incompatabilities.get(x.c, []))))) #(sell - buy / weight)
    # methods.append(lambda x: prices.get(x.c, (x.buy - x.sell)) * (x.sell / max(1, len(incompatabilities.get(x.c, [])))))

    methods.append(lambda x: x.sell / max(0.0001, x.buy) / (0.2 * max(1, len(incompatabilities.get(x.c, []))))) #sell / buy
    methods.append(lambda x: ((x.sell - x.buy) / max(0.0001, x.weight) / (0.2 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell - buy / weight)
    methods.append(lambda x: (x.sell / max(0.0001, (x.weight * x.buy)) / (0.2 * max(1, len(incompatabilities.get(x.c, []))))))
    methods.append(lambda x: (x.sell/ max(0.0001, (x.buy + x.weight)) / (0.2 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell / (buy + weight))
    methods.append(lambda x: x.sell / max(0.0001, x.weight) / (0.2 * max(1, len(incompatabilities.get(x.c, []))))) #sell / weight
    # methods.append(lambda x: x.sell / max(0.0001, x.buy) / (0.6 * max(1, len(incompatabilities.get(x.c, []))))) #sell / buy
    # methods.append(lambda x: ((x.sell - x.buy) / max(0.0001, x.weight) / (0.6 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell - buy / weight)
    # methods.append(lambda x: (x.sell / max(0.0001, (x.weight * x.buy)) / (0.6 * max(1, len(incompatabilities.get(x.c, []))))))
    # methods.append(lambda x: (x.sell/ max(0.0001, (x.buy + x.weight)) / (0.6 * max(1, len(incompatabilities.get(x.c, [])))))) #(sell / (buy + weight))
    # methods.append(lambda x: x.sell / max(0.0001, x.weight) / (0.6 * max(1, len(incompatabilities.get(x.c, []))))) #sell / weight
    methods.append(lambda x: x.sell / max(0.0001, x.buy) / max(1, len(incompatabilities.get(x.c, [])))) #sell / buy
    methods.append(lambda x: ((x.sell - x.buy) / max(1, len(incompatabilities.get(x.c, []))))) #(sell - buy / weight)
    methods.append(lambda x: (x.sell / max(1, len(incompatabilities.get(x.c, [])))))
    #DHRUV"S STUFF
    methods.append(lambda x: methods.append(lambda x: ((x.sell - x.buy) / math.pow(max(0.0001, x.weight), 2))))
    methods.append(lambda x: x.sell)
    methods.append(lambda x: math.pow(x.sell, 2) / max(0.0001, x.weight))
    methods.append(lambda x: math.pow((x.sell - x.buy), 2)/ max(0.0001, x.weight))
    methods.append(lambda x: math.pow((x.sell - x.buy), 2)/ (max(x.weight, 0.0001)/ P))
    methods.append(lambda x: (x.sell - x.buy) / (max(x.weight, 0.0001) / P))
    methods.append(lambda x: (x.sell - x.buy)/ math.pow((x.weight * P), 2))
    methods.append(lambda x: ((x.sell - x.buy)/ (max(x.weight, 0.0001) / P) * (x.sell/ math.pow(max(0.0001, x.weight), 2))))
    methods.append(lambda x: (x.sell / (max(x.buy, 0.0001) / M)))
    methods.append(lambda x: (x.sell) / ((max(x.weight , 0.0001) / P) * (max(x.buy, 0.0001) / M)))
    methods.append(lambda x: (x.sell / (max(x.weight, 0.0001) / P)) + (x.sell / (max(x.buy , 0.0001) / M)))
    ma = float('-inf')
    greedies = []
    stuff = items
    for _ in range(1):
        for me in methods:
            # print "HI"
            stuff.sort(key = me, reverse = True)
            res = Util.greedy(stuff, incompatabilities, P, M, ibc, mean, stdev, me)
            if (res[0] > ma):
                ma = res[0]
                greedies = res[1]
        solutions.append((ma,greedies))
    ma = float('-inf')
    greedies = []
    for me in methods:
        # print "HI"
        stuff.sort(key = me, reverse = True)
        res = Util.simple_greedy(stuff, incompatabilities, P, M, ibc, mean, stdev, me)
        if (res[0] > ma):
            ma = res[0]
            greedies = res[1]
    solutions.append((ma,greedies))    
    print (ma)
    "Here we will run Random Sampling"
    r = np.random.choice(items, 50, replace = False)


    "Dynamic Programming. (So help me God)"
    mP = sum(i.sell for i in items)
    i = Util.separateByClass(items)
    return max(solutions, key= lambda x: x[0])[1]

"""
===============================================================================
  No need to change any code below this line.
===============================================================================
"""

def read_input(filename):
    """
    P: float
    M: float
    N: integer
    C: integer
    items: list of tuples
    constraints: list of sets
    """
    with open(filename) as f:
        P = float(f.readline())
        M = float(f.readline())
        N = int(f.readline())
        C = int(f.readline())
        items = []
        constraints = []
        for i in range(N):
            name, cls, weight, cost, val = f.readline().split(";")
            items.append(Item(name, int(cls), float(weight), float(cost), float(val)))
        for i in range(C):
            constraint = set(eval(f.readline()))
            constraints.append(constraint)
    return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
    with open(filename, "w") as f:
        for i in items_chosen:
            f.write(i.name)
            f.write("\n")
def write_output2(ma):
    with open("score1.out", "w") as f:
        f.write("PROJECT")
        f.write(ma)
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="PickItems solver.")
    parser.add_argument("input_file", type=str, help="____.in")
    parser.add_argument("output_file", type=str, help="____.out")
    args = parser.parse_args()

    P, M, N, C, items, constraints = read_input(args.input_file)
    items_chosen = solve(P, M, N, C, items, constraints)
    write_output(args.output_file, items_chosen)