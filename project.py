import matplotlib.pyplot as plt
from data_structures import *
from convex_hull import *
from minkowski_sum import *
from random import randint
import itertools

def print_points(points, color='black', s=10):
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.scatter(X, Y, s=10, color='black')

def print_segments(segments, color='blue', lw=1):
    for s in segments:
        plt.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], color=color, lw=lw)

def convex_minkowski_sum(A, B):
    p = min(A.points)
    points = [Point(p1.x + p2.x - p.x, p1.y + p2.y - p.y) for (p1, p2) in itertools.product(A.points, B.points)]
    return compute_convex_hull_incremental(points)
    
def visibility_graph(obstacle, p1, p2):
    N = len(obstacle) + 2
    graph = [[0 for i in range(N)] for j in range(N)]
    for i in range(N - 2):
        graph[i][(i + 1) % len(obstacle)] = 1
        graph[(i + 1)%len(obstacle)][i] = 1
    for i in range(N - 2):
        s1 = Segment(p1, obstacle[i].p1)
        s2 = Segment(p2, obstacle[i].p1)
        if not any(s1.has_intersection(s) for s in obstacle):
            graph[N - 2][i] = 1
            graph[i][N - 2] = 1
        if not any(s2.has_intersection(s) for s in obstacle):
            graph[N - 1][i] = 1
            graph[i][N - 1] = 1  
    return graph

def visibility_graph_c(polygon, segments): # possible only if no intersection into polygons
    edges = [s for s in segments]
    N = len(polygon)
    for i in range(N):
        for j in range(i + 1, N):
            for p1 in polygon[i]:
                for p2 in polygon[j]:
                    s = Segment(p1, p2)
                    if not any(s.has_strict_intersection(s1) for s1 in segments):
                        print(s)
                        edges.append(s)
    return edges

def visibility_graph_b(obstacles):
    points = []
    for (i, o) in enumerate(obstacles):
        for p in o.points:
            points.append((i, p))
    points.sort(key=lambda x : x[1])
    #segments = [[] for i in range(len(points))]
    segments = []
    edges = []
    vus = []
    for (i, p) in points:
        segments.append(obstacles[i].edges_with(p)[1])
        segments.append(obstacles[i].edges_with(p)[0])
        for (j, p1) in vus:
            s = Segment(p, p1)
            #valide = True
            #for i in range(p1.id, p.id):
            #    if not any(s.has_strict_intersection(s1) for s1 in segments[i]):
            #        valide = False
            #        break
            #print(valide)
            #if valide:
            if i != j or obstacles[i].external_segment(p, p1):
                if not any(s.has_strict_intersection(s1) for s1 in segments):
                    edges.append(s)
        vus.append((i, p))
    return edges    


points_1 = [Point(randint(0, 40), randint(0, 50)) for i in range(10)]
polygon_1 = compute_convex_hull_incremental(points_1)

polygon_2 = Polygon([Point(120, 120), Point(160, 120), Point(160, 80),
                          Point(120, 80), Point(120, 100), Point(140, 100),
                          Point(140, 90), Point(150, 90), Point(150, 110),
                          Point(120, 110)])


points_3 = [Point(randint(0, 40), randint(90, 130)) for i in range(10)]
polygon_3 = compute_convex_hull_incremental(points_3)

v = VisibilityGraph([polygon_1, polygon_2, polygon_3], [Point(70, 3), Point(15, 30)])

points = [Point(72, 48), Point(30, 70), Point(140, 40), Point(60, 110)]

#for p in points:
#    v.add_point(p)

#v.add_obstacle(polygon_3)

print_points(polygon_1.points())
print_points(polygon_2.points())
print_points(polygon_3.points())
print_points(v.get_points())

print_segments(polygon_1.segments(), color='black', lw=3)
print_segments(polygon_2.segments(), color='black', lw=3)
print_segments(polygon_3.segments(), color='black', lw=3)
print_segments(v.edges, color='red', lw=1)

plt.show()
plt.close()
                
                
                
                
                
