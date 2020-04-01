import random

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
        unused = set(g.keys())
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

# does basic checks that the graph is valid
def checkGraph(g):
    print('checking graph')
    for k, v in g.items():
        for nbr in v:
            assert(k in g[nbr])
    print('graph ok')

def isConnected(g):
    visited = {}
    start = 0
    for v in g.keys():
        visited[v] = False
        start = v # grab any vertex
    stack = [v]
    visited[v] = True
    while len(stack) > 0:
        top = stack.pop()
        for nbr in g[top]:
            if not visited[nbr]:
                stack.append(nbr)
                visited[nbr] = True
    for k, v in visited.items():
        if not v:
            #print('graph not connected')
            return False
    #print('graph is connected')
    return True
    
def countEdges(g):
    total = 0
    # check that edges are going in both directions
    for v, nbrs in g.items():
        for nbr in nbrs:
            assert(v in g[nbr])
        total += len(nbrs)
    if total % 2 != 0:
        print('error, odd number of edges')
    else:
        return total // 2
            
# checks that g is a spanning tree
# g is a adjList, stored as a dict
def isST(g):
    # connected
    if isConnected(g) and countEdges(g) == len(g.keys()) - 1:
        return True
    else:
        return False
        
def tests():
    g = {}
    g[1] = [2, 4]
    g[2] = [1, 3, 4]
    g[3] = [2, 4, 6]
    g[4] = [1, 2, 3, 5]
    g[5] = [4, 6]
    g[6] = [3, 5]

    checkGraph(g)

    print('sample test')
    sp = STSampler(g)
    for i in range(10):
        t = sp.sample()
        print(isST(t))

        
        
        









        
