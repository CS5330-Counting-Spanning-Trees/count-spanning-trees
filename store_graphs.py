# this file contains functions to store graphs that we have generated
# it will save them as json in the file
# the json stores a list of graphs
# use get_graphs to get a list of saved graphs
# append whatever u want to this list
# use save_graphs to save all the graphs again

import json
import pprint
from graphs import make_complete_graph, make_random_graph

filename = "saved_graphs.json"

def get_graphs():
    if filename:
        with open(filename, 'r') as f:
            data = json.load(f)
    return data

def save_graphs(data):
    if filename:
        with open(filename, 'w') as f:
            json.dump(data, f)

def print_all_graphs():
    graphs = get_graphs()
    pp = pprint.PrettyPrinter()
    for g in graphs:
        pp.pprint(g)
