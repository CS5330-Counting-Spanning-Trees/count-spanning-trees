import random
from graphs import ST_counter, is_st
from mtt import MTT

# given a walk as a list of vertices
# returns a newwalk which has no loops
# uses -1 as a invalid value
def eraseLoops(walk):
    result = [-1] * (len(walk) + 1)
    ptr = 0
    seen = {}
    for v in walk:
        if v in seen:
            newptr = seen[v] # erase everything until this point
            for i in range(newptr+1, ptr): # remove these node from seen
                del seen[result[i]]
            ptr = newptr + 1

        else:
            result[ptr] = v # add to result
            seen[v] = ptr # record this location
            ptr += 1
        result[ptr] = -1 # do this to mark the next location

    # copy the result into an array of correct size
    res = []
    for x in result:
        if x == -1:
            return res
        else:
            res.append(x)
        
    return res

# class to sample random spanning trees
class STSampler:
    def __init__(self, g):  
        self.graph = g # graph is adjList stored in a dict

    def set_graph(self, g):
        self.graph = g

    # choose a neighbor of x in self.graph
    def chooseNeighbor(self, x):
        if x in self.graph:
            return random.choice(self.graph[x])
        else:
            print('This node is not in the graph!')
            return -1
        
    # starting from u, do a random walk until we meet the tree
    # assumes that u is not already part of the tree
    def findWalk(self, u, tree):
        walk = [u]
        while walk[-1] not in tree: # while not yet reached tree
            cur = walk[-1]
            nxt = self.chooseNeighbor(cur)
            walk.append(nxt)
        return walk
        
    # adds the found path to the tree
    def addPath(self, tree, path):
        for i in range(0, len(path) - 1):
            tree[path[i]] = [] # add all the vertices
        for i in range(0, len(path) - 1): # add the edges
            u = path[i]
            v = path[i+1]
            tree[u].append(v) # can be improved to check for duplicates
            tree[v].append(u)

    # removes a list of elements B from the set A
    # modifies A
    def remove(self, A, B):
        for x in B:
            A.discard(x)
            
    # returns a ST uniformly distributed
    # implements Wilson's algorithm
    def sample(self):
        unused = set(self.graph.keys())
        root = unused.pop() # choose last elem to be the root, choice of root does not matter
        tree = {} # we will construct this tree. It is in adjList form
        tree[root] = [] # tree is initially just the root

        while len(unused) > 0:
            u = random.sample(unused, 1)[0]
            walk = self.findWalk(u, tree)
            path = eraseLoops(walk)
            self.addPath(tree, path)
            self.remove(unused, path[:-1])

        return tree
        
def test_sampler():
    g = {}
    g[1] = [2, 4]
    g[2] = [1, 3, 4]
    g[3] = [2, 4, 6]
    g[4] = [1, 2, 3, 5]
    g[5] = [4, 6]
    g[6] = [3, 5]

    print('sample test')
    sp = STSampler(g)
    for i in range(10):
        t = sp.sample()
        print(is_st(t))


# tests the distribution of ST_sampler 
def test_st_count():
    g1 = {}
    g1[1] = [2, 6]
    g1[2] = [1, 3, 6]
    g1[3] = [2, 4, 5]
    g1[4] = [3, 5]
    g1[5] = [3, 4, 6]
    g1[6] = [1, 2, 5]

    stc = ST_counter()
    sampler = STSampler(g1)
    N = 1000
    for i in range(N):
        t = sampler.sample()
        stc.add_tree(t)
    print('Correct number of st = {}'.format(MTT(g1)))
    print('number of st seen = {}'.format(len(stc.counts)))
    print('The counts are:')
    print(stc.counts)

    g2 = {}
    g2[1] = [2, 6]
    g2[2] = [1, 3, 6]
    g2[3] = [2, 4, 5]
    g2[4] = [3, 5]
    g2[5] = [3, 4, 6]
    g2[6] = [1, 2, 5, 7]
    g2[7] = [6, 8, 9]
    g2[8] = [7, 9]
    g2[9] = [7, 8]

    stc = ST_counter()
    sampler = STSampler(g2)
    N = 10000
    for i in range(N):
        t = sampler.sample()
        stc.add_tree(t)
    print('Correct number of st = {}'.format(MTT(g2)))
    print('number of st seen = {}'.format(len(stc.counts)))
    print('The counts are:')
    print(stc.counts)
        
if __name__ == "__main__":
    test_sampler()