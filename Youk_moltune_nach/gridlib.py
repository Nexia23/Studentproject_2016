import random as rd
import numpy as np
import classes as cl
import vtktools
import present as pres
import hl

#Parametersettings#
x=10                             #sets gridsize
n=1.0                             #set chance of cells n probability
place=0.6                         #set on_state cells n probability
C_on=17.0                         #signalconcentration of activ cel#
K =  18.0                         #threshold c#
feedback = 1                      #positiv(1) or negative(0) feedback#

radius=1                          #set intial radius of cell
maxrad=radius*2                   #max r which cell can have before division#
k=1.0                             #factor how close neighboring cells can be
g_rate=0.2                        #growthrate of radius

F_g = 0.002                       #gravity
threeD=1

# Dimensions
nx, ny, nz = x, x, 1
if threeD:
    nz = x
lx, ly, lz = 10.0, 10.0, 0.1
if threeD:
    lz = 10.0
dx, dy, dz = lx/nx, ly/ny, lz/nz

ncells = nx * ny * nz
npoints = (nx + 1) * (ny + 1) * (nz + 1)

# Coordinates
x_c = np.arange(0, lx + dx, dx, dtype='float64')
y_c = np.arange(0, ly + dy, dy, dtype='float64')
z_c = np.arange(0, lz + dz, dz, dtype='float64')


C_t=[]                        # concentrations at time step#
state_t=[]                    #lists all individual cellstates at timestep#

resident=np.zeros(npoints)    #spot has cell or not| int references#
c_ary={}                      #cell-class ref#
pos={}                        #dic for grid [0]=x_axis [1]=y_axis#

ita=20                        #iteration of movefunc, cause explicit procedure

fx = np.zeros(ncells)
fy = np.zeros(ncells)
fz = np.zeros(ncells)

def initialize():                               #creats grid on which cells are placed by chance
    if not threeD:
        ce = 0
        for row in range(len(y_c)):                 #grid saved in a dic#
            for col in range(len(x_c)):
                pos[ce] = [x_c[col], y_c[row]]
                ce += 1
    else:
        ce = 0
        for wth in range(len(y_c)):
            for row in range(len(z_c)):  # grid saved in a dic#
                for col in range(len(x_c)):

                    pos[ce] = [x_c[col], y_c[row],z_c[wth]]
                    ce += 1
    c_num=0
    start= (x + 1 ) ** 2 * (maxrad)
    stop = (x + 1) ** 2 * (maxrad + 1)
    print start,stop
    for cc in range(start,stop):                    #cells being placed#
        put = rd.random()

        if cc==stop:                            #only one horizontal row used#
            break

        if border(cc):                          #checks for outofbounds around edges#
            if checkneighbor(cc):               #check if cell can be placed#

                if put <= n:
                    c_ary[c_num] = cl.cell(c_num, 'ecoli ', radius, stategamble(), pos[cc][0], pos[cc][1], pos[cc][2])
                    occupy(cc,c_num)
                    c_num += 1

    cgrad = cl.c_grad(len(c_ary), x, n, place, C_on, K, feedback, c_ary, threeD)
    C_i, state = cgrad.ini_cell_c()

    C_t.append(list(C_i))
    state_t.append(list(state))

def stategamble():                      #prodces random booleanvalue according to place
                                        #usage: setting initial state of cell
    hp = rd.random()
    if hp <= place:
        return True
    else:
        return False

def border(pt):                         #checks for outofbounds around edges #


    if pos[pt][0] - radius < 0 :
        print ('hey b_3')
        return False
    if pos[pt][1] - radius < 0 :
        print ('hey b_o4')
        return False
    if pos[pt][2] - radius < 0:
        print ('hey b_o4')
        return False

    if pos[pt][0] + radius > lx:
        print ('hey b_5')
        return False
    if pos[pt][1] + radius > ly:
        print ('hey b_6')
        return False
    if pos[pt][2] + radius > lz:
        print ('hey b_6')
        return False

    else:
        print ('hey b_ok')
        return True

def checkneighbor(p):                   #check if cell can be placed#

    ind = True

    if p >= (npoints) or p < 0:
        print ('out')
        return False

    if resident[p]!= 0:
        print('str')
        return False

    if maxrad > dx or maxrad > dy or maxrad > dz:
        ind = outersq(p)

    return ind

