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

color = "white"

def fixed(v, n):
    return f"{v:.3f}"


def frontmatter(width,height):
    return f"""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "https://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">

"""
def backmatter():
    return "</svg>"




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
def arrowhead(bx, by, theta):
    multx = 10
    al = 0.5
    t2x = bx - multx * math.cos(theta - al) 
    t2y = by - multx * math.sin(theta - al)
    t3x = bx - multx * math.cos(theta + al)
    t3y = by - multx * math.sin(theta + al)
    retval =  f'\t<polygon fill="{color}" stroke-width="1" points="{bx:.3f},{by:.3f} {t2x:.3f},{t2y:.3f} {t3x:.3f},{t3y:.3f}"/>\n'
    return retval


def arrowfromto(c1x, c1y, c2x, c2y, name):
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
    

    print("dx,dy,hx,hy, px,py", dx, dy, hx,hy, f"{px:.2f} {py:.2f}")
    # if dy > 0 or dx > 0:
    #     print("clock right")
    #     px = hx - counterleft[0] * 25
    #     py = hy - counterleft[1] * 25


    # print(c1x, c1y, c2x, c2y, px ,py)
    d = circleFromThreePoints(c1x, c1y, c2x, c2y, px, py)  
    #return circle(px, py)
    #return circle(d["x"],d["y"])  
    print("Circle", d)
    startAngle = math.atan2(c1y - d["y"], c1x - d["x"]) + 30/d["radius"]
    endAngle = math.atan2(c2y - d["y"], c2x - d["x"]) - 30/d["radius"]
    print(f"Start: {startAngle} end: {endAngle}")
 
    a, sx, sy, ex, ey, sa, ea = arc(d["x"], d["y"], d["radius"], startAngle, endAngle, 0)
    f = a + "\n"
    # print(a, sx, sy, ex, ey, sa, ea)
    a += arrowhead(ex, ey, ea + math.pi / 2) + "\n"
    if name != None:

        #a += circle(px,py)

        offset = 7
        a  += text(name, (hx - counterleft[0] * offset, hy - counterleft[1] * offset), 14) + "\n"
    return a
    #file.write(circle(sx,sy))



def text(str, pos, size):
    fontsize = 22
    if size != None:
        fontsize = size
    return f'\t<text fill="{color}" stroke="{color}" x="{pos[0]-0.3*fontsize*len(str):.3f}" y="{pos[1]+0.25*fontsize:.3f}" font-family="Courier New" font-size="{fontsize}">{str}</text>'

def circle(cx, cy):
    return f'\t<ellipse stroke="{color}" stroke-width="1" fill="none" cx="{cx:.3f}" cy="{cy:.3f}" rx="30" ry="30"/>\n'


def dblcircle(cx, cy):
    v = f'\t<ellipse stroke="{color}" stroke-width="1" fill="none" cx="{cx:.3f}" cy="{cy:.3f}" rx="30" ry="30"/>\n'
    v += f'\n\t<ellipse stroke="{color}" stroke-width="1" fill="none" cx="{cx:.3f}" cy="{cy:.3f}" rx="25" ry="25"/>\n'
    return v

def stroke(ax, ay, bx, by):
    return f'\t<polygon stroke="{color}" stroke-width="1" points="{ax:.3f},{ay:.3f} {bx:.3f},{by:.3f}"/>\n'


def arc(x, y, radius, startAngle, endAngle, isReversed):
    _svgData = ""
    style = 'stroke="' + color + '" stroke-width="1" fill="none"'

    if(endAngle - startAngle == math.pi * 2):
        _svgData += '\t<ellipse ' + style + ' cx="' + fixed(x, 3) + '" cy="' + fixed(y, 3) + '" rx="' + fixed(radius, 3) + '" ry="' + fixed(radius, 3) + '"/>\n';
    else:
        if(isReversed):
            startAngle, endAngle = endAngle, startAngle

        if(endAngle < startAngle):
            endAngle += math.pi * 2
        print(startAngle, endAngle)

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
