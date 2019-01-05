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

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

def is_hull_side(p, q, points):
    if p == q:
        return False
    return all(not point.is_external(p, q) for point in points)

def compute_convex_hull(points):
    N = len(points)
    hull = []
    for i in range(N):
        for j in range(N):
            if i != j:
                if is_hull_side(points[i], points[j], points):
                    hull.append([points[i], points[j]])
    return hull

def print_points(points):
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.plot(X, Y)

points = [Point(randint(0, 10000000000), randint(0, 10000000000)) for i in range(2019)]
X = [p.x for p in points]
Y = [p.y for p in points]
plt.scatter(X, Y, s=10, color='black')
convex_hull = compute_convex_hull(points)
print(len(convex_hull))
#[print(s[0], s[1]) for s in convex_hull]
for s in convex_hull:
    plt.plot([s[0].x, s[1].x], [s[0].y, s[1].y], color='red', lw=1)
plt.show()
plt.close()
