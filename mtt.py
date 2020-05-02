# Matrix tree theorem

import numpy as np
import copy, math

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

    #print(labels)
    matrix = []
    for r in range(n):
        u = vertices[r]
        row = [0] * n # create this row
        nbrs = graph[u]
        for v in nbrs:
            #print(r, v)
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

                
def MTT(graph, log=False):
    m = get_adj_matrix(graph)
    
    L = get_laplacian(m)
    
    # delete last row and col of L
    del L[-1]
    for row in L:
        del row[-1]
    
    # compute determinant
    arr = np.array(L)
    det = 0
    if log:
        det = np.linalg.slogdet(arr)
        return (det[1])
    else:
        det = np.linalg.det(arr)
        return int(round(det))
    #
    

def test():
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

    # log det
    d = MTT(g5, True)
    print(900 == int(round(pow(math.e, d))))

if __name__ == "__main__":
    test()