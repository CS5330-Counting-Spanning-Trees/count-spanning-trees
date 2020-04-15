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
    mult_error = abs(r_est - r) / r
    return mult_error

# we gonna test for all number of vertices, density, and sample_sizes
# test_dir = 'testsuite2'
# sample_sizes = [10, 50, 100, 200]
# num_vertices_list = [20, 40, 60, 80, 100, 120]
# densities_list = [0.1, 0.3, 0.5, 0.7, 0.9]
# graph_number_list = list(range(1, 11))

test_dir = 'testsuite3'
sample_sizes = [10, 50, 100, 200]
num_vertices_list = [40, 60, 80]
densities_list = [0.3, 0.5, 0.7]
graph_number_list = list(range(1, 6))

# where we will save the plotted data
save_dir = 'pics'
save_filename = 'termwise3.png'
save_path = (os.path.join(save_dir, save_filename))

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

            r = nst1 / nst2
            for i in range(len(sample_sizes)):
                mult_error = get_error(g1, g2, e, r, sample_sizes[i]) * 100 # in percent
                mult_error_table[gn-1][i] = mult_error
            
        # take average along cols of mult_error_table
        # covert to list and add to plot data
        errors = list(np.mean(mult_error_table, axis=0))
        dataset = list(zip(sample_sizes, errors))
        plotdata[str((n, density))] = dataset

        
print(plotdata)
plotting.plot_data_and_save(plotdata, save_path)




