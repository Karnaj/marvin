import matplotlib.pyplot as plt
import data_structures
from convex_hull import compute_convex_hull_direct

def print_points(points, color='black', s=10)
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.scatter(X, Y, s=10, color='black')

def print_segments(segments, color='red', lw=1):
    for s in segments:
        plt.plot([s.p1.x, s.p2x], [s.p1.y, s.p2.y], color=color, lw=lw)
        
points = [Point(randint(0, 10000000000), randint(0, 10000000000)) for i in range(2019)]
convex_hull = compute_convex_hull_direct(points)
print_points(points)
print_segments(convex_hull)
plt.show()
plt.close()
