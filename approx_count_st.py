import random
from graph import Graph
from fractions import Fraction
from collections import defaultdict
from st_sampler import STSampler

def approx_count_st(g):
    num_edges = len(g.get_all_edge_indcies())
    num_vertices = len(g.get_vertices())
    # assume g is connected. if |E| = |V| - 1, then there is only 1 st
    if num_edges == num_vertices - 1:
        return 1
    # select any edge in g
    # we arbitrarily select the first edge in the list
    e = g.get_all_edge_indcies()[0]
    # we sample k st from g and see how many has the edge
    # for now we use k = 100
    # TODO(marvin): use adaptive sampling
    k = 1000
    sampler = STSampler(g)
    has_e = 0
    for _ in range(k):
        st = sampler.sample()
        if e in st:
            has_e += 1
    p = Fraction(has_e, k)
    # if more than half has e,
    # then we recurse with e fixed to be in the st
    if p > 0.5:
        g.contract(e)
        approx_count_with_e = approx_count_st(g)
        return Fraction(approx_count_with_e, p)
    # otherwise more than half doesn't have e,
    # then we recurse with e fixed not to be in the st
    g.remove_edge(e)
    approx_count_without_e = approx_count_st(g)
    return Fraction(approx_count_without_e, (1 - p))


if __name__ == "__main__":
    adj_matrix = {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3]}
    g = Graph(adj_matrix)
    count = approx_count_st(g)
    print(int(count))
