import math
import numpy as np

rng = np.random.default_rng()
randoms = []
idx = 0

def get_random(n):
    global rng
    global randoms
    global idx
    if idx == len(randoms):
        randoms = rng.random(size=10000)
        idx = 0
    rand = randoms[idx]
    idx += 1
    return int(n * rand)
