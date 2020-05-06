# this file contains functions to store graphs that we have generated
# main functions are save_data and load_data
# Usage of fix_keys: If you load a dict with integer keys from json, call d = fix_keys(d) to
# convert the keys back to ints

import json, os
import pandas as pd

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

if __name__ == "__main__":
    # p = 'overnight.json'
    # #save_data([], p)
    # rows = load_data(p)
    # print(rows)
    # cols = ['n', 'density', 'edges', 'min deg', 'max deg', 'avg deg', 'log nst1', 'log nst2', 'hit rate', 'K']
    # df = pd.DataFrame(rows, columns=cols)
    # print(df)
    # df.to_csv('log_termwise3.csv')
    pass