# Experiments for approximating the term NST(G_i) / NST(G_{i-1})
import pprint, copy, random, os
import db, graphs, plotting
import numpy as np
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

def run_tests():
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

# fetch data from data_path
# plots the data, then saves the plot to save_path
def plot__data(data_path, save_path)
    data = db.load_data(data_path)
    plotting.plot_data_and_save(data, save_path)

# todo: write code to make some plotz