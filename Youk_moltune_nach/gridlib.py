
import random as rd
import numpy as np
import math
import classes as cl
import vtktools
#Parametersettings#

x=100                              #sets gridsize
n=1.0                             #set chance of cells n probability
place=0.5                         #set on_state cells n probability
C_on=13.0                         #signalconcentration of activ cel#
K =  18.0                         #threshold c#
feedback = 0                      #positiv(1) or negative(0) feedback#
min_cell=5                        #set minimum of cellneigbors for new cellcreation#

radius=1                          #set intial radius of cell

maxrad=radius*2                   #max r which cell can have before division#


g_rate=1                          #growthrate of radius
k=0.9                             #factor how close neighboring cells can be
# Dimensions
nx, ny, nz = x, x, 1
lx, ly, lz = 100.0, 100.0, 0.1
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
c_ary={}                      #cell-class ref#
pos={}                        #dic for grid [0]=x_axis [1]=y_axis#

print(npoints)


def initialize():                               #creats grid on which cells are placed by chance

    ce = 0
    for row in range(len(y_c)):                 #grid saved in a dic#
        for col in range(len(x_c)):
            pos[ce] = [x_c[col], y_c[row]]
            ce += 1

    for cc in range(npoints):                    #cells being placed#
        put = rd.random()

        stop=(x+1)*(maxrad+1)

        if cc==stop:                            #only one horizontal row used#
            break

        if border(cc):                          #checks for outofbounds around edges#

            if checkneighbor(cc):               #check if cell can be placed#

                if put <= n:

                    c_ary[cc] = cl.cell(cc, 'ecoli ', radius, stategamble(), pos[cc][0], pos[cc][1], 1)
                    occupy(cc)


def stategamble():                      #prodces random booleanvalue according to place
    hp = rd.random()                    #usage: setting initial state of cell

    if hp <= place:
        return True

    else:
        return False

def border(pt):                         #checks for outofbounds around edges #


    if pos[pt][0]-maxrad < 0 :
        print ('hey b_3')
        return False
    if pos[pt][1]-maxrad < 0 :
        print ('hey b_o4')
        return False

    if pos[pt][0] + maxrad > lx:
        print ('hey b_5')
        return False
    if pos[pt][1] + maxrad > ly:
        print ('hey b_6')
        return False

    else:
        print ('hey b_ok')
        return True


def checkneighbor(p):                   #check if cell can be placed#

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

                    eq = math.sqrt((pos[poi][0] - c_ary[m].xcor) ** 2 + (pos[poi][1] - c_ary[m].ycor) ** 2)

                    if eq <= rad:               #if smaller or same than position inside the cell

                        if resident[poi] == 0 :
                            resident[poi] = c_ary[m].mid
        else:
            resident[m] = c_ary[m].mid


def force():                                     #calculates movement by forcecalc of cells pushing

    d_x = np.zeros(ncells)
    d_y = np.zeros(ncells)
    d_z = np.zeros(ncells)

    for elem in c_ary:
        for oths in c_ary:

            sum=np.square(c_ary[oths].xcor-c_ary[elem].xcor)\
            +np.square(c_ary[oths].ycor-c_ary[elem].ycor)\
            +np.square(c_ary[oths].zcor-c_ary[elem].zcor)

            d_n=np.sqrt(sum)                        #actual distance of two cells

            R = c_ary[oths].radius+c_ary[elem].radius

            if d_n==0:
                pass

            elif d_n < R :                           #checks if cell[elem] is pushed by cell[y] only when d_n < R
                fac = (k * R) - d_n

                xdd = (c_ary[oths].xcor - c_ary[elem].xcor)/d_n
                ydd = (c_ary[oths].ycor - c_ary[elem].ycor) / d_n
                zdd = (c_ary[oths].zcor - c_ary[elem].zcor) / d_n

                d_x[elem] = xdd * fac + d_x[elem]
                d_y[elem] = ydd * fac + d_y[elem]
                d_z[elem] = zdd * fac + d_z[elem]



    return d_x , d_y , d_z

def move():

    delx,dely,delz = force()

    for elem in c_ary:

        c_ary[elem].xcor = c_ary[elem].xcor + delx[elem]
        c_ary[elem].ycor = c_ary[elem].ycor + dely[elem]
        c_ary[elem].zcor = c_ary[elem].zcor + delz[elem]

    return delx, dely, delz

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

    f1,f2,f3=move()
    return f1,f2,f3




def update(end):

    start=0
    stop = end
    time = np.linspace(start, stop, end*10)

    timer=0

    initialize()

    for step in time:

        f1,f2,f3=event()
    return f1,f2,f3





fx,fy,fz=update(1)

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
    elif pos[i][0]==lx and i!=0:
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
    elif pos[i][0]==lx and i!=0:
        print rei
        rei = ''

x_list=[]
y_list=[]
z_list=[]
r_list=[]
F_x=[]
F_y=[]
F_z=[]

vtk_writer = vtktools.VTK_XML_Serial_Unstructured()

for elem in c_ary:
    x_list.append(c_ary[elem].xcor)
    y_list.append(c_ary[elem].ycor)
    z_list.append(0.0)
    r_list.append(c_ary[elem].radius)
    F_x.append(fx[elem])
    F_y.append(fy[elem])
    F_z.append(fz[elem])

print (x_list)
print(y_list)
print (r_list)


vtk_writer.snapshot("cell_arrangements.vtu",  x_list, y_list, z_list, radii = r_list, x_force = F_x, y_force = F_y, z_force = F_z )
vtk_writer.writePVD("cell_arrangements.pvd")