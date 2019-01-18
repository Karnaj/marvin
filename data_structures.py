from functools import total_ordering
from operator import itemgetter

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
        
    def split(self, p1, p2):
        i = 0
        polygon_points_1, polygon_points_2 = [], []
        
        while self._points[i] != p1 and self._points[i] != p2:
            polygon_points_1.append(self._points[i])
            i += 1
        if self._points[i] == p2:
            p1, p2 = p2, p1
        polygon_points_1.append(p1)        
        polygon_points_2.append(p1)
        
        while self._points[i] != p2:
            polygon_points_2.append(self._points[i])
            i += 1
        polygon_points_2.append(p2)
        polygon_points_1.append(p2)
        
        while self._points[i] != p1:
            polygon_points_1.append(self._points[i])
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
        
    def strictly_contains_points(self, p):
        return (not p in self._points) and self.contains_point(p)
    
    def interior_contains_points(self, p):
        return self.strictly_contains_points(p)
        # Should also check that for all edges e, p is not in e.
        
    def border_stricly_intersect_segment(self, p1, p2):
        # Intersect the polygon border and strictly (not in a vertex).
        if self.has_edge_with(p1, p2):
            return False
        s1 = Segment(p1, p2)
        return any(s1.has_strict_intersection(s2) for s2 in self.segments())

    def is_internal_edge(self, p, p1):
        pm = Point((p.x + p1.x) / 2, (p.y + p1.y)/2)
        if not self.contains(pm):
            return False
        return not self.sricly_intersect_segment(p, p1)
    
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
        
class VisibilityGraph:
    def __init__(self, obstacles, points=[]):
        self.edges = []
        self._points = []
        self.i = 0
        self.obstacles = []
        for o in obstacles:
            self.obstacles.append((self.i, o))
            for p in o.points():
                self._points.append((self.i, p))
            self.i += 1
        for p in points:
            self._points.append((-1, p))
        self.compute()
        
    def compute(self):
        self._points.sort(key=lambda x : x[1])
        vus = []
        points = []
        for p in self._points:
            if p[0] != -1:
                points.append(p)
            else:
                correct = True
                for (j, o) in self.obstacles:
                    if o.strictly_contains_points(p[1]):
                        correct = False
                if correct:
                    points.append(p)
                
        segments = []
        for (i, p) in points:
            correct = True
            if i != -1:
                edges = self.obstacles[i][1].vertex_edges(p)
                segments.append(edges[1])
                segments.append(edges[0])
            else:
                for (j, p1) in vus:
                    if self.obstacles[j][1].strictly_contains_points(p):
                        correct = False
            if correct:
                print(p)
                for (j, p1) in vus:
                    s = Segment(p, p1)
                    if i == j and not self.obstacles[i][1].is_external_edge(p, p1):
                            print("   {} {}", p1, False)
                    if i != j or i == -1 or self.obstacles[i][1].is_external_edge(p, p1):
                        if not any(s.has_strict_intersection(s1) for s1 in segments):
                            self.edges.append(s)
            vus.append((i, p))
    
    def get_points(self):
        return [p[1] for p in self._points]
        
    def add_point(self, point, obstacle_id=-1):
        for (i, o) in self.obstacles:
            if i != obstacle_id and o.contains(point):
                return
        self._points.append((obstacle_id, point))
        self._points.sort(key=lambda x : x[1])
        vus = []
        segments = []
        o_id = obstacle_id
        is_reached = False
        for (i, p) in self._points:
            if i != -1:
                segments.append(self.obstacles[i][1].edges_with(p)[1])
                segments.append(self.obstacles[i][1].edges_with(p)[0])
            if p == point:
                is_reached = True
                for (j, p1) in vus:
                    s = Segment(point, p1)
                    if i != j or i == -1 or self.obstacles[i][1].is_external_edge(p, p1):
                        if not any(s.has_strict_intersection(s1) for s1 in segments):
                            self.edges.append(s)
            else:
                if is_reached:
                    s = Segment(point, p)
                    if i != o_id or o_id == -1 or self.obstacles[i][1].is_external_edge(p, p1):
                        if not any(s.has_strict_intersection(s1) for s1 in segments):
                            self.edges.append(s)
            vus.append((i, p))
