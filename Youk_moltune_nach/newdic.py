import matplotlib.pyplot as plt
import numpy as np
import math

import random as rd

#Variablen fuer Cgradient#

gamma_ = 7.0                  #degradations constant#
diff_const = 1.0              #diffusions constant#
bruch = float(diff_const/gamma_)
lambda_ = float(math.sqrt(bruch))   #radius of signalcloud of cell#

#Parametersettings#

x=10                           #sets gridsize
n=0.5                          #set chance of cells n probability
ch=0.5                         #set on_state cells n probability
pos={}
ce=0

for row in range(x):
    for col in range(x):

        put=rd.random()
        if put<= n:
            pos[(row,col)]=[True]     #dict for cell positions#
            ce+=1
        else:
            pos[(row, col)] = [False]


feedback = 0                  #positiv(1) or negative(0) feedback#

r = np.zeros(len(pos))        #list of cellposition in space#
state=np.arange(len(pos))     #list of default state of each cell#
C_i = np.zeros(len(pos))      # concentration of each cell at time i #
C_print=np.zeros(len(pos))

C_on=13.0                      #signalconcentration of activ cel#
K =  15.0                      #threshold c#

#outputdata#

C_t=[]                        # concentrations at time step#
state_t=[]                    #lists all individual cellstates at timestep#

parameter = 'C_on = ' + str(C_on) \
            + ' K = ' + str(K) \
            + ' n = ' + str(n) \
            + ' gamma  = ' + str(gamma_) \
            + ' diffconst =' + str(diff_const) \
            + ' feedback = ' + str(feedback) \
            + ' on_per_c = '+ str(ch)\
            + ' x = ' + str(x)\
            +'.pdf'

fig = plt.figure()
fig.suptitle('Cell position and state', fontsize=16)


def calcDistances(c_num):

    for i in range(len(r)):
        r[i] = math.sqrt((pos[i][0] - pos[c_num][0]) ** 2 + (pos[i][1] - pos[c_num][1]) ** 2)
        #print(r[i])

    return r
