

# Take the graph as an adjacency list related to nodes (ie a 0 represent nodes[0])
# n the length of nodes.
# deb the index of the first node.

inf = float('inf')

def dijkstra(graph, n, deb, fin):

    d = [inf for e in range(len(nodes))]
    d[deb] = 0

    pred = [-1 for e in range(len(nodes))]
    pred[deb] = deb

    # q
    q = priority_queue()
    while not q.empty():

        s1 = q.pop()
        for s2 in graph[s1]:

            if d[s2] > d[s1] + w(s1, s2):
                d[s2] = d[s1] + w(s1, s2)
                pred[s2] = s1

    return (pred, d)

#Compute a path from beginning to end using distances computed in d.
# beg must be the one used to compute d !!!
def path(nodes, pred, end):

    s = end
    L = []
    while s != pred[s]:
        L.append(s)
        s = pred[s]

    L.append(s)
    return L
