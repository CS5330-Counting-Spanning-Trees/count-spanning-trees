# this module contains all the helper functions for working with graphs

import random, pprint, time
import numpy as np
from collections import defaultdict
import time

import numpy as np
from mtt import MTT

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
    for v in visited.values():
        if not v:
            return False
    return True

# given a graph g, counts the number of edges in the graph
# assumes g is undirected, so each edge appears twice
# useful for sanity checks
def num_edges(g):
    total = 0
    for v in g.values():
        total += len(v)
    return total // 2

def get_edges(g):
    edges = []
    for u, nbrs in g.items():
        for v in nbrs:
            edges.append((u,v))
    return edges

def is_st(g):
    # connected
    if is_connected(g) and num_edges(g) == len(g.keys()) - 1:
        return True
    else:
        return False

# checks that for each edge (u, v) in g, there is also (v, u) in g
def is_undirected(g):
    for u, nbrs in g.items():
        for v in nbrs:
            if not (u in g[v]):
                return False
    return True

def get_random_graph(n, density, max_degree, min_degree):
    g1 = {}
    for i in range(n):
        g1[i] = []
    for i in range(n):
        candidates = [x for x in range(i + 1, n)]
        random.shuffle(candidates)
        for j in candidates:
            if len(g1[i]) >= max_degree:
                break
            if len(g1[j]) >= max_degree:
                continue
            if len(g1[i]) < min_degree or random.random() < density:
                g1[i].append(j)
                g1[j].append(i)
    return g1

def get_random_connected_graph(n, density, seed = None, max_degree = np.inf, min_degree = 0):
    # set a fixed seed
    if seed is not None:
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

# chooses a random edge from g, removes it from g, and returns the edge
# modifies g
def pop_random_edge(g):
    e = get_random_edge(g)
    u, v = e
    g[u].remove(v)
    g[v].remove(u)
    return e

def del_edge(g, e):
    u, v = e
    g[u].remove(v)
    g[v].remove(u)

def tarjans(g):
    n = len(g)
    connections = get_edges(g)
    # g = collections.defaultdict(list)
    # for u, v in connections:
    #     g[u].append(v)
    #     g[v].append(u)

    N = len(connections)
    lev = [None] * N
    low = [None] * N

    def dfs(node, par, level):
        # already visited
        if lev[node] is not None:
            return

        lev[node] = low[node] = level
        for nei in g[node]:
            if not lev[nei]:
                dfs(nei, node, level + 1)

        # minimal level in the neignbors, exclude the parent
        cur = min([level] + [low[nei] for nei in g[node] if nei != par])
        low[node] = cur
        # print(low, lev)

    dfs(0, None, 0)

    ans = []
    for u, v in connections:
        if u >= v:
            continue
        if low[u] > lev[v] or low[v] > lev[u]:
            ans.append([u, v])
    return ans

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
    g = get_random_connected_graph(5, 1)
    sf = get_standard_form(g)
    pp = pprint.PrettyPrinter()
    pp.pprint(g)
    pp.pprint(sf)

    g = get_random_connected_graph(10, 0.3)
    sf = get_standard_form(g)
    pp = pprint.PrettyPrinter()
    pp.pprint(g)
    pp.pprint(sf)

    g = get_random_connected_graph(10, 0.3)
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
    for _ in range(n):
        d[random.randint(a, b)] += 1
    return d

# contracts g about the given edge
# modifies g
def contract(g, edge):
    u, v = edge

    v_nbrs = g.pop(v)
    v_nbrs.remove(u)
    u_nbrs = g[u]
    u_nbrs.remove(v)
    v_and_u = set(v_nbrs).union(set(u_nbrs))
    v_not_u = set(v_nbrs) - set(u_nbrs)
    v_int_u = set(v_nbrs).intersection(set(u_nbrs))

    for w in v_not_u: # merge v into u
        g[u].append(w)
    for w in v_not_u: # replace v by u
        g[w].remove(v)
        g[w].append(u)
    for w in v_int_u: # remove v
        g[w].remove(v)

def test_contract():
    g = {}
    g[1] = [4]
    g[2] = [4, 5]
    g[3] = [5]
    g[4] = [1, 2, 5, 6]
    g[5] = [2, 3, 4, 7]
    g[6] = [4]
    g[7] = [5, 8]
    g[8] = [7]

    printGraph(g)
    contract(g, (4, 5))
    printGraph(g)

def get_degrees(g):
    return [len(nbrs) for nbrs in g.values()]

# do a random walk on the graph and see what percentage of the graph we hit
# this is our attempt at a cheap heuristic to determine the cover time
def get_hit_rate(g, iterations, steps):
    hit_rates = []
    for _ in range(iterations):
        hit = set()
        v = random.sample(g.keys(), 1)[0] # choose random start vertex
        hit.add(v)
        for _ in range(steps):
            v = random.sample(g[v], 1)[0]
            hit.add(v)
        hit_rate = len(hit) / len(g)
        hit_rates.append(hit_rate)
    return np.mean(hit_rates)

if __name__ == "__main__":
    pass
    g = get_random_connected_graph(130, 0.8)
    # d = get_degrees(g)
    # print(d)

    hr = get_hit_rate(g, 30, 130 * 7)
    print(hr)
