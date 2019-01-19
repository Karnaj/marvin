from data_structures import *

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
                    if o.strictly_contains_point(p[1]):
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
                    if self.obstacles[j][1].strictly_contains_point(p):
                        correct = False
            if correct:
                for (j, p1) in vus:
                    s = Segment(p, p1)
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
                segm
                ents.append(self.obstacles[i][1].edges_with(p)[0])
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
