import math
import numpy as np

rng = np.random.default_rng()
randoms = []
idx = 0

# Pregenerate random numbers between [0, 1) and cache them to reduce
# overhead of getting random numbers
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
