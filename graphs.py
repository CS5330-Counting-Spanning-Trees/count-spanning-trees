import random
import pprint
from collections import defaultdict
from mtt import MTT

# given a graph g, counts the number of edges in the graph
# assumes g is undirected, so each edge appears twice
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

def make_random_graph(n, density):
    # we want the graph to be connected, so we start with a spanning tree
    g = make_random_st(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if j in g[i]:
                continue
            if random.random() < density:
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
