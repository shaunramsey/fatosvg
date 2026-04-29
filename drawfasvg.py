# this it the main driving program for creating an FA
# the goal is to read a spec from a file and create that FA
# For now, FA's are restricted to predefined locations that are
# positioned like so:
#  *   *   *   *   *
#    *   *   *   *
#  *   *   *   *   *
# nodes are numbered starting at 1 in English reading order
# 

# drawfasvg.py
import math
import drawsvg as ds	


def drawState(name, pos, accept=False):
    c = ds.circle(pos[0], pos[1])
    if accept:
        c = ds.dblcircle(pos[0], pos[1])
    t = ds.text(name, pos, 22)
    return c + "\n" + t + "\n"

def drawFrom(name, pa, pb):
     a = ds.arrowfromto( pa[0], pa[1], pb[0], pb[1], name)
     return a

def testWrites(file):
    A = (100, 100)
    nx = 200
    B = (nx, 50)
    C = (nx, nx+10)
    D = (300, 300)
    # file.write( drawState("A", A) )
    # file.write( drawState("ha", B, True) )
    # file.write( drawState("C", C))
    # file.write( drawState("D", D))

    # file.write( drawFrom("a", A, B))
    # file.write( drawFrom("a", C, A))
    # file.write( drawFrom("a", B, D))
    # file.write( drawFrom("a", C, D))
    # file.write( drawFrom("a", D, C))

# 30 units along a vector from 1 to the other
# 100,100 is the vector so 100,100 + 30*rt2/2
with open("test.svg", "w") as file:
 
    file.write( ds.frontmatter(600,600))
    file.write( ds.arrowfromto(0,0,50,50, "straight") )


    for i in range(5):
        mypoly = f'\t<polygon fill="white" stroke-width="1" points="{100*i-10},0 {100*i},10, {100*i+10},0"/>'
        file.write(mypoly)
        mypoly = f'\t<polygon fill="white" stroke-width="1" points="0,{100*i-10} 10,{100*i}, 0,{100*i+10}"/>'
        file.write(mypoly)

    pts = []
    for i in range(4):
        pts.append( (150*i+50, 50) )
    for i in range(3):
        pts.append( (150*i+125, 200) )
    for i in range(4):
        pts.append( (150*i+50, 300))
    ct = 0
    for i in pts:
        ct += 1
        file.write(drawState(f"{ct}",i))

    for i in range(len(pts)):
        if i != 0 and i != 4:
            file.write(drawFrom("a", pts[i], pts[i-1]))
        if i != 4 and i != 0:
            file.write(drawFrom("~~~", pts[i-1], pts[i]))
    
    file.write(drawFrom("A", pts[1], pts[5]))
    file.write(drawFrom("A", pts[5], pts[1]))
    file.write(drawFrom("A", pts[2], pts[5]))
    file.write(drawFrom("A", pts[5], pts[2]))

    file.write(drawFrom("B", pts[7], pts[10]))
    file.write(drawFrom("A", pts[1], pts[5]))




    #file.write( arrowfromto( B[0], B[1], A[0], A[1]))
    #file.write( arrowfromto( A[0], A[1], B[0], B[1]))

    # startx = 100+15*math.sqrt(2)
    # endx = 200-15*math.sqrt(2)
    # theta = math.atan2(endx-startx, endx-startx)

    # file.write(stroke(startx, startx, endx, endx))
    # file.write("\n")

    # file.write(arrowhead(endx, endx, theta))
    # file.write("\n")
    #################################
    # d = circleFromThreePoints(100,100, 200, 200, 150, 200)    

    # startAngle = math.atan2(100 - d["y"], 100 - d["x"]) - 30/d["radius"]
    # endAngle = math.atan2(200 - d["y"], 200 - d["x"]) + 30/d["radius"]

    # a, sx, sy, ex,ey,sa, ea = arc(d["x"], d["y"], d["radius"], startAngle, endAngle, 1)
    # file.write(a)
    # file.write("\n")
    # print(a, sx, sy, ex, ey, sa, ea)
    # file.write(arrowhead(sx,sy,sa - math.pi / 2))
    # #file.write(circle(sx,sy))
    # file.write("\n")

    file.write(ds.backmatter())
