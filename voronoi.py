
import heapq
from enum import Enum

class EventType(Enum):
        SITE = 0
        EDGE = 1

class Event():
    def __init__(self):
        self.type = -1

class Site(Event):
    def __init__(self, pos):
        self.type = EventType.SITE*
        self.pos = pos

class Edge(Event):
    def __init__(self):
        self.type = EventType.EDGE


# yd the directrix
def parabola_eq(yd, focus):
    xf, yf = focus.x, focus.y

    def f(x):
        return 1/(2*(yf-yd))*(x-xf)*(x-xf) + (yf + yd)/2

    return f


# Here is my implementation of fortune's algorithm
# I used a sweep line from top to bottom.
def fortune(points):

    queue = []
    beachline = []

    for i_site in sites:

        queue.heappush(Site(pos))

    #
    while not queue.empty():
        event = queue.heappop()

        if event.type == EventType.SITE:

            point = event.pos
            yd = point.y # The directrix is on the point

            add_new_site(site, beachline)

        else: # It's Event.EDGE
            remove_cell(cell, beachline)


    cleanup()

    return 0
