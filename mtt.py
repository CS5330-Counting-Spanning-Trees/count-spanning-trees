# Matrix tree theorem

import numpy as np
import copy

def print2d(matrix):
    for r in matrix:
        print(r)

# given a graph as adjList
# returns the adj matrix of the graph
# right now, just gonna arbitrarily label the vertices by 0 to n-1
def get_adj_matrix(graph):
    n = len(graph)
    vertices = [] # label[i] stores the actual vertex that we have relabel to i
    
    for u in graph.keys(): # first find all the vertices
        vertices.append(u)

    labels = {} # labels stores the reverse mapping, from vertex to its number
    for i in range(len(vertices)):
        labels[vertices[i]] = i

    matrix = []
    for r in range(n):
        u = vertices[r]
        row = [0] * n # create this row
        nbrs = graph[u]
        for v in nbrs:
            row[labels[v]] = 1
        matrix.append(row)
    return matrix

def get_laplacian(adj_matrix):
    L = copy.deepcopy(adj_matrix)
    for i in range(len(L)):
        row = L[i]
        degree = 0
        for j in range(len(row)):
            if row[j] == 1: # flip all signs in the row
                degree += 1
                row[j] = -1
        row[i] = degree
    return L

                
def MTT(graph):
    m = get_adj_matrix(graph)
    
    L = get_laplacian(m)
    
    # delete last row and col of L
    del L[-1]
    for row in L:
        del row[-1]
    
    # compute determinant
    arr = np.array(L)
    det = np.linalg.det(arr)
    return int(round(det))

def test():
    g = {}
    g[1] = [2, 4]
    g[2] = [1, 3, 4]
    g[3] = [2, 4, 6]
    g[4] = [1, 2, 3, 5]
    g[5] = [4, 6]
    g[6] = [3, 5]

    print(MTT(g))

    # complete graph with 4 vertices
    g2 = {}
    g2[1] = [2, 3, 4]
    g2[2] = [1, 3, 4]
    g2[3] = [1, 2, 4]
    g2[4] = [1, 2, 3]

    print(MTT(g2)) # shud be 4**2 =16

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
    
    m = get_adj_matrix(g3)
    print2d(m)
    L = get_laplacian(m)
    print2d(L)
    
    print(MTT(g3)) # shud be 16 ** 2 = 256
        
test()
