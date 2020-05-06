import random, math, collections, copy, time
from fractions import Fraction
from decimal import Decimal
from collections import defaultdict
import graphs, st_sampler, mtt, db
import pandas as pd

def make_graph():
    filename = 'mygraph.json'
    n = 10
    den = 0.3
    g = graphs.get_random_connected_graph(n, den)
    db.save_data(g, filename)

def get_graph():
    filename = 'mygraph.json'
    g = db.load_data(filename)
    g = db.fix_keys(g)
    return g

def test():
    #g = get_graph()
    #nst = mtt.MTT(g)
    #print(nst)

    g = {}
    g[0] = [2, 4]
    g[1] = [3, 5]
    g[2] = [0, 3, 4]
    g[3] = [1, 2, 5]
    g[4] = [0, 2]
    g[5] = [1, 3]

    print(graphs.tarjans(g))

    g = graphs.get_random_connected_graph(1000, 7/1000)

    blist = graphs.tarjans(g)
    for b in blist:
        g2 = copy.deepcopy(g)
        graphs.del_edge(g2, b)
        print(graphs.is_connected(g2))


