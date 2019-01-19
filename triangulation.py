
#O(n^2)
# poly is a polygon
def simple_triangulation(poly):

    def aux(poly, L):

        po = poly.points[0]
        pg, pd = poly.neighbours(po)

        triangle = Polygon.from_points([po, pg, pd])

        #s = Segement(pg, pd)
        if poly.internal_segment(pg, pd):
            L.append(triangle)
            #p = poly.copy(); is it necessary ?
            poly.remove(po, [pg, pd]) # Remove po so now we have the segment pg pd instead of po pg and po pd.
            aux(poly, L)

        else:
            l = [e for e in poly.points if triangle.contains(e)]
            s = Segment(pg, pd)

            def dist(s, c):
                a, b = s.p1, s.p2
                return abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))

            pj = max(l, key=lambda e: dist(s,e))
            poly_l, poly_r = poly.split(po, pj)
            aux(poly_l, L)
            aux(poly_r, R)

    p = poly.copy()
    return aux(p, [])



#####################
##############################

import binary_tree

# Advanced Algorithm, inspired from Computational Geometry : Algorithms & applications by Berg & al.

def start_vertex(i, D, T):
    ei = D.get_from(i)
    T.insert((ei, i)) #vi is the helper of e

def end_vertex(i, D, T):

    epi = D.get_from(i-1) #e(i-1)
    helper = T.find(epi)

    if is_merge(helper):
        D.add()

def y_monotonous_partition(poly):

    D = poly.deque() #Double ended queue of the edges.
    q = poly.points()

    q.sort(key = lambda p : (p.y, -p.x))

    # Currently sweeped edges from left to right, (who has the interior of P to their right) with their resp. helpers.
    T = BST()

    while not q.empty():
        v = q.pop()

        # En fonction du cas, appeler la f°


    return 0

#O(n*log(n))
# We use the monotone decomposition of polygon, takes log(n) time
# Then, triangulating a monotone polygon is linear.
# Note : doesn't work on non simple polygons (ie poly where 2 edges intersects)
def fast_triangulation(poly):


    return 0
