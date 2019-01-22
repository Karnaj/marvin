from functools import total_ordering
from operator import itemgetter
import itertools
from copy import deepcopy
import numpy as np
from math import atan, atan2, pi
import matplotlib.pyplot as plt

from fractions import *

def intersection_points(P1, P2):
    IP1 = [[] for i in range(len(P1.points()))]
    IP2 = [[] for i in range(len(P2.points()))]
    
    def dist(p1, p2):
        a, b = s.p1, s.p2
        return abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))
    
    
    for (i, s1) in enumerate(P1.segments()):
        for (j, s2) in enumerate(P2.segments()):
            if s1.is_aligned_with(s2):
                P = s1.interior_points(s2)
                for p in P:
                    IP1[i].append(p)
                    IP2[j].append(p)
            else:
                inter = s1.intersection_with(s2)
                if inter:
                    IP1[i].append(inter)
                    IP2[j].append(inter)
        IP1[i] = list(set(IP1[i]))
        IP1[i].sort(key=lambda p: P1.points()[i].dist_c(p))
    for j in range(len(P2.segments())):
        IP2[j] = list(set(IP2[j]))
        IP2[j].sort(key=lambda p: P2.points()[j].dist_c(p))
    return IP1, IP2

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist_c(self, other):
        return (self.x - other.x)*(self.x - other.x) + (self.y - other.y)*(self.y - other.y)
        
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

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
        
    def is_aligned_with(self, other1, other2):
        p1, p2, p3 = self, other1, other2
        if (p2.x - p1.x) * (p3.y - p2.y) == (p2.y - p1.y) * (p3.x - p2.x):
                return True
        return False
        
    def __hash__(self):
        return hash((self.x, self.y))

#counterclockwise order
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
        
class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def is_aligned_with(self, other):
        p1, p2, p3, p4 = self.p1, self.p2, other.p1, other.p2
        if (p2.x - p1.x) * (p3.y - p2.y) == (p2.y - p1.y) * (p3.x - p2.x):
            if (p2.x - p1.x) * (p4.y - p2.y) == (p2.y - p1.y) * (p4.x - p2.x):
                return True
        return False
    
    def interior_points(self, other):
        p1, p2, p3, p4 = self.p1, self.p2, other.p1, other.p2
        P1 = [p1, p2]
        P1.sort()
        P2 = [p3, p4]
        P2.sort()
        P = [p1, p2, p3, p4]
        P.sort()
        if (P[0] in P1 and P[3] in P1) or P[0] in P2 and P[3] in P2:
            return [P[1], P[2]]
        elif (P[0] in P1 and P[2] in P1) or (P[0] in P2 and P[2] in P2):
            return [P[1], P[2]]
        elif P[1] == P[2]:
            return [P[2]]
        return []
        
    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __str__(self):
        return "[A{} , B{}]".format(self.p1, self.p2)

    def __repr__(self):
        return "[A{} , B{}]".format(self.p1, self.p2)
        
    def has_intersection(self, other):
        A, B, C, D = self.p1, self.p2, other.p1, other.p2
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def has_strict_intersection(self, other):
        if self.p1 == other.p1 or self.p1 == other.p2 or self.p2 == other.p1 or self.p2 == other.p2:
            return False
        A, B, C, D = self.p1, self.p2, other.p1, other.p2
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D) 

    def intersection_with(self, other):
        if self.p1 == other.p1 or self.p1 == other.p2:
            return self.p1
        elif self.p2 == other.p1 or self.p2 == other.p2:
            return self.p2
        if not self.has_intersection(other):
            return None
        line1 = [[self.p1.x, self.p1.y], [self.p2.x, self.p2.y]]
        line2 = [[other.p1.x, other.p1.y], [other.p2.x, other.p2.y]]
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           return None

        d = (det(*line1), det(*line2))
        x = Fraction(det(d, xdiff), div)
        y = Fraction(det(d, ydiff), div)
        return Point(x, y)

