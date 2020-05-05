from collections import defaultdict, deque
from graph import Graph
from random_graphs import get_random_connected_graph
from mtt import MTT
from math import log, exp
import time
import random

def edges_to_adj_list(g, edges):
    adj_list = defaultdict(list)
    for idx in edges:
        u, v = g.get_edge(idx)
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list

def get_neighborhood(g, edge_idx, max_depth):
    neighborhood_edges = set([edge_idx])
    u, v = g.get_edge(edge_idx)
    # store entries in the form (vertex, depth)
    queue = deque([(u, 0), (v, 0)])
    visited = set([u, v])
    # do a dfs to get the set of edges that are within range
    while len(queue) > 0:
        curr, depth = queue.popleft()
        if depth == max_depth:
            continue
        adj_edges = g.get_edge_indices(curr)
        for idx in adj_edges:
            neighborhood_edges.add(idx)
            neighbor = g.neighbor(curr, idx)
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append((neighbor, depth + 1))
    return neighborhood_edges

def approx_count_st_rec(g):
    g_edges = g.get_all_edge_indcies()
    g_vertices = g.get_vertices()
    if len(g_edges) == len(g_vertices) - 1:
        return 0
    edge_idx = g_edges[0]
    u, v = g.get_edge(edge_idx)
    # look around the neighborhood of the edge and count
    # number of ST in the neighborhood
    explore_factor = min(20, len(g_vertices))
    neighborhood_edges = get_neighborhood(g, edge_idx, explore_factor)
    neighborhood = edges_to_adj_list(g, neighborhood_edges)
    neighborhood_st = MTT(neighborhood, use_log=True)
    # contract that edge from the neighborhood, and count
    # number of ST with the contracted edge
    # this isn't very efficient, but let's try this for now
    neighborhood_g = Graph(neighborhood)
    neighborhood_edge_idx = neighborhood_g.get_edge_between_vertices(u, v)
    neighborhood_g.contract(neighborhood_edge_idx)
    neighborhood_with_e = neighborhood_g.to_adj_list()
    neighborhood_with_e_st = MTT(neighborhood_with_e, use_log=True)
    p = neighborhood_with_e_st - neighborhood_st
    if p > log(0.5):
        g.contract(edge_idx)
        approx_count_with_e = approx_count_st_rec(g)
        return approx_count_with_e - p
    else:
        g.remove_edge(edge_idx)
        approx_count_without_e = approx_count_st_rec(g)
        q = log(1 - exp(p))
        return approx_count_without_e - q


def approx_count_st(g):
    denominator = 0
    while True:
        g_edges = g.get_all_edge_indcies()
        g_vertices = g.get_vertices()
        if len(g_edges) == len(g_vertices) - 1:
            break
        edge_idx = g_edges[0]
        u, v = g.get_edge(edge_idx)
        # look around the neighborhood of the edge and count
        # number of ST in the neighborhood
        # explore_factor = min(20, len(g_vertices))
        explore_factor = 5
        neighborhood_edges = get_neighborhood(g, edge_idx, explore_factor)
        neighborhood = edges_to_adj_list(g, neighborhood_edges)
        neighborhood_st = MTT(neighborhood, use_log=True)
        # contract that edge from the neighborhood, and count
        # number of ST with the contracted edge
        # this isn't very efficient, but let's try this for now
        neighborhood_g = Graph(neighborhood)
        neighborhood_edge_idx = neighborhood_g.get_edge_between_vertices(u, v)
        neighborhood_g.contract(neighborhood_edge_idx)
        neighborhood_with_e = neighborhood_g.to_adj_list()
        if len(neighborhood_with_e) == 0:
            neighborhood_with_e_st = 0
        else:
            neighborhood_with_e_st = MTT(neighborhood_with_e, use_log=True)
        p = neighborhood_with_e_st - neighborhood_st
        if p > log(0.5):
            g.contract(edge_idx)
            denominator += p
        else:
            g.remove_edge(edge_idx)
            q = log(1 - exp(p))
            denominator += q
    return -denominator

