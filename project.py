import matplotlib.pyplot as plt
from data_structures import *
from convex_hull import *
from random import randint


def print_points(points, color='black', s=10):
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.scatter(X, Y, s=10, color='black')

def print_segments(segments, color='red', lw=1):
    for s in segments:
        plt.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], color=color, lw=lw)

points = [Point(randint(-1000000000, 1000000000), randint(-10000000000, 1000000000)) for i in range(20000)]
convex_hull = compute_convex_hull_incremental(points)
print(len(convex_hull))
print_points(points)
print_segments(convex_hull)
plt.show()
plt.close()
