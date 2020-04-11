# Experiments for approximating the term NST(G_i) / NST(G_{i-1})
import pprint, copy, random, os
import db, graphs
from mtt import MTT
from st_sampler import STSampler

subdir = 'testsuite1'
filename = 'g_100_70.json'
path = os.path.join(subdir, filename)
data = db.load_data(path) # has the form [g1, NST(g1), g2, NST(g2), (u, v)]

g1 = db.fix_keys(data[0])
nst1 = data[1]
g2 = db.fix_keys(data[2])
nst2 = data[3]
e = data[4]

r = nst1 / nst2

sampler = STSampler(g1)
num_samples = 1000
good = 0
for i in range(num_samples):
    t = sampler.sample()
    if not (e[1] in t[e[0]]): # doesnt contains bad edge
        good += 1
r_est = num_samples / good

# graphs.printGraph(g1)
# graphs.printGraph(g2)

print('actual = {}; estimated = {}, ratio = {}'.format(r, r_est, r / r_est))

