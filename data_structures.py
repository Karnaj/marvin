from functools import total_ordering
from operator import itemgetter
import itertools
from copy import deepcopy

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def is_strictly_external(self, A, B):
        return (B.x-A.x) * (self.y-A.y) - (B.y-A.y) * (self.x-A.x) > 0

    def is_external(self, A, B):
        return (B.x-A.x) * (self.y-A.y) - (B.y-A.y) * (self.x-A.x) >= 0

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


#counterclockwise order
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
        
class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __str__(self):
        return "[A{} , B{}]".format(self.p1, self.p2)

    def has_intersection(self, other):
        A, B, C, D = self.p1, self.p2, other.p1, other.p2
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def has_strict_intersection(self, other):
        if self.p1 == other.p1 or self.p1 == other.p2 or self.p2 == other.p1 or self.p2 == other.p2:
            return False
        A, B, C, D = self.p1, self.p2, other.p1, other.p2
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D) 


class Polygon:
    def is_hull_side(p, q, points):
        if p == q:
            return False
        return all(not point.is_strictly_external(p, q) for point in points)
    
    def compute_convex_hull_incremental(points):
        N = len(points)

        def compute(hull, sup=True):
            a, b, g = (2, N, 1) if sup else (N - 3, - 1, - 1)
            for i in range(a, b, g):
                hull.append(points[i])
                while len(hull) > 2:
                    p3 = hull[-1]
                    p2 = hull[-2]
                    p1 = hull[-3]
                    if p3.is_external(p1, p2):
                        hull.pop(-2)
                    else:
                        break

        points.sort()
        hull_points = [points[0],points[1]]
        compute(hull_points)
        hull_points.append(points[N-2])
        compute(hull_points, sup=False)
        return Polygon(hull_points)
    
    def __init__(self, points):
        _points = []
        for (i, p) in enumerate(points):
            if p != points[i - 1]:
                _points.append(p)
        N = len(_points)
        i_min, _ = min(enumerate(_points), key=itemgetter(1))
        if points[(i_min + 1) % N].y > _points[i_min - 1].y:
            self._points = [_points[(i_min + i) % N] for i in range(N)]
        else:
            self._points = [_points[(i_min - i) % N] for i in range(N)]

    def convex_minkowski_sum(self, P2):
        points_1, points_2 = self._points, P2.points()
        p = min(points_2)
        points = [Point(p1.x + p2.x - p.x, p1.y + p2.y - p.y) for (p1, p2) in itertools.product(points_2, points_1)]
        return Polygon.compute_convex_hull_incremental(points)
    
    def minkowski_sum(self, P2):
        points_1, points_2 = self._points, P2.points()
        p = min(points_2)
        points = [Point(p1.x + p2.x - p.x, p1.y + p2.y - p.y) for (p1, p2) in itertools.product(points_2, points_1)]
        return Polygon.compute_convex_hull_incremental(points)    
    
    def points(self):
        return self._points
        
    def segments(self):
        points = self._points
        N = len(points)
        return [Segment(points[i], points[(i + 1) % N]) for i in range(N)]
    
    def has_vertex(self, p):
        return p in self._points()
    
    def vertex_neighbours(self, p):
        i = self._points.index(p)
        N = len(self._points)
        return [self._points[i - 1], self._points[(i + 1) % N]]
        
    def vertices_number(self):
        return len(self._points)
     
    def vertex_edges(self, p):
        p1, p2 = self.vertex_neighbours(p)
        return [Segment(p1, p), Segment(p, p2)]
    
    def has_edge_with(self, p1, p2):
        N = len(self._points)
        for (i, p) in enumerate(self._points):
            if (p == p1 and self._points[i - 1] == p2) or (p == p2 and self._points[i - 1] == p1):
                return True
        return False
  
    def remove_vertex(self, p):
        self._points.remove(p)
        N = len(self._points)
        i_min, _ = min(enumerate(self._points), key=itemgetter(1))
        self._points = [self._points[(i_min + i) % N] for i in range(N)]
        
    def split(self, p1, p2):
        i = 0
        N = len(self._points)
        polygon_points_1, polygon_points_2 = [], []
            
        while self._points[i] != p1 and self._points[i] != p2:
            polygon_points_1.append(self._points[i])
            i += 1
        if self._points[i] == p2:
            p1, p2 = p2, p1
        polygon_points_1.append(p1)        
        polygon_points_2.append(p1)
        
        while self._points[i % N] != p2:
            polygon_points_2.append(self._points[i % N])
            i += 1
        polygon_points_2.append(p2)
        polygon_points_1.append(p2)
        
        while self._points[i % N] != p1:
            polygon_points_1.append(self._points[i % N])
            i += 1
        
        return Polygon(polygon_points_1), Polygon(polygon_points_2)
        
    def contains_point(self, p):
        y = p.y
        x_min = min(self._points).x - 1
        s = Segment(Point(p.x, y), Point(x_min, y))
        nb_intersections = 0
        for s1 in self.segments():
            if s.has_intersection(s1):
                nb_intersections += 1
        return nb_intersections % 2 == 1
        
    def strictly_contains_point(self, p):
        return (not p in self._points) and self.contains_point(p)
    
    def interior_contains_point(self, p):
        return self.strictly_contains_point(p)
        # Should also check that for all edges e, p is not in e.
        
    def border_strictly_intersect_segment(self, p1, p2):
        # Intersect the polygon border and strictly (not in a vertex).
        if self.has_edge_with(p1, p2):
            return False
        s1 = Segment(p1, p2)
        return any(s1.has_strict_intersection(s2) for s2 in self.segments())

    def is_internal_edge(self, p, p1):
        pm = Point((p.x + p1.x) / 2, (p.y + p1.y)/2)
        if not self.contains_point(pm):
            return False
        return not self.border_strictly_intersect_segment(p, p1)
    
    def is_external_edge(self, p, p1):
        if self.has_edge_with(p, p1):
            return True
        pm = Point((p.x + p1.x) / 2, (p.y + p1.y)/2)
        if self.contains_point(pm):
            return False    
        s = Segment(p, p1)
        for s1 in self.segments():
            if s1.p1 not in [p, p1] and s1.p2 not in [p, p1]:
                if s.has_strict_intersection(s1) :
                    return False
        return True
        
    def is_non_trivial_triangle(self):
        if len(self._points) != 3:
            return False
        p1, p2, p3 = self._points
        return (p2.x - p1.x) * (p3.y - p2.y) != (p2.y - p1.y) * (p3.x - p2.x) 
        
    def simple_triangulation(self):
        def aux(poly, L):
            if len(poly.points()) < 4:
                L.append(poly)
            else:
                po = poly.points()[0]
                pg, pd = poly.vertex_neighbours(po)

                triangle = Polygon([po, pg, pd])

                #s = Segement(pg, pd)
                if poly.is_internal_edge(pg, pd):
                    L.append(triangle)
                    #p = poly.copy(); is it necessary ?
                    poly.remove_vertex(po) # Remove po so now we have the segment pg pd instead of po pg and po pd.
                    aux(poly, L)
                else:
                    l = [e for e in poly.points() if triangle.strictly_contains_point(e)]
                    s = Segment(pg, pd)
                
                    def dist(s, c):
                        a, b = s.p1, s.p2
                        return abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))

                    pj = max(l, key=lambda e: dist(s,e))
                    poly_l, poly_r = poly.split(po, pj)
                    aux(poly_l, L)
                    aux(poly_r, L)

        p = deepcopy(self)
        L = []
        aux(p, L)
        return [t for t in L if t.is_non_trivial_triangle()]
