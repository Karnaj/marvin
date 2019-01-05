import data_structures

def is_hull_side(p, q, points):
    if p == q:
        return False
    return all(not point.is_external(p, q) for point in points)

def compute_convex_hull_direct(points):
    N = len(points)
    hull = []
    for i in range(N):
        for j in range(N):
            if i != j:
                if is_hull_side(points[i], points[j], points):
                    hull.append(Segment(points[i], points[j]))
    return hull

def compute_convex_hull_incremental(points):
    def compute(hull, sup=True)
        N = len(points)
        a, b, g = (2, N, 1) if sup else (N - 3, - 1, - 1) 
        for i in range(a, b, g):
            hull.append(points[i])
            while len(hull) > 2:
                p3 = hull[-1]
                p2 = hull[len(hull) - 2]
                p1 = hull[len(hull) - 3]
                if p3.is_external(p1, p2):
                    hull.remove(p2)
                else:
                    break

    points.sort()
    hull = [points[0],points[1]]
    compute(hull)
    hull.append(points[N-2])
    compute(hull, sup=False)
    return [Segment(hull[i], hull[i + 1]) for i in range(len(hull) - 1)]
