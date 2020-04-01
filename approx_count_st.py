import random
from fractions import Fraction
from collections import defaultdict
from mc_sampler import MCSampler

def get_initial_st_dfs(g, v, visited, st):
    visited.add(v)
    neighbors = g[v][:]
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if neighbor not in visited:
            st[neighbor].append(v)
            st[v].append(neighbor)
            get_initial_st_dfs(g, neighbor, visited, st)

def get_initial_st(g):
    root = random.sample(g.keys(), 1)[0]
    visited = set()
    st = defaultdict(list)
    get_initial_st_dfs(g, root, visited, st)
    return st

def get_remaining_edges(g, st):
    edges = []
    for v, neighbors in g.items():
        for neighbor in neighbors:
            if v > neighbor:
                # every edge is represented twice in g
                # to avoid double counting, we only consider edges for v < neighbor
                continue
            if neighbor in st[v]:
                # don't include edges in the st
                continue
            edge = (v, neighbor)
            edges.append(edge)
    random.shuffle(edges)
    return edges

def approx_count_st(g, rounds, samples):
    g_i = get_initial_st(g)
    remaining_edges = get_remaining_edges(g, g_i)
    # the initial graph has only 1 st
    result = 1
    for new_edge in remaining_edges:
        # add the remaining edges until we get back the original graph
        u, v = new_edge
        g_i[u].append(v)
        g_i[v].append(u)
        # denominator is the number of samples that are also st for g without the new edge
        denominator = 0
        for _ in range(samples):
            sampler = MCSampler(g_i)
            sample = sampler.sample(rounds)
            if u not in sample[v]:
                denominator += 1
        result *= Fraction(samples, denominator)
    return float(result)
