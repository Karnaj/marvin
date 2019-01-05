from functools import total_ordering

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        self.x == other.x and self.y == other.y

    def __lt__(self, other):
        self.x < other.x or (self.x == other.x and self.y < other.y)

    def is_external(self, segment):
        A, B = segment.p1, segment.p2
        return (B.x-A.x) * (self.y-A.y) - (B.y-A.y) * (self.x-A.x) > 0

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Segment:
    def __init__(p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        self.p1 == other.p1 and self.p2 == other.p2

    def __str__(self):
        return "[A{} , B{}]".format(p1, p2)

    #counterclockwise order
    def __ccw(A,B,C):
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

    def has_intersection(other):
        A, B, C, D = self.p1, self.p2, other.p1, other.p2
        return __ccw(A,C,D) != __ccw(B,C,D) and __ccw(A,B,C) != __ccw(A,B,D)
