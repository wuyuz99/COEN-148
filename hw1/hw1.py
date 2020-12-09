from PIL import Image
width = 320
height = 240
img = Image.new('RGB', (width, height))
pixels = img.load()
center = [160, 120]
R = 100
color = (255, 0, 0)

def draw(x, y):
    pixels[center[0] + x, center[1] - y] = color

#draw the circle
d = 5/4 - R
x = 0
y = R
while x <= y:
    draw(x, y)  #0-45
    draw(y, x)  #45-90
    draw(y, -x) #90-135 
    draw(x, -y) #135-180
    draw(-x, -y)#180-225
    draw(-y, -x)#225-270
    draw(-y, x) #270-315
    draw(-x, y) #315-360

    x = x + 1
    if d < 0:
        d = d + 2 * x + 3
    else:
        d = d + 2 * (x - y) + 5
        y = y - 1
img.show()
img.save("circle.png")

#fill the circle
def incircle(w, h):
    return (w - center[0]) ** 2 + (h - center[1]) ** 2 < R ** 2

for w in range(width):
    for h in range(height):
        if incircle(w, h):
            pixels[w, h] = color
img.show()
img.save("circle_fill.png")

#anti-aliasing
def avg(w, h):
    preserve = 0.2
    take = (1 - preserve) / 4
    pixel = pixels[w, h]
    r = pixel[0] * preserve
    g = pixel[1] * preserve
    b = pixel[2] * preserve
    #left
    if w == 0:
        r = r + pixel[0] * take
        g = g + pixel[1] * take
        b = b + pixel[2] * take
    else:
        r = r + pixels[w - 1, h][0] * take
        g = g + pixels[w - 1, h][1] * take
        b = b + pixels[w - 1, h][2] * take
    #top
    if h == 0:
        r = r + pixel[0] * take
        g = g + pixel[1] * take
        b = b + pixel[2] * take
    else:
        r = r + pixels[w, h - 1][0] * take
        g = g + pixels[w, h - 1][1] * take
        b = b + pixels[w, h - 1][2] * take
    #right
    if w == width - 1:
        r = r + pixel[0] * take
        g = g + pixel[1] * take
        b = b + pixel[2] * take
    else:
        r = r + pixels[w + 1, h][0] * take
        g = g + pixels[w + 1, h][1] * take
        b = b + pixels[w + 1, h][2] * take
    #buttom
    if h == height - 1:
        r = r + pixel[0] * take
        g = g + pixel[1] * take
        b = b + pixel[2] * take
    else:
        r = r + pixels[w, h + 1][0] * take
        g = g + pixels[w, h + 1][1] * take
        b = b + pixels[w, h + 1][2] * take
    return (int(r), int(g), int(b))

img2 = Image.new('RGB', (width, height))
pixels2 = img2.load()
for w in range(width):
    for h in range(height):
        pixels2[w, h] = avg(w,  h)
img2.show()
img2.save("circle_aa.png")