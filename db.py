# this file contains functions to store graphs that we have generated
# main functions are save_data and load_data

import json
import pprint
import os
import random
import copy
from graphs import make_complete_graph, make_random_graph

# filename = "saved_graphs.json"
# subdir = 'graphs'

def save_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

# json will save dict keys as strings, even though they are ints
# so when loading a dict from json, need to convert the keys back to ints
# returns the fixed dictionary
def fix_keys(g):
    g_int = {}
    for k, v in g.items():
        try:
            d = int(k)
        except ValueError:
            d = k
        g_int[d] = v
    return g_int

# def save_graph_as(gname, g):
#     # gname shud be mygraph.json
#     # saves graph in graphs/gname file
#     # it will overwrite existing files without msg!!!
#     filepath = os.path.join(subdir, gname)
#     with open(filepath, "w") as f:
#         json.dump(g, f)

# def load_graph(gname):
#     # load the named graph, if it exists
#     filepath = os.path.join(subdir, gname)
#     if not os.path.isfile(filepath):
#         print('No such file', gname)
#         return None
#     with open(filepath, "r") as f:
#         g = json.load(f)
#         # json will save dict keys as strings, even though they are ints
#         # so need to convert the keys back to ints
#         g_int = {}
#         for k, v in g.items():
#             try:
#                 d = int(k)
#             except ValueError:
#                 d = k
#             g_int[d] = v
#         return g_int

# def num_edges(g): # assumes undirected
#     total = 0
#     for k, v in g.items():
#         total += len(v)
#     return total // 2

# # i use this fn to insert stuff into database
# def insert():
#     n = 40
#     density = 0.5
#     g1 = {}
#     for i in range(n):
#         g1[i] = []
#     for i in range(n):
#         for j in range(n):
#             if not (i < j):
#                 continue
#             if random.random() < density:
#                 g1[i].append(j)
#                 g1[j].append(i)
    
#     u = 0
#     v = g1[u][0]
#     g2 = copy.deepcopy(g1)
#     g2[u].remove(v)
#     g2[v].remove(u)
#     print(num_edges(g1))
#     print(num_edges(g2))

#     save_graph_as("g5.json", g1)
#     save_graph_as("g6.json", g2)
