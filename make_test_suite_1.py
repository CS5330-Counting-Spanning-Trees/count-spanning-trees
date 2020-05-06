# the python code here is to generate the test suite for testing the approximation of NST(G_i) / NST(G_{i-1})
# each json file in the testsuite indicates the number of vertices and the density
# each json file contains a list [g1, NST(g1), g2, NST(g2), (u, v)]
# where g1 is a graph, and g2 is g1 with the edge (u,v) removed

import db
import random_graphs
import mtt
import os, copy, random

def get_random_edge(g):
    random_u = random.choice(list(g.keys()))
    random_v = random.choice(g[random_u]) # g[u] is not empty, assuming g is connected
    return (random_u, random_v)

subdir = 'testsuite2'
num_vertices_list = [20, 40, 60, 80, 100, 120]
densities_list = [0.1, 0.3, 0.5, 0.7, 0.9]
graph_number_list = list(range(1, 11))

# subdir = 'testsuite3'
# sample_sizes = [10, 50, 100, 200]
# num_vertices_list = [40, 60, 80]
# densities_list = [0.3, 0.5, 0.7]
# graph_number_list = list(range(1, 6))

try:
    os.mkdir(subdir)
    print("Directory " , subdir ,  " Created ")
except FileExistsError:
    print("Directory " , subdir ,  " already exists")

for n in num_vertices_list:
    for p in densities_list:
        for i in graph_number_list: # i gonna make 10 graphs of the same type (num_vertices and density)
            filename = 'g{}_{}_{}.json'.format(i, n, int(100*p))
            path = os.path.join(subdir, filename)

            g1 = random_graphs.get_random_connected_graph(n, p)
            u, v = get_random_edge(g1)

            g2 = copy.deepcopy(g1)
            g2[u].remove(v) # remove (u,v) from g2. there is a small chance that this disconnects the graph
            g2[v].remove(u)

            NST1 = mtt.MTT(g1)
            NST2 = mtt.MTT(g2)

            data = [g1, NST1, g2, NST2, [u,v]]

            db.save_data(data, path)
