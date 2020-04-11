# the python code here is to generate the test suite for testing the approximation of NST(G_i) / NST(G_{i-1})
# each json file in the testsuite indicates the number of vertices and the density
# each json file contains a list [g1, NST(g1), g2, NST(g2), (u, v)]
# where g1 is a graph, and g2 is g1 with the edge (u,v) removed

import db
import graphs
import mtt
import os, copy, random

def get_random_edge(g):
    random_u = random.choice(list(g.keys()))
    random_v = random.choice(g[random_u]) # g[u] is not empty, assuming g is connected
    return (random_u, random_v)

num_vertices_list = [20, 50, 100, 120]
densities_list = [0.1, 0.3, 0.5, 0.7]
subdir = 'testsuite1'

try:
    os.mkdir(subdir)
    print("Directory " , subdir ,  " Created ") 
except FileExistsError:
    print("Directory " , subdir ,  " already exists")

for n in num_vertices_list:
    for p in densities_list:
        filename = 'g_{}_{}.json'.format(n, int(100*p))
        path = os.path.join(subdir, filename)

        g1 = graphs.get_random_connected_graph(n, p)
        u, v = get_random_edge(g1)
        
        g2 = copy.deepcopy(g1)
        g2[u].remove(v) # remove (u,v) from g2
        g2[v].remove(u)

        NST1 = mtt.MTT(g1)
        NST2 = mtt.MTT(g2)

        data = [g1, NST1, g2, NST2, [u,v]]

        db.save_data(data, path)
