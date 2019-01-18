
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
