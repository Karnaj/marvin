from functools import total_ordering
import matplotlib.pyplot as plt
from random import randint

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        self.x == other.x and self.y == other.y
        
    def __lt__(self, other):
        self.x < other.x or (self.x == other.x and self.y < other.y)
        
    def is_external(self, a, b):
        return (b.x-a.x)*(self.y-a.y)-(b.y-a.y)*(self.x-a.x)>0
    
def is_hull_side(p, q, points):
    if p == q:
        return False
    return all(not point.is_external(p, q) for point in points)
    
def compute_convex_hull(points):
    N = len(points)
    hull = []
    for i in range(N):
        for j in range(N):
            if is_hull_side(points[i], points[j], points):
                hull.append([points[i], points[j]]) 
    hull = [s[0] for s in hull]
    return hull
    
def print_points(points):
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.plot(X, Y)
    
points = [Point(randint(0, 15), randint(0, 15)) for i in range(20)]
convex_hull = compute_convex_hull(points)
print_points(convex_hull)
plt.show()
plt.close()