def outersq(p):

    rad = radius

    for h in range(-rad, rad + 1):      #go along the (row)
        for b in range(-rad, rad + 1):  #outer quadrate of the circle r=rad (col)
            for l in range(-rad, rad + 1):

                poi = p + b + h * x +  l * x * x        #position in the chain
                if poi >= npoints:
                    print ('hey f1')
                    return False
                if poi < 0:
                    print ('hey f2')
                    return False

                eq = np.sqrt((pos[poi][0] - pos[p][0]) ** 2 + (pos[poi][1] - pos[p][1]) ** 2 + (pos[poi][2] - pos[p][2]) ** 2)

                if eq <= rad:               #if smaller or same than position inside the cell

                    if resident[poi] != 0:
                        print ('hey f3')
                        return False

    return True

def occupy(m,id):                              #cellplacement

    if isinstance(c_ary[id], cl.cell):       #get cell_r for placement#
        rad = radius

        if maxrad > dx or maxrad > dy:

            for h in range(-rad,rad+1):         # go along the (row)
                for b in range(-rad,rad+1):     #outer quadrate of the circle r=rad (col)
                    for l in range(-rad, rad + 1):

                        poi = m + b + h * x  + l * x * x  # position in the chain
                        if poi == m:
                            pass

                        eq = np.sqrt((pos[poi][0] - c_ary[id].xcor) ** 2 + (pos[poi][1] - c_ary[id].ycor) ** 2 + (pos[poi][2] - c_ary[id].zcor) ** 2)

                        if eq <= rad:               #if smaller or same than position inside the cell

                            if resident[poi] == 0 :
                                resident[poi] = c_ary[id].mid
        else:
            resident[m] = c_ary[id].mid

def force():                                    #calculates movement by forcecalc of cells pushing

    thres=np.zeros(ncells)                      #array for saving the fac as threshold

    for elem in c_ary:
        fx[elem]=0
        fy[elem]=0
        if threeD:
            fz[elem]=0
        for oths in c_ary:

            if c_ary[elem].xcor <= c_ary[elem].radius:
                c_ary[elem].xcor = c_ary[elem].radius
            if c_ary[elem].ycor <= c_ary[elem].radius:
                c_ary[elem].ycor = c_ary[elem].radius
            if c_ary[elem].zcor <= c_ary[elem].radius:
                c_ary[elem].zcor = c_ary[elem].radius

            sum=np.square(c_ary[oths].xcor-c_ary[elem].xcor)\
            +np.square(c_ary[oths].ycor-c_ary[elem].ycor)\
            +np.square(c_ary[oths].zcor-c_ary[elem].zcor)

            d_n=np.sqrt(sum)                            #actual distance of two cells

            R = c_ary[oths].radius+c_ary[elem].radius

            if d_n == 0:
                continue

            elif d_n < k*R :                           #checks if cell[elem] is pushed by cell[y] only when d_n < R
                fac = (k * R) - d_n


                xdd = -(c_ary[oths].xcor - c_ary[elem].xcor) / d_n
                ydd = -(c_ary[oths].ycor - c_ary[elem].ycor) / d_n
                zdd = -(c_ary[oths].zcor - c_ary[elem].zcor) / d_n

                thres[oths]= fac

                fx[elem] = xdd * fac + fx[elem]
                fy[elem] = ydd * fac + fy[elem]
                if threeD:
                    fz[elem] = zdd * fac + fz[elem]
        thres[elem]=max(thres)

    return max(thres)

def move():                                                 #cells being moved as forces dictate

    thrs=force()
    if not max(np.square(max(fx)),np.square(max(fy)),np.square(max(fz))) == 0:
        dt = 0.1 / np.sqrt(max(np.square(max(fx)),
                       np.square(max(fy)),
                       np.square(max(fz))))
    else:
        dt = 0.1
    for elem in c_ary:
        grav = -4 * np.pi * np.square(c_ary[elem].radius) * F_g
        y_cor=max(0,min((c_ary[elem].ycor + dt * fy[elem] + grav),ly))

        c_ary[elem].xcor = max(min(c_ary[elem].xcor + dt*fx[elem],lx),0)
        c_ary[elem].ycor = max(y_cor,radius)
        if threeD:
            c_ary[elem].zcor = max(min(c_ary[elem].zcor + dt*fz[elem],lz),0)

    return thrs

