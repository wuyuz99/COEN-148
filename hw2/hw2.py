# object representation
from PIL import Image, ImageDraw
import math
import csv

vert = False
IMGSIZE = 600
IMGMID = IMGSIZE / 2
img = Image.new('RGB', (IMGSIZE, IMGSIZE))

# this list hold all vertices
# you can use append() to add all x, y, z
# into it. the format could be like this:
# [[x1, y1, z1], [x2, y2, z2],......]
vertices = []
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
        #print(float(row[0]), float(row[1]), float(row[2]))

pixels = img.load()

def draw_pixel(x,y, color):
    if x >= 0 and x <= IMGSIZE and y >= 0 and y <= IMGSIZE:
        pixels[x,y] = (color,0,0)

d = 2
amp = IMGSIZE
def plotvert():
    for verticy in vertices:
        zbd = float(verticy[2]) / d
        xp = int(amp * float(verticy[0]) / (1.0 + zbd))
        yp = int(amp * float(verticy[1]) / (1.0 - zbd))
        #print(xp, yp)
        draw_pixel(IMGMID + xp, IMGMID - yp, 255)
def prottri(a, b, c):
    draw = ImageDraw.Draw(img)

    zbda = vertices[a][2] / d
    xpa = int(amp * vertices[a][0] / (1.0 + zbda))
    ypa = int(amp * vertices[a][1] / (1.0 - zbda))
    zbdb = vertices[b][2] / d
    xpb = int(amp * vertices[b][0] / (1.0 + zbdb))
    ypb = int(amp * vertices[b][1] / (1.0 - zbdb))
    zbdc = vertices[c][2] / d
    xpc = int(amp * vertices[c][0] / (1.0 + zbdc))
    ypc = int(amp * vertices[c][1] / (1.0 - zbdc))


    draw.line((IMGMID + xpa,IMGMID - ypa,IMGMID + xpb,IMGMID - ypb), fill=255)
    draw.line((IMGMID + xpa,IMGMID - ypa,IMGMID + xpc,IMGMID - ypc), fill=255)
    draw.line((IMGMID + xpc,IMGMID - ypc,IMGMID + xpb,IMGMID - ypb), fill=255)

#rotateX((180+45) / 180 * math.pi)
#rotateY(45 / 180 * math.pi)
if vert:
    plotvert()
else:
    #read index
    with open('face-index.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for index in csv_reader:
            prottri(int(index[0]), int(index[1]), int(index[2]))
        


img.show()
