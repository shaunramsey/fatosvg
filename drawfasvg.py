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
import sys

if __name__ == "__main__":

    filename = "faspec.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    width = -1
    height = -1
    displayAllStates = False
    displayTicMarks = False
    inferSize = True

    ds.SPACING = 150
    ds.color = "white"

    edges = []
    states = {}
    names = {} #look up the position to get the name
    invnames = {} #look up name to get the position
    accept = {}
    last_offset = (0, 0)
    color_saturation = 1
    color = "#ffffff"
    with open(filename, "r") as file:
        f = file.readlines()
        for i in range(len(f)):
            first = f[i].split()
            if first[0] == "size" and len(first) > 2:
                width = int(first[1])
                height = int(first[2])
            elif first[0] == "#":
                continue #ignore #
            elif first[0] == "option" and len(first) > 1:
                if first[1] == "displayAllStates":
                    displayAllStates = True
                if first[1] == "displayTicMarks":
                    displayTicMarks = True
                if first[1] == "inferSize":
                    inferSize = True
                if first[1] == "extendWidth" and len(first) > 2:
                    ds.END_X_SPACING += int(first[2])
                if first[1] == "extendHeight" and len(first) > 2:
                    ds.END_Y_SPACING += int(first[2])

            elif first[0] == "acc":
                accept[first[1]] = True
            elif first[0] == "name":
                if len(first) > 2:
                    names[first[1]] = first[2]
                    invnames[first[2]] = first[1]
            elif first[0] == "textOffset":
                if len(first) > 2:
                    last_offset = (int(first[1]), int(first[2]))
                    #print(last_offset)
            elif first[0] == "color":
                if len(first) > 1:
                    color = first[1]
            elif len(first) > 2:
                if len(first) > 3 and first[0] == first[1]: # edge that goes to itself
                    #color = f"#{int(255*color_saturation):02x}{int(255*color_saturation):02x}{int(255*color_saturation):02x}"
                    e = ds.Edge(first[0], first[1], first[2], last_offset, color, first[3])
                    edges.append(e)
                    last_offset = (0, 0)
                    color_saturation = 1
                    color = "#ffffff"
                else:
                    #color = f"#{int(255*color_saturation):02x}{int(255*color_saturation):02x}{int(255*color_saturation):02x}"
                    e = ds.Edge(first[0], first[1], first[2], last_offset, color)
                    edges.append(e)
                    last_offset = (0, 0)
                    color_saturation = 1
                    color = "#ffffff"



    # we may infer size from positions in names
    # num_states = 1,2 then 1x1
    # num_states = 3,  then 2x2
    # num_states = 4,5 then 3x2
    # num_states = 6,7 then 4x2
    num_states = {}
    num_states[1] = (1,1)
    num_states[2] = (1,1)
    num_states[3] = (2,2)
    num_states[4] = (3,2)
    num_states[5] = (3,2)
    num_states[6] = (4,2)
    num_states[7] = (4,2)


    if width == -1 or inferSize: #infer width from largest %10 value
        max_state = 0
        for n in names.keys():
            w1 = int(n)%10
            if (int(n)//10)%2 == 0:
                w1 += 0.5
            max_state = max(max_state, w1)
        width = max_state + 1 # value 12 means width 3
    if height == -1 or inferSize: #infer height from largest /10 value
        max_state = 0
        for n in names.keys():
            print(n, int(n)//10)
            max_state = max(max_state, int(n)//10)
        height = max_state
    
    # walk through edges and figure out how many unique names there are
    unique_names = {}
    for i in edges:
        unique_names[i.i1] = True
        unique_names[i.i2] = True

    width = max(width, num_states[len(unique_names)][0])
    height = max(height, num_states[len(unique_names)][1])
    # this is the width/height based on  if 'name' was listed for each state
    print("inferred or given width/height is now ", width, height)
    positions = {}
    for j in range(height):
        w = width if j%2 == 0 else width-1
        for i in range(w):
            positions[f"{j+1}{i}"] = [False, ds.stateNumberToLocation(10+j*10+i)]
    # print("pos:", positions)

    for i in names:
        if i in positions:
            positions[i][0] = True
        else:
            raise Exception(f"Error: name {i} is not in a valid position")
            print(f"Warning: name {i} is not in positions")

    # print(f"positions: {positions}, names: {names}")




    #print(edges)  

    print(f"Creating svg with width={width} and height={height}")
    print(f"End x spacing: {ds.END_X_SPACING} end y spacing: {ds.END_Y_SPACING}")
  



    out = ds.front(width,height)
    out += ds.arrowfromto(10, 10,50,50,(0,0), "straight", 1)
    if displayTicMarks:
        out += ds.drawTicMarks(width, height, 50)

    if displayAllStates:
        out += ds.drawAllStates(width, height, names, accept)
    else:
        states = {}
        for i in edges:
            print("drawing edge:", i.name, i)
            out += ds.drawEdge(i, invnames, positions, states)
        print("states:", states)
        for i in states.keys():
            if i not in accept:
                out += ds.drawState(i, states[i], names, False)                
        for i in accept:
            out += ds.drawState(i, ds.nameToPosition(i, invnames, positions), names, True)



    out += ds.backmatter()

    # print(out)
        
    with open("test.svg", "w") as file:
        file.write(out)