def rdspot(p):      #after muller 1959/Marsaglia 1972 picking random point on sphere uniform

    x_r = rd.gauss(0, 1)
    y_r = rd.gauss(0, 1)
    if threeD:
        z_r = rd.gauss(0, 1)
    else:
        z_r=0
    uni = np.sqrt(np.square(x_r) + np.square(y_r) + np.square(z_r))

    x_r = (x_r * radius) / uni
    y_r = (y_r * radius) / uni
    z_r = (z_r * radius) / uni

    return x_r, y_r, z_r

def divide(p):        #takes rd point and places new cell

    xn,yn,zn=rdspot(p)
    xn = max((xn + c_ary[p].xcor),radius)
    yn = max((yn + c_ary[p].ycor),radius)
    if threeD:
        zn = max((zn + c_ary[p].zcor),radius)
    else:
        zn=2
    c_num=max(c_ary.keys())

    c_ary[c_num+1] = cl.cell(c_num+1, 'ecoli ', radius, stategamble(), xn, yn, zn)
    c_ary[p].radius = radius
    c_ary[p].status = True

def growth(p):

    c_ary[p].radius = c_ary[p].radius + g_rate

def event(step):                                #what happens to cell in time step#

    for elem in c_ary.keys():               #keys()cause new created cells do nothing

        if c_ary[elem].radius >= maxrad:    #cell_r big enough -> division#
            divide(elem)

        elif c_ary[elem].status:
            growth(elem)                    #if cell=on -> grows#

    cgrad = cl.c_grad(len(c_ary), x, n, place, C_on, K, feedback, c_ary, threeD)

    for i in range(ita):
        thres = move()
        if thres <= 0.1:
            break

    C_true = cgrad.calc_cval(step,C_t)                          #actual c of cells

    gridprint(step, C_true)

    C_i,state = cgrad.switch()
    switch_cary(state)

    state_t.append(list(state))
    C_t.append(list(C_i))

def switch_cary(state):                 #updates cell.status
    for elem in c_ary:
        c_ary[elem].status = state[elem]

def pic(a):                     #creats vtu data with cell situation at time step


    x_list = []
    y_list = []
    z_list = []
    r_list = []
    F_x = []
    F_y = []
    F_z = []



    vtk_writer = vtktools.VTK_XML_Serial_Unstructured()

    for elem in c_ary:
        x_list.append(c_ary[elem].xcor)
        y_list.append(c_ary[elem].ycor)
        z_list.append(c_ary[elem].zcor)
        r_list.append(c_ary[elem].radius)
        F_x.append(fx[elem])
        F_y.append(fy[elem])
        F_z.append(fz[elem])

    vtk_writer.snapshot("cell_arrangements"+str(a)+".vtu", x_list, y_list, z_list, radii=r_list, x_force=F_x, y_force=F_y,
                        z_force=F_z)
    vtk_writer.writePVD("cell_arrangements"+str(a)+".pvd")

def gridprint (z, C_true):

        picgrid=pres.gridpic(x,k,c_ary,threeD,pos,C_true)

        C = picgrid.calc_cval()

        # Variables
        point_data = np.zeros((nx + 1, ny + 1, nz + 1))
        # cell_data = np.zeros((nx, ny, nz))
        distribution = np.zeros((nx, ny, nz))
        for i in range(len(C)):
            x_dis = i % x+1
            z_dis = i // ((x+1)**2)
            y_dis = (i %((x+1) ** 2)) // x
            if ( max([x_dis,y_dis,z_dis]) <= 11 ):
                #print (i)
                point_data[x_dis][y_dis][z_dis]=C[i]
            else:
                print(i)

        hl.gridToVTK("c_grid"+str(z), x_c, y_c, z_c, cellData={"distribution": distribution}, pointData={"point_data": point_data})

def update(end):

    start = 0
    time = range(start, end)

    initialize()

    for step in time:
       event(step)
       pic(step)



#run program

update(20)
#print(state_t)
#print(C_t)