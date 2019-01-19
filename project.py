import matplotlib.pyplot as plt
from data_structures import *
from convex_hull import *
from triangulation import *
from random import randint, sample
import itertools
from visibility_graph import *

def print_points(points, color='black', s=10):
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.scatter(X, Y, s=10, color='black')

def print_segments(segments, color='blue', lw=1):
    for s in segments:
        plt.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], color=color, lw=lw)


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

points_1 = [Point(randint(0, 40), randint(0, 50)) for i in range(10)]
polygon_1 = Polygon.compute_convex_hull_incremental(points_1)

polygon_2 = Polygon([Point(120, 120), Point(160, 120), Point(160, 80),
                          Point(120, 80), Point(120, 100), Point(140, 100),
                          Point(140, 90), Point(150, 90), Point(150, 110),
                          Point(120, 110)])


points_3 = [Point(randint(0, 40), randint(90, 130)) for i in range(10)]
polygon_3 = Polygon.compute_convex_hull_incremental(points_3)

polygon_list = polygon_2.simple_triangulation()

v = VisibilityGraph([polygon_1, polygon_2, polygon_3], [Point(70, 3), Point(15, 30)])

points = [Point(72, 48), Point(30, 70), Point(140, 40), Point(60, 110)]

#for p in points:
#    v.add_point(p)

#v.add_obstacle(polygon_3)

print_points(polygon_1.points())
print_points(polygon_2.points())
print_points(polygon_3.points())
print_points(v.get_points())


polygon_1 = Polygon([Point(0, 0), Point(0, 7), Point(7, 7), Point(7, 0)])
polygon_list = [p.convex_minkowski_sum(polygon_1) for p in polygon_list]

for p in polygon_list:
    print_segments(p.segments(), color=sample(['b', 'g', 'r', 'c', 'm', 'y', 'k'], 1)[0], lw=1)
    for p1 in p.points():
        print(p1)    
    print()
    print()
    
v = VisibilityGraph(polygon_list, [Point(0, 7), Point(148, 100)])
    
print_segments(polygon_1.segments(), color='black', lw=3)
print_segments(polygon_2.segments(), color='black', lw=2)
print_segments(polygon_3.segments(), color='black', lw=3)


print_segments(v.edges, color='red', lw=1)

plt.show()
plt.close()
   
