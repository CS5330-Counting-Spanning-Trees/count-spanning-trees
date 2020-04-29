from collections import defaultdict
from graph import Graph
from mtt import MTT
from math import log, exp

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
    stack = [(u, 0), (v, 0)]
    visited = set([u, v])
    # do a dfs to get the set of edges that are within range
    while len(stack) > 0:
        curr, depth = stack.pop()
        if depth == max_depth:
            continue
        adj_edges = g.get_edge_indices(curr)
        for idx in adj_edges:
            neighborhood_edges.add(idx)
            neighbor = g.neighbor(curr, idx)
            if neighbor in visited:
                continue
            visited.add(neighbor)
            stack.append((neighbor, depth + 1))
    # construct the adj list
    return edges_to_adj_list(g, neighborhood_edges)

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
    neighborhood = get_neighborhood(g, edge_idx, explore_factor)
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
        explore_factor = min(20, len(g_vertices))
        neighborhood = get_neighborhood(g, edge_idx, explore_factor)
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


def test_get_neighborhood():
    g_adj_list = {
        1: [2, 3, 4],
        2: [1, 3],
        3: [1, 2],
        4: [1, 5],
        5: [4, 6],
        6: [5],
    }
    g = Graph(g_adj_list)
    edge_idx = g.get_edge_between_vertices(2, 3)
    n = get_neighborhood(g, edge_idx, 2)
    print(n)
    g.contract(edge_idx)
    edge_idx = g.get_edge_between_vertices(1, 2)
    n = get_neighborhood(g, edge_idx, 2)
    print(n)
    num_st = MTT(n)
    print(f"MTT: {num_st}")


if __name__ == "__main__":
    test_get_neighborhood()
