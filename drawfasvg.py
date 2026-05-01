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

    ds.SPACING = 150
    ds.color = "white"

    edges = []
    states = {}
    names = {}
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
            elif first[0] == "option" and len(first) > 1:
                if first[1] == "displayAllStates":
                    displayAllStates = True
                if first[1] == "displayTicMarks":
                    displayTicMarks = True
                if first[1] == "extendWidth" and len(first) > 2:
                    ds.END_X_SPACING += int(first[2])
                if first[1] == "extendHeight" and len(first) > 2:
                    ds.END_Y_SPACING += int(first[2])
            elif first[0] == "#":
                continue #ignore #
            elif first[0] == "acc":
                accept[first[1]] = True
            elif first[0] == "name":
                if len(first) > 2:
                    names[first[1]] = first[2]
            elif first[0] == "textOffset":
                if len(first) > 2:
                    last_offset = (int(first[1]), int(first[2]))
                    #print(last_offset)
            elif first[0] == "colorSaturation":
                if len(first) > 1:
                    color_saturation = float(first[1])
                    #print(color_saturation)
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
    if width == -1: #infer width from largest %10 value
        max_state = 0
        for e in edges:
            w1 = int(e.i1)%10
            w2 = int(e.i2)%10
            if (int(e.i1)//10)%2 == 0:
                w1 += 0.5
            if (int(e.i2)//10)%2 == 0:
                w2 += 0.5
            max_state = max(max_state, max(w1, w2))
        width = max_state + 1 # value 12 means width 3
    if height == -1: #infer height from largest /10 value
        max_state = 0
        for e in edges:
            max_state = max(max_state, max(int(e.i1)//10, int(e.i2)//10))
        height = max_state


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
            out += ds.drawEdge(i, states)
        for i in states.keys():
            if i not in accept:
                out += ds.drawState(i, states[i], names, False)                
        for i in accept:
            out += ds.drawState(i, ds.stateNumberToLocation(i), names, True)



    out += ds.backmatter()

    # print(out)
        
    with open("test.svg", "w") as file:
        file.write(out)

