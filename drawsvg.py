# This file contains the helper functions to create an svg
# there are primitives here directly dedicated to drawing an svg

"""
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "https://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg width="800" height="600" version="1.1" xmlns="http://www.w3.org/2000/svg">
	<ellipse stroke="black" stroke-width="1" fill="none" cx="287.5" cy="129.5" rx="30" ry="30"/>
	<ellipse stroke="black" stroke-width="1" fill="none" cx="160.5" cy="140.5" rx="30" ry="30"/>
	<polygon stroke="black" stroke-width="1" points="36.5,88.5 132.834,128.898"/>
	<polygon fill="black" stroke-width="1" points="132.834,128.898 127.39,121.193 123.523,130.415"/>
	<path stroke="black" stroke-width="1" fill="none" d="M 269.123,152.958 A 74.78,74.78 0 0 1 182.637,160.449"/>
	<polygon fill="black" stroke-width="1" points="269.123,152.958 259.791,154.34 266.276,161.952"/>
</svg>
"""


arrows = """
    <polygon stroke="white" stroke-width="1" points="36.5,88.5 132.834,128.898"/>
	
	<polygon fill="white" stroke-width="1" points="132.834,128.898 127.39,121.193 123.523,130.415"/>
	<path stroke="white" stroke-width="1" fill="none" d="M 269.123,152.958 A 74.78,74.78 0 0 1 182.637,160.449"/>
    
    <polygon fill="white" stroke-width="1" points="269.123,152.958 259.791,154.34 266.276,161.952"/>

"""
import math

defaultColor = "#ffffff"
SPACING = 150
START_SPACING = 50
ODD_LINE_SPACING = 0.5*SPACING
END_X_SPACING = 40 # must account for the state size ending
END_Y_SPACING = 40 # 84 allows for an end circle and text
# END_Y_SPACING = 40

def fixed(v, n):
    return f"{v:.3f}"


def frontmatter(width,height):
    return f"""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "https://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">

"""
def front(width, height):
   return frontmatter((width-1)*SPACING + START_SPACING + END_X_SPACING, (height-1)*SPACING + START_SPACING + END_Y_SPACING) 

def getDimensions(width, height):
    return ( (width-1)*SPACING + START_SPACING + END_X_SPACING, (height-1)*SPACING + START_SPACING + END_Y_SPACING)

def backmatter():
    return "</svg>"

class Edge:
    def __init__(self, i1, i2, name, textOffset, color, pos=None):
        self.i1 = i1
        self.i2 = i2
        self.name = name
        self.textOffset = textOffset
        self.color = color
        self.pos = pos
    def __str__(self):
        return f"Edge({self.i1}, {self.i2}, {self.name}, {self.textOffset}, {self.color}, {self.pos})"
    def __repr__(self):
        return self.__str__()


#2d rot
#cos -sin
#sin cos

def det(a, b, c, d, e, f, g, h, i):
	return a*e*i + b*f*g + c*d*h - a*f*h - b*d*i - c*e*g

def circleFromThreePoints(x1, y1, x2, y2, x3, y3):
    a = det(x1, y1, 1, x2, y2, 1, x3, y3, 1)
    bx = -det(x1*x1 + y1*y1, y1, 1, x2*x2 + y2*y2, y2, 1, x3*x3 + y3*y3, y3, 1)
    by = det(x1*x1 + y1*y1, x1, 1, x2*x2 + y2*y2, x2, 1, x3*x3 + y3*y3, x3, 1)
    c = -det(x1*x1 + y1*y1, x1, y1, x2*x2 + y2*y2, x2, y2, x3*x3 + y3*y3, x3, y3)
    d = {}
    d['x'] = -bx / (2*a)
    d['y'] = -by / (2*a)
    d['radius'] = math.sqrt(bx * bx + by * by - 4 * a * c) / (2 * math.fabs(a))
    return d