class Polygon:
    def union(self, P2, co=False):
        def angle(p1, p2):
            dot = p1.x*p2.x + p1.y * p2.y
            det = p1.x*p2.y - p1.y*p2.x
            return atan2(det, dot)
        IP1, IP2 = intersection_points(self, P2)
        if len(list(set([item for sublist in IP1 for item in sublist]))) < 2:    
            return None   
        L1, L2 = [], []
        vus = []
        for (i, p) in enumerate(self.points()):
            L1.append((p, -1))
            for p1 in IP1[i]:
                if i == 0 or p1 != self.points()[i-1]:
                    L1.append((p1, 1))

        for (i, p) in enumerate(P2.points()):
            L2.append((p, -1))
            for p1 in IP2[i]:
                if i == 0 or p1 != P2.points()[i -1]:
                    L2.append((p1, 0))
           
        i = 0
        j = 0
        print()
        print()
        print()
        print()
        print(self.points())
        print(P2.points())
        print()
        print(L1)
        print(L2)
        print()
        points = []
        if self.points()[0] < P2.points()[0]:
            a = 0
            cond = 0
        else:
            a = 1
            cond = 1
        while i < len(L1) or j < len(L2):
            conf = False
            if a == 0:
                (p, pi) = L1[i % len(L1)]
                points.append(p)
                if pi == 1:
                    a = 1
                    conf = True
                    while p != L2[j % len(L2)][0]:
                        j += 1
                    while p == L2[j % len(L2)][0]:
                        j += 1
                while p == L1[i % len(L1)][0]:
                    i += 1
                if conf == True:
                    print("ICI", p)
                    p0 = L1[i % len(L1)][0]
                    p1 = L2[j % len(L2)][0]
                    if p.is_aligned_with(p0, p1):
                        LISTE = [p, p0, p1]
                        LISTE.sort()
                        if LISTE[1] == p0:
                            a = 0
                    else:
                        p3 = points[-2]
                        angle0 = angle(Point(p.x - p3.x, p.y - p3.y), Point(p0.x - p.x, p0.y - p.y))
                        angle1 = angle(Point(p.x - p3.x, p.y - p3.y), Point(p1.x - p.x, p1.y - p.y))
                        if angle0 > angle1:
                            a = 0
            elif a == 1:
                (p, pj) = L2[j % len(L2)]
                points.append(p)
                if pj == 0:
                    a = 0
                    conf = True
                    while p != L1[i % len(L1)][0]:
                        i += 1
                    while p == L1[i % len(L1)][0]:
                        i += 1
                while p == L2[j % len(L2)][0]:
                    j += 1
                if conf == True:
                    print("ICI", p)
                    p0 = L1[i % len(L1)][0]
                    p1 = L2[j % len(L2)][0]
                    if p.is_aligned_with(p0, p1):
                        LISTE = [p, p0, p1]
                        LISTE.sort()
                        if LISTE[1] == p1:
                            a = 1
                    else:
                        p3 = points[-2]
                        angle0 = angle(Point(p.x - p3.x, p.y - p3.y), Point(p0.x - p.x, p0.y - p.y))
                        angle1 = angle(Point(p.x - p3.x, p.y - p3.y), Point(p1.x - p.x, p1.y - p.y))
                        if angle1 > angle0:
                            a = 1
        print(points)
        _points = [points[0]]
        i = 1
        N = len(points)
        while i < N and points[i] != points[0]:
            _points.append(points[i])
            i += 1
        return Polygon(_points)
    
    def union1(self, P2, co=False):
        IP1, IP2 = intersection_points(self, P2)
        if [item for sublist in IP1 for item in sublist] == []:
            return None
        L1, L2 = [], []

        for (i, p) in enumerate(self.points()):
            L1.append((p, -1))
            for p1 in IP1[i]:
                    L1.append((p1, 1))
        for (i, p) in enumerate(P2.points()):
            L2.append((p, -1))
            for p1 in IP2[i]:
                    L2.append((p1, 0))  
        i = 0
        j = 0
        points = []
        if self.points()[0] < P2.points()[0]:
            a = 0
        else:
            a = 1
        print()
        print(self.points())
        print(P2.points())
        print()
        print(IP1)
        print(IP2)
        print()
        print(L1)
        print(L2)
        print()
        print("DÉBUT UNION")
        while i < len(L1) or j < len(L2):
            conf = False
            if a == 0:
                (p, pi) = L1[i % len(L1)]
                points.append(p)
                if pi == 1:
                    a = 1
                    while p != L2[j % len(L2)][0]:
                        j += 1
                    while p == L2[j % len(L2)][0]:
                        j += 1
                while p == L1[i % len(L1)][0]:
                    if L1[i % len(L1)][1] == -1 and a== 1:
                        conf = True
                    i += 1
                if conf == True:
                    print("ICI", p)
                    p0 = L1[i % len(L1)][0]
                    p1 = L2[j % len(L2)][0]
                    if p.is_aligned_with(p0, p1):
                        LISTE = [p, p0, p1]
                        LISTE.sort()
                        if LISTE[1] == p0:
                            a = 0
                    else:
                        angle0 = atan2(p0.y - p.y, p0.x - p.x)
                        angle1 = atan2(p1.y - p.y, p1.x - p.x)
                        if angle0 > angle1:
                            a = 0
            elif a == 1:
                (p, pj) = L2[j % len(L2)]
                points.append(p)
                if pj == 0:
                    a = 0
                    while p != L1[i % len(L1)][0]:
                        i += 1
                    while p == L1[i % len(L1)][0]:
                        i += 1
                while p == L2[j % len(L2)][0]:
                    if L2[j % len(L2)][1] == -1 and a==0:
                        conf = True
                    j += 1
                if conf == True:
                    print("ICI", p)
                    p0 = L1[i % len(L1)][0]
                    p1 = L2[j % len(L2)][0]
                    if p.is_aligned_with(p0, p1):
                        LISTE = [p, p0, p1]
                        LISTE.sort()
                        if LISTE[1] == p1:
                            a = 1
                    else:
                        angle0 = atan2(p0.y - p.y, p0.x - p.x)
                        angle1 = atan2(p1.y - p.y, p1.x - p.x)
                        if angle1 > angle0:
                            a = 1
        print("UNION")
        print(points)
        print()
        return Polygon(points)
        
    def union_final(self, P2, co=False):
        IP1, IP2 = intersection_points(self, P2)
        if [item for sublist in IP1 for item in sublist] == []:
            return None
        L1, L2 = [], []

        
        for (i, p) in enumerate(self.points()):
            L1.append((p, -1))
            for p1 in IP1[i]:
                    L1.append((p1, 1))
        for (i, p) in enumerate(P2.points()):
            L2.append((p, -1))
            for p1 in IP2[i]:
                    L2.append((p1, 0))  
                    
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
        def simpl(points):
            _points = [points[0], points[1]]
            for i in range(2, len(points)):
                if points[i].is_aligned_with(_points[-1], _points[-2]):
                    _points.pop()
                _points.append(points[i])
            while len(_points) > 2 and _points[-1].is_aligned_with(_points[0], _points[-2]):
                _points.pop()
            return _points
            
        
        N = len(points)
        i_min, _ = min(enumerate(points), key=itemgetter(1))
        if points[(i_min + 1) % N].y > points[i_min - 1].y:
            self._points = [points[(i_min + i) % N] for i in range(N)]
        else:
            self._points = [points[(i_min - i) % N] for i in range(N)]
        self._points = simpl(self._points)
        N = len(self._points)
        i_min, _ = min(enumerate(self._points), key=itemgetter(1))
        if self._points[(i_min + 1) % N].y > self._points[i_min - 1].y:
            self._points = [self._points[(i_min + i) % N] for i in range(N)]
        else:
            self._points = [self._points[(i_min - i) % N] for i in range(N)]
        
    def compute_convolution_cycle(self, P2, i0, j0):
        points1, points2 = self._points, P2.points()
        C = []
        i, j = i0, j0
        s = points1[i] + points2[j]
        while True:
            inc_p = is_between_counter_clock_wise()
            inc_q = is_between_counter_clock_wise()
            if inc_p:
                t = points1[i + 1] + points2[j]
                C.append(Segment(s, t))
                s = t
                i = (i + 1) % len(points1)
            if inc_q:
                t = points1[i] + points2[j + 1]
                C.append(Segment(s, t))
                s = t
                i = (i + 1) % len(points1)
            if i == i0 and j == j0:
                break
        return C
    
    def minkowski_sum_by_convolution(self, P2):
        points_1 = self._points
        points_2 = P2.points()
        
        
    def convex_minkowski_sum(self, P2):
        points_1, points_2 = self._points, P2.points()
        points = [Point(p1.x + p2.x, p1.y + p2.y) \
                  for (p1, p2) in itertools.product(points_2, points_1)]
        return Polygon.compute_convex_hull_incremental(points)
   
    def minkowski_sum(self, P2):
    
    
        def print_segments(segments, color='blue', lw=1):
            for s in segments:
                plt.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], color=color, lw=lw)
                
        def union_multi(result, co=False):
            P = Polygon(result[0].points())
            L = [False for i in range(len(result))]
            L[0] = True
            ending = False
            while not ending:
                ending = True
                for (i, b) in enumerate(L):
                    # if True:
                        # print_segments(P.segments(), color='r', lw=3)
                    if not b:
                        ending = False
                        P2 = P.union(result[i], co)
                        if P2 != None:
                            P = P2
                            L[i] = True
                            print(P.points())
                            # print_segments(P.segments(), color='b', lw=2)
                    # print_segments(result[i].segments(), color='g')
                    # if True:
                        # plt.show()
                        # plt.close()
            # print("FINI")
            # for P1 in result:
                # print_segments(P1.segments(), color='g')
            # print_segments(P.segments())
            # plt.show()
            # plt.close()
            return P
            

        
        points_2 = P2.points()
        x, y = points_2[0].x, points_2[0].y
        pol_2 = Polygon([Point(x - p1.x, y - p1.y) for p1 in points_2])
        triangles_2 = pol_2.simple_convex_decomposition()
        triangles_1 = self.simple_convex_decomposition()
        result = []
        for t1 in triangles_1:
            T = []
            for t2 in triangles_2:
                T.append(t1.convex_minkowski_sum(t2))
            S = union_multi(T)
            result.append(S)
            print("Fait")
            # print_segments(self.segments())
            # print_segments(S.segments(), lw=2)
            # plt.show()
            # plt.close()
        #P1 = result.pop()
        #while result != []:
        #    P1 = P1.union(result.pop())
        #return P1
        # return Polygon.union(result)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        #for (i, P1) in enumerate(result):
        #    print_segments(P1.segments(), color =colors[i], lw=2)
        #print_segments(self.segments(), color = 'k')
        #plt.show()
        #plt.close()
        print(len(result))
        print()
        print()
        return union_multi(result, co=True)
    
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
    
    def index_vertex_edges(self, i):
        N = len(self._points)
        p1, p, p2 = self._points[i - 1], self._points[i], self._points[(i + 1) % N]
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
        
    def simple_convex_decomposition(self):
        def aux(poly, L):
            if len(poly.points()) < 4 or poly.is_convex():
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
        return [t for t in L if len(t.points()) > 3 or t.is_non_trivial_triangle()]
        
    
    
    def is_convex(self):
        """Return True if the polynomial defined by the sequence of 2D
        points is 'strictly convex': points are valid, side lengths non-
        zero, interior angles are strictly between zero and a straight
        angle, and the polygon does not intersect itself.

        NOTES:  1.  Algorithm: the signed changes of the direction angles
                    from one side to the next side must be all positive or
                    all negative, and their sum must equal plus-or-minus
                    one full turn (2 pi radians). Also check for too few,
                    invalid, or repeated points.
                2.  No check is explicitly done for zero internal angles
                    (180 degree direction-change angle) as this is covered
                    in other ways, including the `n < 3` check.
        """
        TWO_PI = 2 * pi
        polygon = [(p.x, p.y) for p in self._points]
        try:  # needed for any bad points or direction changes
            # Check for too few points
            if len(polygon) < 3:
                return False
            # Get starting information
            old_x, old_y = polygon[-2]
            new_x, new_y = polygon[-1]
            new_direction = atan2(new_y - old_y, new_x - old_x)
            angle_sum = 0.0
            # Check each point (the side ending there, its angle) and accum. angles
            for ndx, newpoint in enumerate(polygon):
                # Update point coordinates and side directions, check side length
                old_x, old_y, old_direction = new_x, new_y, new_direction
                new_x, new_y = newpoint
                new_direction = atan2(new_y - old_y, new_x - old_x)
                if old_x == new_x and old_y == new_y:
                    return False  # repeated consecutive points
                # Calculate & check the normalized direction-change angle
                angle = new_direction - old_direction
                if angle <= -pi:
                    angle += TWO_PI  # make it in half-open interval (-Pi, Pi]
                elif angle > pi:
                    angle -= TWO_PI
                if ndx == 0:  # if first time through loop, initialize orientation
                    if angle == 0.0:
                        return False
                    orientation = 1.0 if angle > 0.0 else -1.0
                else:  # if other time through loop, check orientation is stable
                    if orientation * angle <= 0.0:  # not both pos. or both neg.
                        return False
                # Accumulate the direction-change angle
                angle_sum += angle
            # Check that the total number of full turns is plus-or-minus 1
            return abs(round(angle_sum / TWO_PI)) == 1
        except (ArithmeticError, TypeError, ValueError):
            return False  # any exception means not a proper convex polygon