def test_accuracy(n, density, seed, max_degree):
    print(
        f"Running with n: {n}, density: {density}, seed: {seed}, max_degree: {max_degree}")
    adj_list = get_random_connected_graph(
        n, density, seed, max_degree=max_degree)
    g = Graph(adj_list)
    g_edges = g.get_all_edge_indcies()
    edge_idx = g_edges[0]
    u, v = g.get_edge(edge_idx)

    # test_neighborhood(g, edge_idx)

    # calculate the actual p
    total_st = MTT(adj_list, use_log=True)
    # use a copy of the graph since we need the unmodified graph later
    g_copy = Graph(adj_list)
    g_copy.contract(g_copy.get_edge_between_vertices(u, v))
    with_e_st = MTT(g_copy.to_adj_list(), use_log=True)
    p = with_e_st - total_st

    explore_factor = 1
    while explore_factor < 10:
        start = time.time_ns()
        neighborhood_edges = get_neighborhood(g, edge_idx, explore_factor)
        neighborhood = edges_to_adj_list(g, neighborhood_edges)
        neighborhood_st = MTT(neighborhood, use_log=True)
        neighborhood_g = Graph(neighborhood)
        neighborhood_edge_idx = neighborhood_g.get_edge_between_vertices(u, v)
        neighborhood_g.contract(neighborhood_edge_idx)
        neighborhood_with_e = neighborhood_g.to_adj_list()
        neighborhood_with_e_st = MTT(neighborhood_with_e, use_log=True)
        end = time.time_ns()
        elapsed_ms = (end - start) / (10 ** 6)
        p_est = neighborhood_with_e_st - neighborhood_st
        error = abs(1 - exp(p - p_est))
        neighborhood_edge_size = len(neighborhood_edges)
        neighborhood_vertex_size = len(neighborhood)
        print(
            f"with depth {explore_factor} achieved error {error:.16f} ({elapsed_ms} ms) (neighborhood vertices: {neighborhood_vertex_size}) (neighborhood edges: {neighborhood_edge_size})")
        explore_factor += 1


def test_neighborhood_size():
    for n in [100, 500, 1000, 5000, 10000]:
        adj_list = get_random_connected_graph(n, 0.1, seed=0, max_degree=5)
        g = Graph(adj_list)
        g_edges = g.get_all_edge_indcies()
        edge_idx = g_edges[0]
        u, v = g.get_edge(edge_idx)

        # calculate the actual p
        total_st = MTT(adj_list, use_log=True)
        # use a copy of the graph since we need the unmodified graph later
        g_copy = Graph(adj_list)
        g_copy.contract(g_copy.get_edge_between_vertices(u, v))
        with_e_st = MTT(g_copy.to_adj_list(), use_log=True)
        p = with_e_st - total_st

        explore_factor = 1
        threshold = 0.001
        while True:
            start = time.time_ns()
            neighborhood_edges = get_neighborhood(g, edge_idx, explore_factor)
            neighborhood = edges_to_adj_list(g, neighborhood_edges)
            neighborhood_st = MTT(neighborhood, use_log=True)
            neighborhood_g = Graph(neighborhood)
            neighborhood_edge_idx = neighborhood_g.get_edge_between_vertices(u, v)
            neighborhood_g.contract(neighborhood_edge_idx)
            neighborhood_with_e = neighborhood_g.to_adj_list()
            neighborhood_with_e_st = MTT(neighborhood_with_e, use_log=True)
            end = time.time_ns()
            elapsed_ms = (end - start) / (10 ** 6)
            p_est = neighborhood_with_e_st - neighborhood_st
            error = abs(1 - exp(p - p_est))
            neighborhood_vertex_size = len(neighborhood)
            if error < threshold:
                print(f"for n = {n}, hit threshold of {threshold} with explore depth {explore_factor} ({elapsed_ms} ms) (neighberhood size: {neighborhood_vertex_size})")
                break
            explore_factor += 1