#given circle centers, and an arrow between them,
def arrowhead(bx, by, theta, strokeColor=None):
    multx = 10
    al = 0.5
    if strokeColor == None:
        strokeColor = defaultColor
    t2x = bx - multx * math.cos(theta - al) 
    t2y = by - multx * math.sin(theta - al)
    t3x = bx - multx * math.cos(theta + al)
    t3y = by - multx * math.sin(theta + al)
    retval =  f'\t<polygon fill="{strokeColor}" stroke-width="1" points="{bx:.3f},{by:.3f} {t2x:.3f},{t2y:.3f} {t3x:.3f},{t3y:.3f}"/>\n'
    return retval


def arrowToSelf(cx, cy, name, textOffset, pos, color):
    fontsize = 14
    r = 20 # circle radius
    offset = 44
    labeloffset = offset + r + fontsize/2
    center_offset = (cx+offset, cy) # o bot +30, top is -30
    label_offset = (cx+labeloffset, cy)
    if pos:
        if pos == "S":
                center_offset = (cx, cy + offset)
                label_offset = (cx, cy + labeloffset)
        elif pos == "W":
                center_offset = (cx - offset, cy)
                label_offset = (cx - labeloffset, cy)
        elif pos == "N":
                center_offset = (cx, cy - offset)
                label_offset = (cx, cy - labeloffset)
        elif pos == "NE":
                center_offset = (cx + offset*math.cos(math.pi/4), cy - offset*math.sin(math.pi/4))
                label_offset = (cx + labeloffset*math.cos(math.pi/4), cy - labeloffset*math.sin(math.pi/4)) 
        elif pos == "NW":
                center_offset = (cx - offset*math.cos(math.pi/4), cy - offset*math.sin(math.pi/4))
                label_offset = (cx - labeloffset*math.cos(math.pi/4), cy - labeloffset*math.sin(math.pi/4))
        elif pos == "SE":
                center_offset = (cx + offset*math.cos(math.pi/4), cy + offset*math.sin(math.pi/4))
                label_offset = (cx + labeloffset*math.cos(math.pi/4), cy + labeloffset*math.sin(math.pi/4))
        elif pos == "SW":
                center_offset = (cx - offset*math.cos(math.pi/4), cy + offset*math.sin(math.pi/4))
                label_offset = (cx - labeloffset*math.cos(math.pi/4), cy + labeloffset*math.sin(math.pi/4))
        
        
 
    startAngle = math.atan2(cy - center_offset[1], cx - center_offset[0]) + r/30
    endAngle = math.atan2(cy - center_offset[1], cx - center_offset[0]) - r/30
    #print(f"Start: {startAngle} end: {endAngle}")
 
    a, sx, sy, ex, ey, sa, ea = arc(center_offset[0], center_offset[1], 20, startAngle, endAngle, 0, color)
    f = a + "\n"
    # print(a, sx, sy, ex, ey, sa, ea)
    a += arrowhead(ex, ey, ea + math.pi / 2 - 0.15, color) 

    a += text(name, (label_offset[0] + textOffset[0], label_offset[1] + textOffset[1]), fontsize) 

    return a



