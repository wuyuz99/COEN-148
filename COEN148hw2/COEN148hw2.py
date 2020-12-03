# object representation
import cv2
import numpy as np
import math
import csv

vert = True
IMGSIZE = 600
IMGMID = int(IMGSIZE / 2)
d = 2
amp = IMGSIZE
sens = 0.005
pixels = np.zeros((IMGSIZE, IMGSIZE, 3), np.uint8)
# this list hold all vertices
# you can use append() to add all x, y, z
# into it. the format could be like this:
# [[x1, y1, z1], [x2, y2, z2],......]
vertices = []
indexes = []

def rotateX(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    for i in range(len(vertices)):
        ver = vertices[i]
        tmp = [0.0, 0.0, 0.0]
        tmp[0] = ver[0]
        tmp[1] = cos * ver[1] - sin * ver[2]    
        tmp[2] = sin * ver[1] + cos * ver[2]   
        vertices[i] = tmp

def rotateY(theta):
    cos = math.cos(theta)
    sin = math.sin(theta)
    for i in range(len(vertices)):
        ver = vertices[i]
        tmp = [0.0, 0.0, 0.0]
        tmp[0] = ver[2] * sin + ver[0] * cos
        tmp[1] = ver[1]
        tmp[2] = -sin * ver[0] + cos * ver[2]
        #print(vertices[i])
        #print(tmp)
        vertices[i] = tmp

#read in face vertices
with open('face-vertices.data') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:    
        vertices.append([float(x) for x in row])

#read in face indexes
with open('face-index.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for index in csv_reader:
            indexes.append(index)

def clean():
    global pixels
    pixels = np.zeros((IMGSIZE, IMGSIZE, 3), np.uint8)

def draw_pixel(x, y, color):
    if x >= 0 and x < IMGSIZE and y >= 0 and y < IMGSIZE:
        pixels[int(y)][int(x)][0] = color

def plotvert():
    for verticy in vertices:
        zbd = float(verticy[2]) / d
        xp = int(amp * verticy[0] / (1.0 + zbd))
        yp = int(amp * verticy[1] / (1.0 - zbd))
        #print(xp, yp)
        draw_pixel(IMGMID + xp, IMGMID - yp, 255)

def prottri(a, b, c):
    zbda = vertices[a][2] / d
    xpa = int(amp * vertices[a][0] / (1.0 + zbda))
    ypa = int(amp * vertices[a][1] / (1.0 - zbda))
    zbdb = vertices[b][2] / d
    xpb = int(amp * vertices[b][0] / (1.0 + zbdb))
    ypb = int(amp * vertices[b][1] / (1.0 - zbdb))
    zbdc = vertices[c][2] / d
    xpc = int(amp * vertices[c][0] / (1.0 + zbdc))
    ypc = int(amp * vertices[c][1] / (1.0 - zbdc))

    cv2.line(pixels, (IMGMID + xpa, IMGMID - ypa), (IMGMID + xpb, IMGMID - ypb), (255, 0, 0))
    cv2.line(pixels, (IMGMID + xpa, IMGMID - ypa), (IMGMID + xpc, IMGMID - ypc), (255, 0, 0))
    cv2.line(pixels, (IMGMID + xpc, IMGMID - ypc), (IMGMID + xpb, IMGMID - ypb), (255, 0, 0))

def plotlines():
    for index in indexes:
        prottri(int(index[0]), int(index[1]), int(index[2]))

def refresh():
    clean()
    cv2.putText(pixels, "hold left mouse buttom to rotate", (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    cv2.putText(pixels, "hold right mouse buttom and move up/down to zoom", (0,24), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    cv2.putText(pixels, "press c to change view", (0,38), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    cv2.putText(pixels, "press esc to change escape", (0,52), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    if vert:
        plotvert()
    else:
        plotlines()
    cv2.imshow("image", pixels)

prevxl = -1 
prevyl = -1
prevyr = -1
def rotate_and_zoom(event, x, y, flags, param):
    global prevxl
    global prevyl
    global prevyr
    global amp
    if vert:        #limits the threashold to refresh to reduce computation
        th = 40
    else:
        th = 60
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON :
        if prevxl != -1:
            xdiffl = prevxl - x
            ydiffl = prevyl - y
            if abs(xdiffl) + abs(ydiffl) > th:
                rotateX(sens * -(ydiffl))
                rotateY(sens * -(xdiffl))
                refresh()
                prevxl = x
                prevyl = y
        else:
            prevxl = x
            prevyl = y
    if event == cv2.EVENT_LBUTTONUP:
        prevxl = -1
        prevyl = -1
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_RBUTTON :
        if prevyr != -1:
            ydiffr = prevyr - y
            if abs(ydiffr) > th/3:
                amp = amp * math.e**(0.005 * ydiffr)
                refresh()
                prevyr = y
        else:
            prevyr = y
    if event == cv2.EVENT_RBUTTONUP:
        prevyr = -1
        
rotateX((-15) / 180 * math.pi)
rotateY(-30 / 180 * math.pi)

refresh()
cv2.setMouseCallback("image", rotate_and_zoom)

while True:
    k = cv2.waitKey(200)
    if k == 27:     #esc
        break
    if k == 99 or k == 67:    #'c' or 'C'
        vert = not vert
        refresh()
cv2.destroyAllWindows()
