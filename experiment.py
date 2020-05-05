from wilson_sampler import WilsonSampler
from st_sampler import STSampler
from mtt import MTT
from graph import Graph
from math import log
from random_graphs import get_random_connected_graph
import random

def get_actual_p(g, edge_idx):
    adj_list = g.to_adj_list()
    total_st = MTT(adj_list, use_log=True)
    # make a copy to avoid mutating g
    g_copy = Graph(adj_list)
    u, v = g.get_edge(edge_idx)
    g_copy.contract(g_copy.get_edge_between_vertices(u, v))
    with_e_st = MTT(g_copy.to_adj_list(), use_log=True)
    p = with_e_st - total_st
    return p

def get_sample_p(g, edge_idx, samples):
    sampler = STSampler(g)
    has_e = 0
    for _ in range(samples):
        st = sampler.sample()
        if edge_idx in st:
            has_e += 1
    p = log(has_e / samples)
    return p

def get_sample_p_wilsons(g, edge_idx, samples):
    sampler = WilsonSampler(g)
    has_e = 0
    for _ in range(samples):
        st = sampler.sample()
        if edge_idx in st:
            has_e += 1
    p = log(has_e / samples)
    return p

def test(g, samples, rounds):
    edge_idx = g.get_all_edge_indcies()[0]
    actual_p = get_actual_p(g, edge_idx)
    total = 0
    print("RANDOM WALK")
    for _ in range(rounds):
        sample_p = get_sample_p(g, edge_idx, samples)
        diff = actual_p - sample_p
        total += diff
        print(diff)
    print(f"avg: {total / rounds}")


    total = 0
    print("WILSONS")
    for _ in range(rounds):
        sample_p = get_sample_p_wilsons(g, edge_idx, samples)
        diff = actual_p - sample_p
        total += diff
        print(diff)
    print(f"avg: {total / rounds}")

if __name__ == "__main__":
    adj_list = get_random_connected_graph(100, 0.1, seed=0)
    g = Graph(adj_list)
    # test(g, 100, 10)
    # do some contractions
    for _ in range(80):
        edge_idx = random.sample(g.get_all_edge_indcies(), 1)[0]
        g.contract(edge_idx)
    print("------")
    test(g, 100, 100)
