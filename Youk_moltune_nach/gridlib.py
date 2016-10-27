
import random as rd
import numpy as np
import math
import classes as cl

#Parametersettings#

x=10                              #sets gridsize
n=1.0                             #set chance of cells n probability
place=0.5                         #set on_state cells n probability
C_on=13.0                         #signalconcentration of activ cel#
K =  18.0                         #threshold c#
feedback = 0                      #positiv(1) or negative(0) feedback#
min_cell=5                        #set minimum of cellneigbors for new cellcreation#

radius=1                          #set intial radius of cell

maxrad=radius*2                   #max r which cell can have before division#

cc=0                              #the entrykey for dics
g_rate=1                          #growthrate of radius

# Dimensions
nx, ny, nz = x, x, 1
lx, ly, lz = 10.0, 10.0, 0.1
dx, dy, dz = lx/nx, ly/ny, lz/nz

ncells = nx * ny * nz
npoints = (nx + 1) * (ny + 1) * (nz + 1)

# Coordinates
x_c = np.arange(0, lx + dx, dx, dtype='float64')
y_c = np.arange(0, ly + dy, dy, dtype='float64')
z_c = np.arange(0, lz + dz, dz, dtype='float64')

r = np.zeros(npoints)         #list of cellposition in space#
state=np.arange(npoints)      #list of default state of each cell#
C_i = np.zeros(npoints)       #concentration of each cell at time i #
C_print=np.zeros(npoints)     #actual concentrations at position cells + neighbor#

resident=np.zeros(npoints)    #spot has cell or not| int references#
c_ary={}                     #cell-class ref#
pos={}                       #dic for grid [0]=x_axis [1]=y_axis#




def initialize():                               #creats grid on which cells are placed by chance

    ce = 0
    for row in range(len(x_c)):                 #grid saved in a dic#
        for col in range(len(y_c)):
            pos[ce] = [x_c[row], y_c[col]]
            ce += 1

    for cc in range(npoints):                    #cells being placed#
        put = rd.random()

        stop=(x+1)*(radius+1)

        if cc==stop:                            #only one horizontal row used#
            break

        if border(cc):                          #checks for outofbounds around edges#

            if checkneighbor(cc):               #check if cell can be placed#

                if put <= n:
                    print(cc)
                    c_ary[cc] = cl.cell(cc, 'ecoli ', radius, True)

                    occupy(cc)

    for i in c_ary.keys():                      #produce random state of cells#

        hp = rd.random()

        if hp <= place:
            c_ary[i].status = True

        else:
            c_ary[i].status = False


def border(pt):                         #checks for outofbounds around edges #

    #if pt - x * radius < 0:
        #print ('hey b_1')

        #return False
    #if pt + x * radius > ncells:
        #print ('hey b_2')

        #return False

    if pos[pt][0]-radius < 0 :
        print ('hey b_3')
        return False
    if pos[pt][1]-radius < 0 :
        print ('hey b_o4')
        return False

    if pos[pt][0] + radius > lx:
        print ('hey b_5')
        return False
    if pos[pt][1] + radius > ly:
        print ('hey b_6')
        return False

    else:
        print ('hey b_ok')
        return True


def checkneighbor(p):                   #check if can be placed#
    print('check')

    ind = True

    if p >= (npoints)**2 or p < 0:
        print ('out')
        return False

    if resident[p]!= 0:
        print('str')
        return False

    if maxrad > dx or maxrad > dy:
        ind = outersq(p)



    return ind

def outersq(p):

    rad = radius
    if p in c_ary:                      #check if cell there possible different r#
        rad = c_ary[p].radius

    for h in range(-rad, rad + 1):      #go along the (row)
        for b in range(-rad, rad + 1):  #outer quadrate of the circle r=rad (col)

            poi = p + h * x + b         #position in the chain
            if poi >= npoints:
                print ('hey f1')
                return False
            if poi < 0:
                print ('hey f2')
                return False

            eq = math.sqrt((pos[poi][0] - pos[p][0]) ** 2 + (pos[poi][1] - pos[p][1]) ** 2)

            if eq <= rad:               #if smaller or same than position inside the cell

                if resident[poi] != 0:
                    print ('hey f3')
                    return False

    return True

def occupy(m):                              #cellplacement

    if isinstance(c_ary[m], cl.cell):       #get cell_r for placement#
        rad = c_ary[m].radius

        if maxrad > dx or maxrad > dy:

            for h in range(-rad,rad+1):         # go along the (row)
                for b in range(-rad,rad+1):     #outer quadrate of the circle r=rad (col)

                    poi = m + h*x + b  # position in the chain
                    if poi == m:
                        pass

                    eq = math.sqrt((pos[poi][0] - pos[m][0]) ** 2 + (pos[poi][1] - pos[m][1]) ** 2)

                    if eq <= rad:               #if smaller or same than position inside the cell

                        if resident[poi] == 0 :
                            resident[poi] = c_ary[m].mid
        else:
            resident[m] = c_ary[m].mid




def move(p):

    if outersq(p):
        occupy(p)
    else:
        x_bp = pos[p][0] + c_ary[p].radius
        y_bp = pos[p][1] + c_ary[p].radius

        x_bn = pos[p][0] - c_ary[p].radius
        y_bn = pos[p][1] - c_ary[p].radius

        x_bp/(x+1)
    #print('shiiit'+ str(p))

def divide(p):
    pass

def growth(p):

    c_ary[p].radius = c_ary[p].radius + g_rate


def event():                                #what happens to cell in time step#

    for elem in c_ary:

        if c_ary[elem].radius >= maxrad:    #cell_r big enough -> division#
            divide(elem)

        elif c_ary[elem].status:
            growth(elem)                    #if cell=on -> grows#

        move(elem)




def update(end):

    start=0
    stop = end
    time = np.linspace(start, stop, end*10)

    timer=0

    initialize()

    for step in time:

        event()






update(1)

rei = ''
bla=0
for i in range(0, npoints):
    bla+=1
    rei = rei +'|'+ str(resident[i])
    if str(resident[i])=='0.0':
        rei=rei+' '
    if i ==120:
        print rei
        break
    elif pos[i][1]==lx and i!=0:
        print rei
        rei = ''
rei = ''
bla=0

for i in range(0, npoints):
    bla+=1
    rei = rei +'|'+ str(i)
    if i<x:
        rei=rei+' '
    if i == 120:
        print rei
        break
    elif pos[i][1]==lx and i!=0:
        print rei
        rei = ''


print(pos)
for elem in c_ary:
    print(c_ary[elem].status)
    print(c_ary[elem].radius)

