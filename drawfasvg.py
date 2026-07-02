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
# import math
import drawsvg as ds	
import sys
import os
ghostNodeColor = "#666666"

def renderFile(filename, outfilename, bookMode=True, verbosity_level=0, forced=False):

    if not os.path.isfile(filename):
        print(f"    [XXXX] {filename} is not a file")
        return -1
    if os.path.isfile(outfilename): # don't generate unless filenamemod  is younger than outfilename crt
        # print(os.path.getctime(outfilename), os.path.getmtime(filename))
        if os.path.getmtime(outfilename) > os.path.getmtime(filename) and not forced:
            if verbosity_level > 0:
                print(f"   [****] {outfilename} is already up to date compared to {filename}")
            return -1
        # else:
        #     print(f" {os.path.getctime(outfilename)}, {os.path.getctime(filename)}")
        #     print(f" {os.path.getmtime(outfilename)}, {os.path.getmtime(filename)}")

    # we may infer size from positions in names
    # num_states = 1,2 then 1x1
    # num_states = 3,  then 2x2
    # num_states = 4,5 then 3x2
    # num_states = 6,7 then 4x2
    num_states = {}
    num_states[0] = (0,0)
    num_states[1] = (1,1)
    num_states[2] = (2,1)
    num_states[3] = (2,2)
    num_states[4] = (3,2)
    num_states[5] = (3,2)
    num_states[6] = (4,2)
    num_states[7] = (4,2)

    width = -1
    height = -1
    displayNamedStates = False
    displayAllStates = False
    displayTicMarks = False
    inferSize = True
    if not bookMode:
        ds.defaultColor = "#000000"
    ds.SPACING = 150
    ds.END_X_SPACING = 40
    ds.END_Y_SPACING = 40
    startState = "10"
    edges = []
    states = {}
    names = {} #look up the position to get the name
    invnames = {} #look up name to get the position
    positionOffsets = {} #name has position offset 
    accept = {}
    hidden = {} # don't draw these states circles
    hiddenEdges = []
    last_text_pct = 0.5
    last_offset = (0, 0)
    last_color = ds.defaultColor
    last_bend = 0
    last_hide = False
    highlightNode = None

    with open(filename, "r") as file:
        f = file.readlines()
        for i in range(len(f)):
            first = f[i].split()
            if len(first) == 0:
               continue
            if first[0] == "size" and len(first) > 2:
                width = int(first[1])
                height = int(first[2])
                inferSize = False
            elif first[0] == "#":
                continue #ignore #
            elif first[0] == "option" and len(first) > 1:
                if first[1] == "displayAllStates":
                    displayAllStates = True
                elif first[1] == "displayNamedStates":
                    displayNamedStates = True
                elif first[1] == "displayTicMarks":
                    displayTicMarks = True
                elif first[1] == "extendWidth" and len(first) > 2:
                    ds.END_X_SPACING += int(first[2])
                elif first[1] == "extendHeight" and len(first) > 2:
                    ds.END_Y_SPACING += int(first[2])
                elif first[1] == "defaultColor":
                    ds.defaultColor = first[2]
                elif first[1] == "highlightNode":
                    highlightNode = first[2]
                else:
                    print(f" [XXX] option does not exist: ${f[i]}")
                
            elif first[0] == "bend":
                last_bend = int(first[1])
            elif first[0] == "acc" and "acc" not in invnames:
                accept[first[1]] = True
            elif first[0] == "accept":
                accept[first[1]] = True
            elif first[0] == "hide" and len(first) > 1:
                hidden[first[1]] = True
            elif first[0] == "hideedge":
                last_hide = True
            elif first[0] == "start":
                if len(first) > 1:
                    startState = first[1]
            elif first[0] == "name":
                if len(first) > 2:
                    names[first[1]] = first[2]
                    invnames[first[2]] = first[1]
            elif first[0] == "posOffset":
                if len(first) > 3:
                    positionOffsets[first[1]] = (int(first[2]), int(first[3]))
            elif first[0] == "textOffset":
                if len(first) > 2:
                    last_offset = (int(first[1]), int(first[2]))
                    #print(last_offset)
            elif first[0] == "textPct":
                if len(first) > 1:
                    last_text_pct = float(first[1])
            elif first[0] == "color":
                if len(first) > 1:
                    last_color = first[1]
            elif len(first) > 2:
                pos = None
                if len(first) > 3 and first[0] == first[1]: # edge that goes to itself
                    pos = first[3]
                    #color = f"#{int(255*color_saturation):02x}{int(255*color_saturation):02x}{int(255*color_saturation):02x}"
                e = ds.Edge(first[0], first[1], first[2], last_offset, last_text_pct, last_color, last_bend, pos)
                if last_hide:
                    hiddenEdges.append(e)
                edges.append(e)
                last_text_pct = 0.5
                last_offset = (0, 0)
                last_color = ds.defaultColor
                last_bend = 0
                last_hide = False



 


    if width == -1 or inferSize: #infer width from largest %10 value
        max_state = 0
        for n in names.keys():
            w1 = int(n)%10
            if (int(n)//10)%2 == 0:
                w1 += 1
            max_state = max(max_state, w1)
        width = max_state + 1 # value 12 means width 3
    if height == -1 or inferSize: #infer height from largest /10 value
        max_state = 0
        for n in names.keys():
            # print(n, int(n)//10)
            max_state = max(max_state, int(n)//10)
        height = max_state
    
    # walk through edges and figure out how many unique names there are
    unique_names = {}
    for i in edges:
        unique_names[i.i1] = True
        unique_names[i.i2] = True

    if len(unique_names) in num_states:
        width = max(width, num_states[len(unique_names)][0])
        height = max(height, num_states[len(unique_names)][1])
    else:
        print(edges)
        print("unique names", unique_names)
        print(len(unique_names), num_states)
    # this is the width/height based on  if 'name' was listed for each state
    # print(" [*] inferred or given width/height is now ", width, height)
    positions = {}
    for j in range(height):
        w = width if j%2 == 0 else width-1
        for i in range(w):
            positions[f"{j+1}{i}"] = [False, ds.stateNumberToLocation(10+j*10+i)]
    # print("pos:", positions)
    for i in positionOffsets:
        positions[i][1][0] += positionOffsets[i][0]
        positions[i][1][1] += positionOffsets[i][1]
    for i in names:
        if i in positions:
            positions[i][0] = True
        else:
            raise Exception(f"Error: name {i} is not in a valid position")
            print(f"Warning: name {i} is not in positions")

    # print(f"positions: {positions}, names: {names}")




    #print(edges)  

    if verbosity_level > 1:
        if displayAllStates:
            print(f"   [x] Option: Display All States is True")
        if displayTicMarks:
            print(f"   [x] Option: Display Tic Marks is True")
        print(f"   (*) Creating svg with width={width} and height={height}")
        print(f"     (-) End x spacing: {ds.END_X_SPACING} end y spacing: {ds.END_Y_SPACING}")
        print(f"     (-) # of Unique States = {len(unique_names)}")
        print(f"     (-) # of Positions = {len(positions)}")

  

    out = ds.front(width,height)

    # PRINT THE STARTING ARROW
    startLineOffset = 50
    # print(positions)
    startPos = positions[startState][1]
    if highlightNode == None:
        out += ds.arrowfromto(startPos[0] - startLineOffset, startPos[1] - startLineOffset, startPos[0], startPos[1], (0,0), 0.5, "straight", 1, 0)
    
    # DISPLAY TIC MARKS
    if displayTicMarks:
        out += ds.drawTicMarks(width, height, 20)

    # DISPLAY ALL THE STATES OR ONLY NAMED STATES - NO TRANSITIONS
    if displayAllStates:
        out += ds.drawAllStates(width, height, names, accept, positionOffsets, False)
    elif displayNamedStates:
        out += ds.drawAllStates(width, height, names, accept, positionOffsets, True)
    else: # DRAW THE DIAGRAM WITH GIVEN OPTIONS
        states = {}
        # print("hidden edges: ", hiddenEdges)
        for i in edges:
            # print("drawing edge:", i.name, i)
            if i not in hiddenEdges:
                out += ds.drawEdge(i, invnames, positions, states, highlightNode)
            else:
                states[i.i1] = ds.nameToPosition(i.i1, invnames, positions)
                states[i.i2] = ds.nameToPosition(i.i2, invnames, positions)
        # print("states:", states)
        for i in states.keys():
            # print(states, accept, hidden, i)
            if (i not in accept) and not (i in hidden) and (highlightNode == None or i == highlightNode):
                out += ds.drawState(i, states[i], names, False)   
            elif (i not in accept) and not (i in hidden):
                out += ds.drawState(i, states[i], names, False, ghostNodeColor)             
        for i in accept:
            if i not in hidden and (highlightNode == None or i == highlightNode):
                out += ds.drawState(i, ds.nameToPosition(i, invnames, positions), names, True)
            elif (i not in hidden):
                out += ds.drawState(i, ds.nameToPosition(i, invnames, positions), names, True, ghostNodeColor)



    out += ds.backmatter()

    # print(out)
    with open(outfilename, "w") as file:
        file.write(out)

def help():
    print(" Welcome to the FA to SVG converter")
    print("Command Line Options    Description")
    print("-----------------------------------")
    print("-f            \t\tForce create svg despite timestamps")
    print("-i <filename> \t\tSpecify a singular input file name")
    print("-o <filename> \t\tSpecify a singular output filename")
    print("-d <dir_name> \t\tSpecify a directory of fa files as inputs")
    print("-od <dr_name> \t\tSpecify the output directory for svg files default fa/svg")
    print("-----------------------------------")
    print("DEFAULTS")
    print("-i fa/faspec.fa")
    print("-o fa/svg/faspec.svg")
    print("-od <dir_name>/svg     Defaults to the -d name as name/svg")

if __name__ == "__main__":

    filenames = ["fa/faspec.fa"]
    outfilenames = ["fa/svg/faspec.svg"]
    usingDefault = True
    outputDirectory = None #defaults to dirName/svg
    dirName = None
    bookSettings = True # 
    verbosity_level = 0 # 0 is silent, 1 is some info, 2 is more ... 10 is all DEBUG
    forced = False 

    if len(sys.argv) > 1:
        for i in range(len(sys.argv)):
            arg = sys.argv[i]
            if arg == "-i": #input filename
                filenames[0] = sys.argv[i+1]
                if usingDefault:
                    outfilenames[0] = filenames[0][:-2] + "svg"
                usingDefault = False
            if arg == "-o":
                outfilenames[0] = sys.argv[i+1]
                usingDefault = False
            if arg == "-d": # specify input directory
                dirName = sys.argv[i+1]
                if dirName[-1] != "/": # add it then
                    dirName += "/"
                if outputDirectory == None:
                    outputDirectory = f"{dirName}svg/"
                filenames = [dirName + f for f in os.listdir(dirName) if os.path.isfile(dirName + f)]
                outfilenames = [f"{outputDirectory}{f[len(dirName):-2]}svg" for f in filenames]
            if arg == "-od": # specify output directory
                outputDirectory = sys.argv[i+1]
                if outputDirectory[-1] != "/": # add it
                    outputDirectory += "/"
                if dirName != None: # input dir already specified
                    outfilenames = [f"{outputDirectory}{f[len(dirName):-2]}svg" for f in filenames]
            if arg == "-nb": #turn off book specific settings
                bookSettings = False
            if arg == "-h":
                help()
                sys.exit(0)
            if arg == "-f":
                forced = True
    
    if outputDirectory != None and not os.path.isdir(outputDirectory):
        help()
        print("*"*80)
        print(f"   [XXXX] {outputDirectory} is not an existing directory name.")
        print("*"*80)
        sys.exit(0)
   
    print(f" [*] Rendering up to [{len(filenames)}] '.fa' files that require updating.")    
    newout = 0
    for i in range(len(filenames)):
        if bookSettings:
            out = outfilenames[i][:-4] + "-white.svg"
            ghostNodeColor = "#666666"
            if verbosity_level > 0:
                print(f" [*] Rendering {filenames[i]} to {out}")
            ds.defaultColor = "white"
            result1 = renderFile(filenames[i], out, bookSettings, verbosity_level, forced)
            if result1 == None:
                newout += 1
            ds.defaultColor = "black"
            ghostNodeColor = "#cccccc"
            out = outfilenames[i][:-4] + "-black.svg"
            if verbosity_level > 1:
                print(f" [*] Rendering {filenames[i]} to {out}")
            result2 = renderFile(filenames[i], out, bookSettings, verbosity_level, forced)
            if result2 == None:
                newout += 1
            #take outfilenames[i][:4] and produce the book cod
            if result1 == None and result2 == None:
                name = outfilenames[i][:-4]
                path = name.split("/")
                print("-"*60)
                print("")
                print(f"::: {{#fig-{path[-1]}}}")
                print("::: {.light-content}")
                print(f"![](/images/RL/{path[-1]}-black.svg)")
                print(":::")
                print("")
                print("::: {.dark-content}")
                print(f"![](/images/RL/{path[-1]}-white.svg)")
                print(":::")
                print("")
                print("Caption")
                print(":::")
                print("")
                print("-"*60)
    print(f" [*] Done rendering. [{newout}] new '.svg' files were created.")

   

