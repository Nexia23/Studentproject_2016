import matplotlib.pyplot as plt
import numpy as np
import math


#Variablen fuer Cgradient#

gamma_ = 1                   #degradations constant#
diff_const = 0.2             #diffusions constant#
bruch = diff_const/gamma_
lambda_ = math.sqrt(bruch)   #radius of signalcloud of cell#

#Parametersettings

feedback = 1                 #positiv(1) or negative(0) feedback#

r = [0.1,0.1,0.1]            #list of cellposition in space#
state=[1,1,1]                #list of default state of each cell#
C_i = np.arange(len(r))      # concentration of each cell at time i #


C_on=10                      #signalconcentration of activ cel#
K =  2                      #threshold c#

#outputdata

C_t=[]                       # concentrations at time step#
state_t=[list(state)]        #lists all individual cellstates in one entry#



def calc_cval(step,i):
    c_neighbor = 0
    for j in range(len(C_i)):                #nachbarzellen_c aufaddieren
        if j!=i:
            c_neighbor = C_t[step][j] * np.exp(-r[j] / lambda_) + c_neighbor

    c_value = c_neighbor + C_t[step][i]
    #print('c_value :'+ str(c_value))
    C_i[i]=c_value


def calc_expterm(i):
    f_n = 0

    for j in range(len(r)):          #calc the signal strengh f_n for cell i #
        if j != i:
            f_n = np.exp(-r[j]/lambda_)+f_n
    return f_n

def set_state():                    #function to  set concentration#

    #print(state)
    for j, val in enumerate(state):
        if val == 1:                #anyone with 1 is activ
            C_i[j]=C_on             #and concentration is set on c_on for active cell
        else:
            C_i[j]=1                #or inactive than set to 1




def neighbor(step,i):                    #function to sum the current activated neighboring cells #
    acti = 0

    for j, val in enumerate(state_t[step]):
        if val == 1 and j!=i :      #anyone else whos activ is counted
            acti += 1

    return acti


def switch (step,ci):             # determine cell ci´s status for next step.#

    f_n = calc_expterm(ci)
    acti=neighbor(step,ci)
    f_n=0.2
    #print('Soviele active drum rum '+str(ci)+' '+str(acti))
    #print('f_n ='+str(f_n))

    # A_0 = 1 + f_n - K
    A_n = C_i[ci] - K / f_n + (1 + (len(state) - acti) * f_n) / f_n  # activation  threshold
    # D_0 = C_i[ci] - K + f_n
    D_n = C_i[ci] - K / (f_n + 1) + (1 + (acti) * f_n) / (1 + f_n)  # deactivation threshold


    if feedback==1:           #positiv feedback

        print('A_n ='+str(A_n))
        print('D_n ='+str(D_n))

        if C_i[ci]>= A_n:   #if > than active in next state
            state[ci]=1
            C_i[ci]=C_on

        if C_i[ci]<= D_n:   # if < than deactive in next state
            state[ci]=0
            C_i[ci]=1

        if C_i[ci] >= D_n and C_i[ci]<=A_n:  # if inbetween bistable#
            if state[ci] == 0:
                state[ci]=0
                C_i[ci] = 1
            else:
                state[ci]=1
                C_i[ci]=C_on

    if feedback == 0:  # negativ feedback#

        print('A_n ='+str(A_n))
        print('D_n ='+str(D_n))

        if C_i[ci] >= A_n:  # if > than deactive in next state#
                state[ci] = 0
                C_i[ci] = 1

        if C_i[ci] <= D_n:  # if < than active in next state#
            state[ci] = 1
            C_i[ci] = C_on

        if C_i[ci] >= D_n and C_i[ci] <= A_n:  # if inbetween flipflop#
            if state[ci] == 0:
                state[ci] = 1
                C_i[ci] = C_on
            else:
                state[ci] = 0
                C_i[ci] = 1

def update(end):
    start=0
    stop = end
    time = np.linspace(start, stop, 10)

    timer=0

    for step in time:

        set_state()

        if timer==0:
            C_t.append(list(C_i))

        for i in range(len(C_i)):
            calc_cval(timer,i)

        for j in range(len(C_i)):
            switch(timer,j)

        timer+=1
        state_t.append(list(state))
        C_t.append(list(C_i))

    print(C_t)
    print(state_t)

update(100)