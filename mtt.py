# Matrix tree theorem

import numpy as np
import copy

def print2d(matrix):
    for r in matrix:
        print(r)

def get_mapping(vertices):
    mapping = {}
    idx = 0
    for v in vertices:
        mapping[v] = idx
        idx += 1
    return mapping

# returns the laplacian matrix without the last row and column
def get_laplacian_prime(adj_list):
    n = len(adj_list) - 1
    matrix = np.zeros((n, n), dtype=int)
    mapping = get_mapping(adj_list.keys())
    for u in adj_list:
        u_idx = mapping[u]
        if u_idx == n:
            continue
        neighbors = adj_list[u]
        degree = len(neighbors)
        matrix[u_idx][u_idx] = degree
        for v in adj_list[u]:
            v_idx = mapping[v]
            if v_idx == n:
                continue
            matrix[u_idx][v_idx] -= 1
    return matrix

# return in natural log scale, if the use_log flag is set
def MTT(adj_list, use_log = False):
    L = get_laplacian_prime(adj_list)
    # compute determinant
    if use_log:
        _, logdet = np.linalg.slogdet(L)
        return logdet
    else:
        det = np.linalg.det(L)
        return int(round(det))

def test_mtt():
    # cycle graph
    g1 = {}
    g1[1] = [2, 4]
    g1[2] = [1, 3]
    g1[3] = [2, 4]
    g1[4] = [3, 1]
    print(MTT(g1) == 4)

    # complete graph with 4 vertices
    g2 = {}
    g2[1] = [2, 3, 4]
    g2[2] = [1, 3, 4]
    g2[3] = [1, 2, 4]
    g2[4] = [1, 2, 3]
    print(MTT(g2) == 16)

    # two copies of K_4, joined together by vertex 9
    g3 = {}
    g3[1] = [2, 3, 4]
    g3[2] = [1, 3, 4]
    g3[3] = [1, 2, 4]
    g3[4] = [1, 2, 3, 9]
    g3[5] = [6, 7, 8, 9]
    g3[6] = [5, 7, 8]
    g3[7] = [5, 6, 8]
    g3[8] = [5, 6, 7]
    g3[9] = [4, 5]
    print(MTT(g3) == 256)

    # hexagon with 2 lines
    g4 = {}
    g4[1] = [2, 6]
    g4[2] = [1, 3, 6]
    g4[3] = [2, 4, 5]
    g4[4] = [3, 5]
    g4[5] = [3, 4, 6]
    g4[6] = [1, 2, 5]
    print(MTT(g4) == 30) # hand-calculate there are 30 ways

    # 2 copies of hexagon with 2 lines
    g5 = {}
    g5[1] = [2, 6]
    g5[2] = [1, 3, 6]
    g5[3] = [2, 4, 5]
    g5[4] = [3, 5]
    g5[5] = [3, 4, 6]
    g5[6] = [1, 2, 3, 7]
    g5[7] = [8, 11, 12, 6]
    g5[8] = [7, 9, 10]
    g5[9] = [8, 10]
    g5[10] = [9, 8, 11]
    g5[11] = [7, 10, 12]
    g5[12] = [7, 11]
    print(MTT(g5) == 900)

if __name__ == "__main__":
    test_mtt()
