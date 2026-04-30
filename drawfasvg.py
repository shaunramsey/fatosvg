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

SPACING = 150
START_SPACING = 50
ODD_LINE_SPACING = 0.5*SPACING
END_X_SPACING = 40 # must account for the state size ending
END_Y_SPACING = 70
def stateNumberToLocation(n):
    ax = int(n)%10 * SPACING + START_SPACING
    ay = int(n)//10 - 1
    print("stateNumber: ay=", ay)
    if ay%2 != 0:
        ax += ODD_LINE_SPACING
    return (ax, ay * SPACING + START_SPACING)

if __name__ == "__main__":
    width = 2
    height = 2
    displayAllStates = False

    edges = []
    states = {}
    accept = []
    with open("faspec.txt", "r") as file:
        f = file.readlines()
        for i in range(len(f)):
            first = f[i].split()
            if first[0] == "size" and len(first) > 2:
                width = int(first[1])
                height = int(first[2])
            elif first[0] == "option" and len(first) > 1:
                if first[1] == "displayAllStates":
                    displayAllStates = True
            elif first[0] == "#":
                continue #ignore #
            elif first[0] == "acc":
                accept.append(first[1])
            elif len(first) > 2:
                edges.append((first[0], first[1], first[2]))


    print(edges)  

    print(f"Creating svg with width={width} and height={height}")
  

    out = ds.frontmatter((width-1)*SPACING + START_SPACING + END_X_SPACING, (height-1)*SPACING + START_SPACING + END_Y_SPACING) 
    out += ds.arrowfromto(0,0,50,50, "straight") 

    totalw = width*SPACING + START_SPACING
    totalh = height*SPACING + START_SPACING
    print(f"totalw,totalh = ({totalw}, {totalh})")
    TIC_SPACE = 25
    ARROW_WIDTH = 5
    for i in range(totalw//TIC_SPACE + 1):
        mypoly = f'\t<polygon fill="white" stroke-width="1" points="{TIC_SPACE*i-ARROW_WIDTH},0 {TIC_SPACE*i},{ARROW_WIDTH}, {TIC_SPACE*i+ARROW_WIDTH},0"/>\n'
        out += mypoly
    for i in range(totalh//TIC_SPACE + 1):
        mypoly = f'\t<polygon fill="white" stroke-width="1" points="0,{TIC_SPACE*i-ARROW_WIDTH} {ARROW_WIDTH},{TIC_SPACE*i}, 0,{TIC_SPACE*i+ARROW_WIDTH}"/>\n'
        out += mypoly

    if displayAllStates:
        pts = []
        names = []
        v = width # int( (width*150 - 50) / 150)
        current_y = 50
        hi = 1
        while current_y < height*150+50:
            for i in range(v):
                pts.append( (150*i+50, current_y) )
                names.append(f"{hi}{i}")
            current_y += 150
            hi += 1
            if current_y >= height*150:
                break
            for i in range(v-1):
                pts.append( (150*i+125, current_y) )
                names.append(f"{hi}{i}")
            current_y += 150
            hi += 1
        ct = 0
        for i in range(len(pts)):
            ct += 1
            out += drawState(names[i], pts[i])
    
    states = {}
    for i in edges:
        a = stateNumberToLocation(i[0])
        b = stateNumberToLocation(i[1])
        print(i[2],a,b)
        out += drawFrom(i[2],a,b)
        states[i[0]] = a
        states[i[1]] = b

    for i in states.keys():
        if i in accept:
            out += drawState(i, states[i], True)
            accept.remove(i)
        else:
            out += drawState(i, states[i], False)
    for i in accept:
        print("drawing accept states",i, stateNumberToLocation(i))
        out += drawState(i, stateNumberToLocation(i), True)

    i = 20
    l = stateNumberToLocation(i)

    offset = 44
    center_offset = (l[0]+offset,l[1]) # o bot +30, top is -30
    center_offset = (l[0], l[1]+offset)
    r = 20 # circle radius
    startAngle = math.atan2(l[1] - center_offset[1], l[0] - center_offset[0]) + r/30
    endAngle = math.atan2(l[1] - center_offset[1], l[0] - center_offset[0]) - r/30
    #print(f"Start: {startAngle} end: {endAngle}")
 
    a, sx, sy, ex, ey, sa, ea = ds.arc(center_offset[0], center_offset[1], 20, startAngle, endAngle, 0)
    f = a + "\n"
    # print(a, sx, sy, ex, ey, sa, ea)
    a += ds.arrowhead(ex, ey, ea + math.pi / 2 - 0.15) + "\n"
    out += a
    out += ds.backmatter()

    # print(out)
        
    with open("test.svg", "w") as file:
        file.write(out)

