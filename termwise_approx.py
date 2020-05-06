# Experiments for approximating the term NST(G_i) / NST(G_{i-1})
import pprint, copy, random, os, math, time
import db, random_graphs, plotting
import numpy as np
import pandas as pd
from mtt import MTT
from st_sampler import STSampler
from collections import defaultdict
from fractions import Fraction
from decimal import Decimal

def mult_error(est, actual):
    return abs(est - actual) / actual

def mult_error_log(log_est, log_actual):
    return math.exp(log_est - log_actual) - 1

# theoretical number of samples required to obtain a (eps/2m, delta/m)-approximation for each term
def calc_num_samples(g, eps, delta):
    n = len(g)
    m = random_graphs.num_edges(g)
    logterm = math.log(2 * m / delta, math.e)
    return round(12 * n * m**2 * logterm / eps**2)

# draws samples until the error is within eps of the true value actual
def sample_till_error_less_than(g, e, eps, actual):
    upper_limit = 100000
    sampler = STSampler(g)
    has_e = 0
    num_samples = 0
    err = 0
    while(num_samples < upper_limit):
        denom = num_samples - has_e
        if denom == 0:
            err = 1
        else:
            err = mult_error(Decimal(num_samples) / Decimal(denom), actual)
        if (err <= eps):
            break
        sample = sampler.sample()
        if e[1] in sample[e[0]]:
            has_e += 1
        num_samples += 1

        if (num_samples % 200 == 0):
            print(f'taking sample no. {num_samples}, err = {err}, eps = {eps}')

    return num_samples

def avg_num_samples_for_eps(g, e, actual, eps, num_runs, log=False):
    total = 0
    for i in range(num_runs):
        print('run=', i)
        M = sample_till_error_less_than(g, e, eps, actual, log)
        total += M
    return total / num_runs

def make_row(n, density):
    # params
    final_eps = 0.01
    final_delta = 0.01
    iterations = 5
    steps = int(n * math.log(n, 2))

    g1 = random_graphs.get_random_connected_graph(n, density)
    g2 = copy.deepcopy(g1)
    e = random_graphs.pop_random_edge(g2)
    if not random_graphs.is_connected(g2):
        print('bad pop')
        return None

    # graph stats
    m = random_graphs.num_edges(g1)
    nst1 = MTT(g1)
    nst2 = MTT(g2)
    actual = Decimal(nst1) / Decimal(nst2)
    degrees = random_graphs.get_degrees(g1)
    min_deg = min(degrees)
    max_deg = max(degrees)
    avg_deg = sum(degrees) / n
    hit_rate = random_graphs.get_hit_rate(g1, iterations, steps)

    eps = final_eps / (2 * m)
    delta = final_delta / m
    t0 = time.time()
    K = sample_till_error_less_than(g1, e, eps, actual)
    t1 = time.time()

    row = [n, density, m, min_deg, max_deg, avg_deg, nst1, nst2, hit_rate, K, t1-t0]
    return row

fjson = 'rows1_batch2.json'
fcsv = fcsv = 'rows1_batch2.json'


# we want find K for various graphs n with density 10 / n
def gen_data():
    ns = list(range(30, 150, 10))
    rows = db.load_data(fjson)
    for n in ns:
        try:
            density = 10 / n
            r = make_row(n, density)
            print('row:', r)
            rows.append(r)
            db.save_data(rows, fjson) # allows termination at any time
        except KeyboardInterrupt:
            raise
        except:
            pass

def make_csv():
    rows = db.load_data(fjson)
    cols = ['n', 'density', 'm', 'min deg', 'max deg', 'avg deg', 'nst1', 'nst2', 'hit rate', 'K', 'time']
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    df.to_csv(fcsv)

if __name__ == "__main__":
    make_csv()