def arrowfromto(c1x, c1y, c2x, c2y, textOffset, name, color):
    dx = (c2x - c1x)
    dy = (c2y - c1y)

    size = math.sqrt(dx*dx+dy*dy)
    counterleft = (-dy / size, dx / size)
    clockright = (dy / size, dx / size)
    # -dy, dx is counter clockwise left
    hx = (c1x + c2x)*0.5
    hy = (c1y + c2y)*0.5 # half way point

    offset = 15
    px = hx - counterleft[0] * offset
    py = hy - counterleft[1] * offset
    s = 1
    if name and name == "straight":
        endx = c2x - 30 / math.sqrt(2)
        endy = c2y - 30 / math.sqrt(2)
        a = stroke(c1x, c1y, endx, endy)
        a += arrowhead(endx, endy, math.pi/4)
        return a
    

    # print("dx,dy,hx,hy, px,py", dx, dy, hx,hy, f"{px:.2f} {py:.2f}")
    # if dy > 0 or dx > 0:
    #     print("clock right")
    #     px = hx - counterleft[0] * 25
    #     py = hy - counterleft[1] * 25


    # print(c1x, c1y, c2x, c2y, px ,py)
    d = circleFromThreePoints(c1x, c1y, c2x, c2y, px, py)  
    #return circle(px, py)
    #return circle(d["x"],d["y"])  
    #print("Circle", d)
    startAngle = math.atan2(c1y - d["y"], c1x - d["x"]) + 30/d["radius"]
    endAngle = math.atan2(c2y - d["y"], c2x - d["x"]) - 30/d["radius"]
    #print(f"Start: {startAngle} end: {endAngle}")
 
    a, sx, sy, ex, ey, sa, ea = arc(d["x"], d["y"], d["radius"], startAngle, endAngle, 0, color)
    f = a + "\n"
    # print(a, sx, sy, ex, ey, sa, ea)
    a += arrowhead(ex, ey, ea + math.pi / 2, color) + "\n"
    if name != None:

        #a += circle(px,py)

        offset = 7
        a  += text(name, (hx - counterleft[0] * offset + textOffset[0], hy - counterleft[1] * offset + textOffset[1]), 14, color)
    return a
    #file.write(circle(sx,sy))



def text(str, pos, size, textColor = None):
    if textColor == None:
         textColor = defaultColor
    fontsize = 22
    if size != None:
        fontsize = size
    return f'\t<text fill="{textColor}" stroke="{textColor}" x="{pos[0]-0.3*fontsize*len(str):.3f}" y="{pos[1]+0.25*fontsize:.3f}" font-family="Courier New" font-size="{fontsize}">{str}</text>\n'

def circle(cx, cy):
    strokeColor = defaultColor
    return f'\t<ellipse stroke="{strokeColor}" stroke-width="1" fill="none" cx="{cx:.3f}" cy="{cy:.3f}" rx="30" ry="30"/>\n'


def dblcircle(cx, cy):
    strokeColor = defaultColor
    v = f'\t<ellipse stroke="{strokeColor}" stroke-width="1" fill="none" cx="{cx:.3f}" cy="{cy:.3f}" rx="30" ry="30"/>\n'
    v += f'\n\t<ellipse stroke="{strokeColor}" stroke-width="1" fill="none" cx="{cx:.3f}" cy="{cy:.3f}" rx="25" ry="25"/>\n'
    return v

def stroke(ax, ay, bx, by, strokeColor=None):
    if strokeColor == None:
        strokeColor = defaultColor
    return f'\t<polygon stroke="{strokeColor}" stroke-width="1" points="{ax:.3f},{ay:.3f} {bx:.3f},{by:.3f}"/>\n'


def arc(x, y, radius, startAngle, endAngle, isReversed, strokeColor=None):
    _svgData = ""
    if strokeColor == None:
        strokeColor = defaultColor
    style = 'stroke="' + strokeColor + '" stroke-width="1" fill="none"'

    if(endAngle - startAngle == math.pi * 2):
        _svgData += '\t<ellipse ' + style + ' cx="' + fixed(x, 3) + '" cy="' + fixed(y, 3) + '" rx="' + fixed(radius, 3) + '" ry="' + fixed(radius, 3) + '"/>\n'
    else:
        if(isReversed):
            startAngle, endAngle = endAngle, startAngle

        if(endAngle < startAngle):
            endAngle += math.pi * 2
        # print(startAngle, endAngle)

        startX = x + radius * math.cos(startAngle)
        startY = y + radius * math.sin(startAngle)
        endX = x + radius * math.cos(endAngle)
        endY = y + radius * math.sin(endAngle)
        useGreaterThan180 = (math.fabs(endAngle - startAngle) > math.pi)
        #useGreaterThan180 = 0
        goInPositiveDirection = 1

        _svgData += '\t<path ' + style + ' d="'
        _svgData += 'M ' + fixed(startX, 3) + ',' + fixed(startY, 3) + ' ' # startPoint(startX, startY)
        _svgData += 'A ' + fixed(radius, 3) + ',' + fixed(radius, 3) + ' ' # radii(radius, radius)
        _svgData += '0 '; # value of 0 means perfect circle, others mean ellipse
        if useGreaterThan180:
            _svgData += "1 "
        else:
            _svgData += "0 "
        _svgData += str(goInPositiveDirection) + ' '
        _svgData += fixed(endX, 3) + ',' + fixed(endY, 3) #  endPoint(endX, endY)
        _svgData += '"/>\n'
        return (_svgData, startX, startY, endX, endY, startAngle, endAngle)
    
