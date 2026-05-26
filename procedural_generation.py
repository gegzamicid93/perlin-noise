from math import pi, cos, sin
from random import randint, uniform
import pygame

def random_vectors_tabel():
    res=[]
    for _ in range(0,size+1):
        sup=[]
        for _ in range(0,size+1):
            angle=uniform(0,2*pi)
            sup.append([cos(angle),sin(angle)])
        res.append(sup)
    return res

def point_P_vectors(px,py):
    j = int(px) #я короче аодумала, зачем каждый раз проходиться по таблице, если ее можео с собой просто таскать
    i = int(py)
    localx = px - j
    localy = py - i
    return {
        "pos":(localx,localy),
        "vectors":(
            [localx, localy],
            [localx-1, localy],
            [localx, localy-1],
            [localx-1, localy-1]
        ),
        "cell":(i,j)
    }

def scalar_product(point_vector,original):
    i,j = point_vector["cell"]
    return {
        "pos":point_vector["pos"],
        "vectors":[
            (point_vector["vectors"][0][0]*original[i][j][0]+point_vector["vectors"][0][1]*original[i][j][1]),
            (point_vector["vectors"][1][0]*original[i][j+1][0]+point_vector["vectors"][1][1]*original[i][j+1][1]),
            (point_vector["vectors"][2][0]*original[i+1][j][0]+point_vector["vectors"][2][1]*original[i+1][j][1]),
            (point_vector["vectors"][3][0]*original[i+1][j+1][0]+point_vector["vectors"][3][1]*original[i+1][j+1][1])
    ]}

def fade(t):
    return 6*t**5-15*t**4+10*t**3

def lerp(a,b,t):
    return a+t*(b-a)

def interpolation(tabel):
    x=tabel["pos"][0]
    y=tabel["pos"][1]
    return lerp(lerp(tabel["vectors"][0],tabel["vectors"][1],fade(x)),lerp(tabel["vectors"][2],tabel["vectors"][3],fade(x)),fade(y))

def diapazon(tabel):
    res=[]
    for i in tabel:
        sup=[]
        for j in i:
            if j<-0.2:
                sup.append(-1)
            elif j<0.2:
                sup.append(0)
            else:
                sup.append(1)
        res.append(sup)
    return res

def render(tabel):
    res=[]
    for i in tabel:
        sup=[]
        for j in i:
            match j:
                case -1: sup.append('🟦')
                case 0: sup.append('🟩')
                case 1: sup.append('🟨')
        res.append(sup)
    for i in res:
        print("".join(i))
    return 0


size = 500
scale = 17
pygame.init()
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = size,size
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
orig = random_vectors_tabel()
noise=[]

for y in range(size):
    sup=[]
    for x in range(size):
        sup.append(interpolation(scalar_product(point_P_vectors(x/scale,y/scale),orig)))
    noise.append(sup)
x,y=0,0
run=True

colors1=(
    (251, 232, 89),
    (183, 219, 96),
    (117, 198, 135),
    (82, 171, 154),
    (75, 142, 157),
    (78, 111, 154),
    (85, 71, 140),
    (79, 26, 99)
)
colors2=(
    (28, 2, 27),
    (67, 12, 43),
    (100, 27, 47),
    (140, 49, 46),
    (157, 79, 60),
    (174, 110, 75),
    (214, 176, 105),
    (251, 246, 146)
)
colors3=(
    (255, 255, 255),
    (216, 216, 216),
    (180, 180, 180),
    (144, 144, 144),
    (108, 108, 108),
    (72, 72, 72),
    (36, 36, 36),
    (0, 0, 0)
)
colors4=(
    (92, 48, 64),
    (116, 64, 82),
    (140, 82, 101),
    (164, 101, 121),
    (188, 123, 143),
    (210, 148, 167),
    (232, 181, 198),
    (248, 220, 229)
)
colors5=(
    (21, 19, 112),
    (32, 29, 184),
    (23, 46, 255),
    (44, 191, 31),
    (140, 222, 33),
    (255, 236, 66),
    (255, 192, 66),
    (255, 158, 66),
)
flat=[x for row in noise for x in row]
minval=min(flat)
maxval=max(flat)
step=(maxval-minval)/8

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    y = 0
    for i in noise:
        x = 0
        for j in i:
            if j < minval+step:
                clr=colors1[0]
            elif j < minval+step*2:
                clr=colors1[1]
            elif j < minval+step*3:
                clr=colors1[2]
            elif j < minval+step*4:
                clr=colors1[3]
            elif j < minval+step*5:
                clr=colors1[4]
            elif j < minval+step*6:
                clr=colors1[5]
            elif j < minval+step*7:
                clr=colors1[6]
            else:
                clr=colors1[7]
            pygame.draw.rect(surface=screen,color=clr,rect=(x,y,2,2))
            x+=2
        y+=2
    pygame.display.flip()
    clock.tick(5)
pygame.quit()

#render(diapazon(interpolation(scalar_product(point_P_vectors(x),x))))          #это если в терминале вывести надо