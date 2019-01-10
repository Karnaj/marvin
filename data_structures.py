from functools import total_ordering

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
    def __init__(self, segments):
        self.points = [s.p1 for s in segments]
        self.points.sort()
        self.segments = []
        self.neighbours_list = {}
        
        i = 0
        while segments[i].p1 != self.points[0]:
            i += 1
        
        for j in range(len(segments)):
            s = segments[(j + i) % len(segments)]
            self.segments.append(s)
    
    def external_segment(self, p, p1):
        if self.are_neighbours(p, p1):
            return True
        pm = Point((p.x + p1.x) / 2, (p.y + p1.y) / 2)
        if self.contains(pm):
            return False
        s = Segment(p, p1)
        nb_intersections = 0
        for s1 in self.segments:
            if s.has_strict_intersection(s1):
                nb_intersections += 1
        return nb_intersections % 2 == 0
        
    def contains(self, point):
        y = point.y
        x_min = min([s.x for s in self.points]) - 1
        s = Segment(Point(point.x, y), Point(x_min, y))
        nb_intersections = 0
        for s1 in self.segments:
            if s.has_intersection(s1):
                nb_intersections += 1
        return nb_intersections % 2 == 1
    
    
    def neighbours(self, point):
        i = 0
        while self.segments[i].p1 != point:
            i += 1
        return [self.segments[i - 1].p1, self.segments[i].p2]
    
    def are_neighbours(self, p1, p2):
        return p2 in self.neighbours(p1)
        
    def edges_with(self, point):
        return [Segment(point, p) for p in self.neighbours(point)]
        
class VisibilityGraph:
    def __init__(self, obstacles=[], points=[]):
        self.edges = []
        self.points = []
        self.i = 0
        self.obstacles = []
        for o in obstacles:
            self.obstacles.append((self.i, o))
            for p in o.points:
                self.points.append((self.i, p))
            self.i += 1
        for p in points:
            self.points.append((-1, p))
        self.compute()
        
    def compute(self):
        self.points.sort(key=lambda x : x[1])
        vus = []
        points = []
        for p in self.points:
            if p[0] != -1:
                points.append(p)
            else:
                correct = True
                for (j, o) in self.obstacles:
                    if o.contains(p[1]):
                        correct = False
                if correct:
                    points.append(p)
                
        segments = []
        for (i, p) in points:
            correct = True
            if i != -1:
                segments.append(self.obstacles[i][1].edges_with(p)[1])
                segments.append(self.obstacles[i][1].edges_with(p)[0])
            else:
                for (j, p1) in vus:
                    if self.obstacles[j][1].contains(p):
                        correct = False
            if correct:
                for (j, p1) in vus:
                    s = Segment(p, p1)
                    if i != j or i == -1 or self.obstacles[i][1].external_segment(p, p1):
                        if not any(s.has_strict_intersection(s1) for s1 in segments):
                            self.edges.append(s)
            vus.append((i, p))
    
    def get_points(self):
        return [p[1] for p in self.points]
        
    def add_point(self, point):
        for (i, o) in self.obstacles:
            if o.contains(point):
                return
        self.points.append((-1, point))
        self.points.sort(key=lambda x : x[1])
        vus = []
        segments = []
        is_reached = False
        for (i, p) in self.points:
            if p == point:
                is_reached = True
                for (j, p1) in vus:
                    s = Segment(point, p1)
                    if not any(s.has_strict_intersection(s1) for s1 in segments):
                        self.edges.append(s)
            else:
                if i != -1:
                    segments.append(self.obstacles[i][1].edges_with(p)[1])
                    segments.append(self.obstacles[i][1].edges_with(p)[0])
                if is_reached:
                    s = Segment(point, p)
                    if not any(s.has_strict_intersection(s1) for s1 in segments):
                        self.edges.append(s)
            vus.append((i, p))
        
    def add_obstacle(self, obstacles):
        pass