def stateNumberToLocation(n):
    ax = int(n)%10 * SPACING + START_SPACING
    ay = int(n)//10 - 1
    if ay%2 != 0:
        ax += ODD_LINE_SPACING
    # print(f"stateNumber:{n} ax={ax} ay={ay*SPACING+START_SPACING}")
    return (ax, ay * SPACING + START_SPACING)

def drawState(name, pos, names, accept=False):
    c = circle(pos[0], pos[1])
    if accept:
        c = dblcircle(pos[0], pos[1])
    stateName = name
    if name in names:
         stateName = names[name]
         #print(f"Found name for {name} in names, using {stateName}")
    t = text(stateName, pos, 22)
    return c + t

def drawEdge(edge, states):
    return drawFrom(edge.name, edge.i1, edge.i2, edge.textOffset, edge.pos, edge.color, states)

def drawFrom(name, i1, i2, textOffset, pos, color, states):
    if(i1 == i2): # same state, draw a loop
        states[i1] = stateNumberToLocation(i1)
        a = arrowToSelf(states[i1][0], states[i1][1], name, textOffset, pos, color)
        return a
    
    a = stateNumberToLocation(i1)
    b = stateNumberToLocation(i2)
    states[i1] = a
    states[i2] = b
    a = arrowfromto( a[0], a[1], b[0], b[1], textOffset, name, color)
    return a

def drawTicMarks(width, height, TIC_SPACE = 25, TIC_WIDTH = 5):
    totalw, totalh = getDimensions(width, height)
    out = ""
    for i in range(int(totalw/TIC_SPACE + 1)):
        mypoly = f'\t<polygon fill="white" stroke-width="1" points="{TIC_SPACE*i-TIC_WIDTH},0 {TIC_SPACE*i},{TIC_WIDTH}, {TIC_SPACE*i+TIC_WIDTH},0"/>\n'
        out += mypoly
    for i in range(int(totalh/TIC_SPACE + 1)):
        mypoly = f'\t<polygon fill="white" stroke-width="1" points="0,{TIC_SPACE*i-TIC_WIDTH} {TIC_WIDTH},{TIC_SPACE*i}, 0,{TIC_SPACE*i+TIC_WIDTH}"/>\n'
        out += mypoly
    return out

def drawAllStates(width, height, nameLookup, acceptStates):
    pts = []
    names = []
    print(" [*] DRAWING ALL STATES")
    for i in range(0, height, 2):

        for j in range(width):
            pts.append( ( SPACING * j + START_SPACING, SPACING * i + START_SPACING) )
            names.append(f"{i+1}{j}")
      
        if height%2 == 0:
            for j in range(width-1):
                pts.append( ( SPACING * j + START_SPACING + ODD_LINE_SPACING, SPACING * (i+1) + START_SPACING) )
                names.append(f"{i+2}{j}")


    out = ""
    print(acceptStates)
    for i in range(len(pts)):
        if names[i] in acceptStates:
            out += drawState(names[i], pts[i], nameLookup, True)
        else:
            out += drawState(names[i], pts[i], nameLookup, False)

    return out

