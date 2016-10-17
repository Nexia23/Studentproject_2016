
import random as rd
import numpy as np
import math
import classes as cl


def initialize():                       #creats grid on which cells placed
    ce = 0
    for row in range(len(x_c)):
        for col in range(len(y_c)):
            pos[ce] = [x_c[row], y_c[col]]
            ce += 1


def border(pt):                         #checks for outofbounds around edges#

    if pt - x * radius < 0:
        return False
    if pt + x * radius > ncells:
        return False

    if pos[pt][0]-radius < 0 :
        return False
    if pos[pt][1]-radius < 0 :
        return False

    else:
        return True


def checkneighbor(p):                   # check if can be placed
    print('check')
    ind = True

    if p >= (ncells)**2 or p < 0:
        print ('out')
        return False

    if resident[p]!=0:
        #print('str')
        return False


    rad = radius

    for h in range(-rad, rad + 1):                      # go along the (row)
        for b in range(-rad, rad + 1):                  # outer quadrate of the circle r=rad (col)

            poi = p + h * x + b                         # position in the chain
            if poi >= ncells:
                return False
            if poi < 0:
                return False

            eq = math.sqrt((pos[poi][0] - pos[p][0]) ** 2 + ( pos[poi][1] - pos[p][1]) ** 2)

            if eq <= rad:                               # if smaller or same than position inside the cell

                if resident[poi]!=0:
                    ind = False

    return ind



def occupy(m):                              #cellplacement

    if isinstance(c_ary[m], cl.cell):         #check if cell there safety
        rad = c_ary[m].radius

        for h in range(-rad,rad+1):         # go along the (row)
            for b in range(-rad,rad+1):     #outer quadrate of the circle r=rad (col)

                poi = m + h*x + b  # position in the chain
                if poi == m:
                    pass

                eq = math.sqrt((pos[poi][0] - pos[m][0]) ** 2 + (pos[poi][1] - pos[m][1]) ** 2)

                if eq <= rad:               #if smaller or same than position inside the cell

                    if resident[poi] == 0 :
                        resident[poi] = c_ary[m].mid







def move(p):
    pass
    #print('shiiit'+ str(p))

#Parametersettings#

x=10                              #sets gridsize
n=1.0                             #set chance of cells n probability
place=0.5                         #set on_state cells n probability
C_on=13.0                         #signalconcentration of activ cel#
K =  18.0                         #threshold c#
feedback = 0                      #positiv(1) or negative(0) feedback#
min_cell=5                        #set minimum of cellneigbors for new cellcreation#
radius=2

cc=0                              #the entrykey for dics


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

r = np.zeros(ncells)         #list of cellposition in space#
state=np.arange(ncells)      #list of default state of each cell#
C_i = np.zeros(ncells)       #concentration of each cell at time i #
C_print=np.zeros(ncells)     #actual concentrations at position cells + neighbor#

resident=np.zeros(ncells)    #spot has cell or not| int references#
c_ary={}                     #cell-class ref#
pos={}                       #dic for grid#


initialize()


for cc in range(ncells):
    print(cc)
    put=rd.random()

    if border(cc):

        if checkneighbor(cc):

            if put<= n :
                print(cc)
                c_ary[cc] = cl.cell(cc,'ecoli ', radius, True)

                occupy(cc)
print(pos)
print(c_ary)
print(resident)



