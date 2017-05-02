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
    incompatabilities = {}
    for constraint in constraints:
        for c in constraint:
            if c not in incompatabilities:
                incompatabilities[c] = set(constraint)
            else:
                incompatabilities[c].update(constraint)
            

    for c in incompatabilities:
        l = list(incompatabilities[c])
        l.remove(c)
        incompatabilities[c] = set(l)
    "finished making our incompatability list"

    """Pre-Processing"""
    prices = {}
    ibc = {}
    for i in items:
        # if i.c not in prices:
        #     prices[i.c] = (i.sell - i.buy)
        # else:
        #     prices[i.c] = prices[i.c] + (i.sell - i.buy)
        if i.c not in ibc:
            ibc[i.c] = [i]
        else:
            ibc[i.c].append(i)

    # print len(items)
    "We will store all our greedy stuff as tuples, to see what is best."
    solutions = []
    methods = []
    methods.append(lambda x: x.sell / max(0.0001, x.buy))
    methods.append(lambda x: ((x.sell - x.buy) / max(0.0001, x.weight))) #(sell - buy / weight)
    methods.append(lambda x: (x.sell / max(0.0001, (x.weight * x.buy))))
    methods.append(lambda x: (x.sell/ max(0.0001, (x.buy + x.weight)))) #(sell / (buy + weight))
    methods.append(lambda x: x.sell / max(0.0001, x.weight))
    methods.append(lambda x: x.sell / max(0.0001, x.buy))
    methods.append(lambda x: ((x.sell - x.buy)))
    methods.append(lambda x: x.sell)
    methods.append(lambda x: (x.sell - x.buy)/ math.pow(max(x.weight, 0.0001) /P, 2))
    methods.append(lambda x: ((x.sell - x.buy)/ (max(x.weight, 0.0001) / P) * (x.sell/ math.pow(max(0.0001, x.weight), 2))))
    methods.append(lambda x: (x.sell / (max(x.weight, 0.0001) / P)) + (x.sell / (max(x.buy , 0.0001) / M)))

    for i in range(25):
        # print i
        stuff = items
        for me in methods:
            solutions.append(Util.greed_by_classes(stuff, incompatabilities, P, M, ibc, me))
    stuff = items
    for me in methods:
        stuff.sort(key = me, reverse = True)
        solutions.append(Util.simple_greedy(stuff,incompatabilities, P, M))
    print max(solutions, key = lambda x: x[0])[0]
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
