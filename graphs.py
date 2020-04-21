#!/usr/bin/env python3

import random
import pprint
from collections import defaultdict

import numpy as np
from mtt import *

# print graph with nice formatting
def printGraph(g):
    pp = pprint.PrettyPrinter()
    pp.pprint(g)

# does dfs to test for connected-ness
def is_connected(g):
    visited = {}
    start = 0
    for v in g.keys():
        visited[v] = False
        start = v # grab any vertex
    stack = [start]
    visited[start] = True
    while len(stack) > 0:
        top = stack.pop()
        for nbr in g[top]:
            if not visited[nbr]:
                stack.append(nbr)
                visited[nbr] = True
    for k, v in visited.items():
        if not v:
            return False
    return True

# given a graph g, counts the number of edges in the graph
# assumes g is undirected, so each edge appears twice
# useful for sanity checks
def num_edges(g):
    total = 0
    for k, v in g.items():
        total += len(v)
    return total // 2

def make_complete_graph(n):
    g = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            g[i].append(j)
            g[j].append(i)
    return g

def make_random_graph(n, density, seed = None, max_degree = np.inf, min_degree = 0):

    # set a fixed seed
    if seed:
        random.seed(seed)

    # we want the graph to be connected, so we start with a spanning tree
    g = make_random_st(n)
    for i in range(n):
        for j in range(i+1, n):
            if j in g[i]:
                continue
            # check existing degree
            if len(g[i]) >= max_degree:
                break
            if len(g[i]) < min_degree or random.random() < density:
                g[i].append(j)
                g[j].append(i)
    return g

def make_random_st_dfs(n, v, visited, st):
    visited.add(v)
    # consider all other vertices except v as neighbors
    neighbors = [x if x < v else x + 1 for x in range(n - 1)]
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if neighbor not in visited:
            st[v].append(neighbor)
            st[neighbor].append(v)
            make_random_st_dfs(n, neighbor, visited, st)


def make_random_st(n):
    root = random.randint(0, n - 1)
    visited = set()
    st = defaultdict(list)
    make_random_st_dfs(n, root, visited, st)
    return st

def get_random_graph(n, density, max_degree, min_degree):
    g1 = {}
    for i in range(n):
        g1[i] = []
    for i in range(n):
        for j in range(i+1, n):
            if len(g1[i]) >= max_degree:
                break
            if len(g1[i]) < min_degree or random.random() < density:
                g1[i].append(j)
                g1[j].append(i)
    return g1

def get_random_connected_graph(n, density, seed = None, max_degree = np.inf, min_degree = 0):

    # set a fixed seed
    if seed:
        random.seed(seed)

    if (density == 0 and n > 1):
        print("this is impossible.")
        return None
    g = get_random_graph(n, density, max_degree, min_degree)
    while not is_connected(g):
        g = get_random_graph(n, density, max_degree, min_degree)
    return g

 # chooses a random edge from g and returns it
 # assumes g is connected
def get_random_edge(g):
    random_u = random.choice(list(g.keys()))
    random_v = random.choice(g[random_u]) # g[u] is not empty, assuming g is connected
    return (random_u, random_v)

# To examine distribution of spanning tree samplers, need a way to put same graphs into some same form
# assuming the graph vertices are labelled with integers, can put the graph into standard form as
# [num_vertices, list of edges], where edges (u, v) are given lexicographic order
# example: [5, (1, 2), (1, 3), (1, 4), (2, 3)]
def get_standard_form(g):
    num_vertices = len(g)
    vertices = []
    edges = []
    for u, nbrs in g.items():
        vertices.append(u)
        for v in nbrs:
            if (u < v): # prevent edge appearing twice
                edges.append((u, v))
    edges.sort()
    return [num_vertices, edges]

def test_sf():
    g = make_random_graph(5, 1)
    sf = get_standard_form(g)
    pp = pprint.PrettyPrinter()
    pp.pprint(g)
    pp.pprint(sf)

    g = make_random_graph(10, 0.3)
    sf = get_standard_form(g)
    pp = pprint.PrettyPrinter()
    pp.pprint(g)
    pp.pprint(sf)

    g = make_random_graph(10, 0.3)
    del g[0]
    sf = get_standard_form(g)
    pp = pprint.PrettyPrinter()
    pp.pprint(g)
    pp.pprint(sf)

# class to count the number of each spanning tree seen
class ST_counter:
    def __init__(self):
        self.trees = []
        self.counts = []

    # warning: this method is really inefficient
    def add_tree(self, t):
        sf = get_standard_form(t)
        for i in range(len(self.trees)):
            if self.trees[i] == sf:
                self.counts[i] += 1
                return
        self.trees.append(sf)
        self.counts.append(1)

# takes a uniform random sample of n integers in the range [a, b] inclusive
# records how many times each integer appears
# this is the benchmark of what a uniform distribution ought to look like
def get_random_distribution(a, b, n):
    d = defaultdict(int)
    for i in range(n):
        d[random.randint(a, b)] += 1
    return d

def test_complete_graphs():
    start_time = time.time()
    print("Generating complete graph...")
    g = make_complete_graph(4)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Calulating MTT...")
    start_time = time.time()
    sign, logdet = MTT(g, use_log=True)
    assert(sign > 0)
    if logdet < 10:
        print("number of spanning trees: %.2f" % (sign * np.exp(logdet)))
    else:
        print("number of spanning trees: exp(%.2f)" % logdet)
    print("--- %s seconds ---" % (time.time() - start_time))


def test_random_graphs(seed = None):
    start_time = time.time()
    print("Generating random graph...")
    g = get_random_connected_graph(5000, 0.2, seed=seed, max_degree=10)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Calulating MTT...")
    sign, logdet = MTT(g, use_log=True)
    assert(sign > 0)
    if logdet < 10:
        print("number of spanning trees: %.2f" % (sign * np.exp(logdet)))
    else:
        print("number of spanning trees: exp(%.2f)" % logdet)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    import time
    print("\n")
    test_complete_graphs()
    print("\n")
    test_random_graphs(seed = 1)
    print("\n")
    
