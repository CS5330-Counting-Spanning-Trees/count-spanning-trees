# Experiments for approximating the term NST(G_i) / NST(G_{i-1})
import pprint, copy, random, os, math
import db, graphs, plotting
import numpy as np
import pandas as pd
from mtt import MTT
from st_sampler import STSampler
from collections import defaultdict

# this is the main testing function
# g = graph
# edge = the edge removed to get g_minus_one_edge
# actual ratio = NST(g) / NST(g_minus_one_edge)
# num_samples = number of samples we will draw to calculate the estimate
def get_error(g, g_minus_one_edge, edge, actual_ratio, num_samples):
    sampler = STSampler(g)
    good = 0 # number of samples without the 'bad' edge
    for i in range(num_samples):
        t = sampler.sample()
        if not (edge[1] in t[edge[0]]): # doesnt contains bad edge
            good += 1
    r_est = num_samples / good
    mult_error = abs(r_est - actual_ratio) / actual_ratio
    return mult_error

def run_testsuite():
    # we gonna test for all number of vertices, density, and sample_sizes
    # for each pair (num_vertices, density) we have 10 graphs - we will take average over all of them
    test_dir = 'testsuite2'
    save_path = 'termwise2_plot_data.json'
    sample_sizes = [10, 50, 100, 200, 300, 400, 500]
    num_vertices_list = [20, 40, 60, 80, 100, 120]
    densities_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    graph_number_list = list(range(1, 11))

    # test_dir = 'testsuite3'
    # save_path = 'termwise3_plot_data.json'
    # sample_sizes = [10, 50, 100, 200]
    # num_vertices_list = [40, 60, 80]
    # densities_list = [0.3, 0.5, 0.7]
    # graph_number_list = list(range(1, 6))

    plotdata = defaultdict(list)
    for n in num_vertices_list:
        for density in densities_list:
            mult_error_table = np.zeros((len(graph_number_list), len(sample_sizes)))
            for gn in graph_number_list:
                filename = 'g{}_{}_{}.json'.format(gn, n, int(100 * density))
                path = (os.path.join(test_dir, filename))

                data = db.load_data(path) # has the form [g1, NST(g1), g2, NST(g2), (u, v)]

                g1 = db.fix_keys(data[0])
                nst1 = data[1]
                g2 = db.fix_keys(data[2])
                nst2 = data[3]
                e = data[4]

                if (nst2 == 0): # the graph got disconnected, discard this point
                    continue # this will skew our results a bit
                r = nst1 / nst2
                for i in range(len(sample_sizes)):
                    mult_error = get_error(g1, g2, e, r, sample_sizes[i]) * 100 # in percent
                    mult_error_table[gn-1][i] = mult_error

            # take average along cols of mult_error_table
            # covert to list and add to plot data
            errors = list(np.mean(mult_error_table, axis=0))
            dataset = list(zip(sample_sizes, errors))
            plotdata[str((n, density))] = dataset

    db.save_data(plotdata, save_path)

#####################################

def mult_error(est, actual):
    return abs(est - actual) / actual

# theoretical number of samples required to obtain a (eps/2m, delta/m)-approximation for each term
def calc_num_samples(g, eps, delta):
    n = len(g)
    m = graphs.num_edges(g)
    logterm = math.log(2 * m / delta, math.e)
    return round(12 * n * m**2 * logterm / eps**2)

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
            err = mult_error(num_samples / (denom), actual)
        if (err <= eps):
            break
        # print(mult_error(num_samples / (num_samples - has_e + 0.00000001), actual))
        sample = sampler.sample()
        if e[1] in sample[e[0]]:
            has_e += 1
        num_samples += 1

        if (num_samples % 200 == 0):
            print(f'taking sample no. {num_samples}, err = {err}, eps = {eps}')

    return num_samples

def avg_num_samples_for_eps(g, e, actual, eps, num_runs):
    total = 0
    for i in range(num_runs):
        print('run=', i)
        M = sample_till_error_less_than(g, e, eps, actual)
        total += M
    return total / num_runs

def run_tests_3():
    eps = 0.01
    ns = list(range(40, 190, 10))
    density = 0.3
    Ks = []
    for n in ns:
        K = get_num_samples_needed(n, density, eps)
        Ks.append(K)
    print(Ks)


def make_row(n, density):
    # params
    num_runs = 10
    final_eps = 0.01
    final_delta = 0.01
    iterations = 5
    steps = int(n * math.log(n, 2))

    g1 = graphs.get_random_connected_graph(n, density)
    g2 = copy.deepcopy(g1)
    e = graphs.pop_random_edge(g2)
    if not graphs.is_connected(g2):
        print('bad pop')
        return None

    # graph stats
    m = graphs.num_edges(g1)
    nst1 = MTT(g1)
    nst2 = MTT(g2)
    actual = nst1 / nst2
    degrees = graphs.get_degrees(g1)
    min_deg = min(degrees)
    max_deg = max(degrees)
    avg_deg = sum(degrees) / n
    hit_rate = graphs.get_hit_rate(g1, iterations, steps)
    
    eps = final_eps / (2 * m)
    delta = final_delta / m
    K = avg_num_samples_for_eps(g1, e, actual, eps, num_runs)

    row = [n, density, m, min_deg, max_deg, avg_deg, nst1, nst2, hit_rate, K]
    return row


if __name__ == "__main__":
    # path = 'testsuite2/g1_100_30.json'
    # data = db.load_data(path)
    # g1, nst1, g2, nst2, e = data
    # g1 = db.fix_keys(g1)
    # g2 = db.fix_keys(g2)
    # act = nst1 / nst2

    rows = []
    for n in range(70, 110, 10):
        for den in [0.2, 0.3]:
            for t in range(10):
                r = make_row(n, den)
                # r = [n+den] * 10
                if r:
                    rows.append(r)
    
    cols = ['n', 'density', 'edges', 'min deg', 'max deg', 'avg deg', 'nst1', 'nst2', 'hit rate', 'K']
    df = pd.DataFrame(rows, columns=cols)
    # print(df)
    df.to_csv('termwise3.csv')

    pass