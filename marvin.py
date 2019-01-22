import matplotlib.pyplot as plt
from data_structures import *
from convex_hull import *
from triangulation import *
from random import randint, sample
import itertools
from visibility_graph import *

def print_points(points, color='black', s=10):
    X = [p.x for p in points]
    Y = [p.y for p in points]
    plt.scatter(X, Y, s=10, color='black')

def print_segments(segments, color='blue', lw=1):
    for s in segments:
        plt.plot([s.p1.x, s.p2.x], [s.p1.y, s.p2.y], color=color, lw=lw)

def read_from_file(file):
    with open(file) as file:
        polygons = []
        robot = []
        points = []
        step = 0
        for line in file:
            if step > 2:
                break
            if line == "\n":
                step += 1
            elif step == 0:
                points = [s.split() for s in line.split(",")]
                points = [Point(int(x), int(y)) for (x, y) in points]
                polygons.append(Polygon(points))
            elif step == 1:
                points = [s.split() for s in line.split(",")]
                points = [Point(int(x), int(y)) for (x, y) in points]
                robot = Polygon(points)
            elif step == 2:
                p = line.split()
                points.append(Point(int(p[0]), int(p[1])))
        return polygons, robot, points
        
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
polygons, robot, points = read_from_file('laby.txt')


#polygons = [triangle for p in polygons for triangle in p.simple_convex_decomposition()]


for p in polygons:
    print_segments(p.segments())
    


print_segments(robot.segments(), color='b', lw=1)

result = []
for p in polygons:
    result.append(p.minkowski_sum(robot))
print("Minkowski fini")



print("Début") 
v = VisibilityGraph(result, [Point(148, 100), Point(122, 10)])
v.add_point(robot.points()[0])
print("Fin")



# for (i,p) in enumerate(result):
    # print_segments(p.segments(), color='k', lw=3)

print_segments(v.edges, color='g', lw=2)
 
 
plt.plot()
plt.show() 
a = Polygon([Point(12, 18), Point(16, 18), Point(12, 16)]) 
    





# while True:
    # str = input().split()
    # if str == []:
        # break
    # elif len(str) == 2:
        # x, y = int(str[0]), int(str[1])
        # v.add_point(Point(x, y))
    # print(24)
    # print_segments(polygon_1.segments(), color='black', lw=3)
    # print_segments(polygon_2.segments(), color='black', lw=2)
    # print_segments(polygon_3.segments(), color='black', lw=3)
    # print_segments(v.edges, color='red', lw=1)
    # plt.show()
    # plt.close()
                
                
                
                
                
