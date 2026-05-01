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


if __name__ == "__main__":
    width = 2
    height = 2
    displayAllStates = False

    edges = []
    states = {}
    names = {}
    accept = []
    last_offset = (0, 0)
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
            elif first[0] == "name":
                if len(first) > 2:
                    names[first[1]] = first[2]
            elif first[0] == "textOffset":
                if len(first) > 2:
                    last_offset = (int(first[1]), int(first[2])) 
            elif len(first) > 2:
                if len(first) > 3 and first[0] == first[1]: # edge that goes to itself
                    edges.append((first[0], first[1], first[2], last_offset, first[3]))
                    last_offset = (0,0)
                else:
                    edges.append((first[0], first[1], first[2], last_offset))
                    last_offset = (0, 0)


    print(edges)  

    print(f"Creating svg with width={width} and height={height}")
  

    ds.SPACING = 150
    ds.color = "white"

    ##### DO WE HAVE A SOUTH FACING LOOP/ ARROW IN THE LAST ROW?
    ds.END_Y_SPACING += 44
    ds.END_X_SPACING += 44

    out = ds.front(width,height)
    out += ds.arrowfromto(0,0,50,50,(0,0), "straight") 
    out += ds.drawTicMarks(width, height, 50)

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
            out += ds.drawState(names[i], pts[i])
    else:
        states = {}
        for i in edges:
            out += ds.drawEdge(i, states) 

        for i in states.keys():
            if i in accept:
                out += ds.drawState(i, states[i], names, True)
                accept.remove(i)
            else:
                out += ds.drawState(i, states[i], names, False)
                
        for i in accept:
            print("drawing accept states",i, ds.stateNumberToLocation(i))
            out += ds.drawState(i, ds.stateNumberToLocation(i), names, True)



    out += ds.backmatter()

    # print(out)
        
    with open("test.svg", "w") as file:
        file.write(out)

