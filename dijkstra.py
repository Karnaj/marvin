class Heap:
    def __init__(self, objs):
        self.n = 0
        self.heap = [None] #index starts at 1
        self.rank = {}
        for e in objs:
            self.push(e)

    def __len__(self):
        return len(self.heap) - 1

    def push(self, x):
        assert x not in self.rank
        i = len(self.heap)
        self.heap.append(x)
        self.rank[x] = i
        self.up(i)

    def pop(self):
        root = self.heap[1]
        del self.rank[root]
        x = self.heap.pop()
        if self:
            self.heap[1] = x
            self.rank[x] = 1
            self.down(1)
        return root

    def up(self, i):
        x = self.heap[i]
        while i > 1 and x < self.heap[i // 2]:
            self.heap[i] = self.heap[i // 2]
            self.rank[self.heap[i // 2]] = i
            i //= 2
        self.heap[i] = x
        self.rank[x] = i

    def down(self, i):
        x = self.heap[i]
        n = len(self.heap)
        while True:
            left = 2*i
            right = left + 1
            if right < n and \
               self.heap[right] < x and self.heap[right] < self.heap[left]:

                self.heap[i] = self.heap[right]
                self.rank[self.heap[right]] = i
                i = right

            elif left < n and self.heap[left] < x:
                self.heap[i] = self.heap[left]
                self.rank[self.heap[left]] = i
                i = left
            else:
                self.heap[i] = x
                self.rank[x] = i
                return

    def update(self, old, new):
        i = self.rank[old]
        del self.rank[old]
        self.heap[i] = new
        self.rank[new] = i
        if old < new:
            self.down(i)
        else:
            self.up(i)


#####  Dijkstra using my heap as a priority queue.
def dijkstra_update_heap(graph, weight, src = 0, trg = None):
    n = len(graph)
    prec = [None]*n
    prec[src] = src
    dist = [float('inf')] * n
    dist[src] = 0
    heap = Heap([(dist[node], node) for node in range(n)])
    
    while heap:
        d_node, node = heap.pop()
        if node == trg:
            break;
        
        print(heap.heap)
        for nb in graph[node]:
            old = dist[nb]
            new = d_node + weight[node][nb]
            if new < old:
                dist[nb] = new
                prec[nb] = node
                heap.update((old, nb), (new, nb))

    print("done")
    return dist, prec

def find_path(prec, trg, h2):
    L = [h2[trg]]
    while prec[trg] != trg:
        trg = prec[trg]
        L.append(h2[trg])
        if trg == None:
            return []
    L.append(h2[trg]) # trg is the source
    print(L)
    return L

def make_graph(vb_grp):
    h = {}
    h2 = []
    n = len(vb_grp._points)
    for (e, (id, p)) in enumerate(vb_grp._points):
        h[p] = e
        h2.append(p)
    mat = [[float('inf') for i in range(n)] for j in range(n)]
    graph = [[] for e in range(n)]

    for e in vb_grp.edges:
        a, b = e.p1, e.p2
        d = a.dist_c(b)
        mat[h[a]][h[b]] = d
        mat[h[b]][h[a]] = d
        graph[h[a]].append(h[b])
        graph[h[b]].append(h[a])

    return graph, mat, h, h2
