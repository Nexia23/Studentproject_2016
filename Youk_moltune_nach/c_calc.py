import matplotlib.pyplot as plt
import numpy as np
import math
import random as rd

#Variablen fuer Cgradient#

gamma_ = 1                   #degradations constant#
diff_const = 0.1             #diffusions constant#
bruch = diff_const/gamma_
lambda_ = math.sqrt(bruch)   #radius of signalcloud of cell#

#Parametersettings

x=10                         #sets gridsize
n=150                         #sets number of cells
pos={i: [rd.randint(0, x),rd.randint(0,x)] for i in range(n)} # dict for cell positions#

feedback = 1                 #positiv(1) or negative(0) feedback#

r = np.zeros(n)            #list of cellposition in space#
state=np.arange(n)          #list of default state of each cell#
C_i = np.zeros(n)          # concentration of each cell at time i #

C_on=5                      #signalconcentration of activ cel#
K =  1                      #threshold c#

#outputdata

C_t=[]                       # concentrations at time step#
state_t=[]        #lists all individual cellstates at timestep#

parameter = 'C_on = ' + str(C_on) \
            + ' K = ' + str(K) \
            + ' n = ' + str(n) \
            + ' gamma  = ' + str(gamma_) \
            + ' diffconst =' + str(diff_const) \
            + ' feedback = ' + str(feedback) \
            + ' x = ' + str(x)\
            +'.png'


def calcDistances(c_num):
    for i in range(len(r)):
        r[i] = math.sqrt((pos[i][0] - pos[c_num][0]) ** 2 + (pos[i][1] - pos[c_num][1]) ** 2)
        #print(r[i])

    return r



def calc_cval(step,i):
    c_neighbor = 0
    calcDistances(i)
    #print(r)
    for j in range(len(C_i)):                #nachbarzellen_c aufaddieren
        if j!=i:
            c_neighbor = C_t[step][j] * np.exp(-r[j] / lambda_) + c_neighbor

    c_value = c_neighbor + C_t[step][i]
    print('c_value :'+ str(c_neighbor))
    C_i[i]=c_value


def calc_expterm(i):
    f_n = 0
    calcDistances(i)
    for j in range(len(r)):          #calc the signal strengh f_n for cell i #
        if j != i:
            f_n = np.exp(-r[j]/lambda_)+f_n
    return f_n


def set_state():                    #function to  set concentration#

    if feedback==1:
        for j, val in enumerate(state):
            if val == 1:                #anyone with 1 is activ
                C_i[j]=C_on             #and concentration is set on c_on for active cell
            else:
                C_i[j]=1                #or inactive than set to 1

    elif feedback==0:
        for j, val in enumerate(state):
            if val == 0:  # anyone with 1 is activ
                C_i[j] = C_on  # and concentration is set on c_on for active cell
            else:
                C_i[j] = 1  # or inactive than set to 1




def neighbor(step,i):                    #function to sum the current activated neighboring cells #
    acti = 0

    for j, val in enumerate(state_t[step]):
        if val == 1 and j!=i :      #anyone else whos activ is counted
            acti += 1

    return acti


def switch (step,ci):             # determine cell cis status for next step.#

    f_n = calc_expterm(ci)
    acti=neighbor(step,ci)

    #print('Soviele active drum rum '+str(ci)+' '+str(acti))
    #print('f_n ='+str(f_n))

    A_0 = 1 + f_n - K
    A_n = C_on + (1-K) / f_n
    #+ (1 + (len(state) - acti) * f_n) / f_n  # activation  threshold

    D_0 = C_i[ci] - K + f_n
    D_n = C_on - K / (f_n + 1)
    # + (1 + (acti) * f_n) / (1 + f_n)  # deactivation threshold


    if feedback==1:           #positiv feedback

        #print('A_n ='+str(A_n))
        #print('D_n ='+str(D_n))
        #print('C_i =' + str(C_i[ci]))

        if C_i[ci]>= A_n and C_i[ci]<= A_0 :   #if true than active in next state cause of neighbor
            state[ci]=1
            C_i[ci]=C_on

        elif C_i[ci]>= D_n and C_i[ci]<=D_0:   # if < than deactive in next state
            state[ci]=0
            C_i[ci]=1

        elif C_i[ci] >= D_0 and C_i[ci]<=A_n:  # if inbetween bistable#
            if state[ci] == 0:
                state[ci]=0
                C_i[ci] = 1
            else:
                state[ci]=1
                C_i[ci]=C_on

    elif feedback == 0:  # negative feedback#

        print('A_n ='+str(A_n))
        print('D_n ='+str(D_n))
        print('C_i =' + str(C_i[ci]))

        if C_i[ci] >= A_n:  # if > than deactive in next state#
                state[ci] = 0
                C_i[ci] = 1

        elif C_i[ci] <= D_n:  # if < than active in next state#
            state[ci] = 1
            C_i[ci] = C_on


        elif C_i[ci] >= D_n and C_i[ci] <= A_n:  # if in between flipflop#

                if state[ci] == 0:
                    state[ci] = 1
                    C_i[ci] = C_on
                else:
                    state[ci] = 0
                    C_i[ci] = 1

def update(end):

    plt.style.use('ggplot')
    start=0
    stop = end
    time = np.linspace(start, stop, end*10)
    timer=0
    i = 0


    while i < n:
        state[i] = rd.randint(0, 1)  # produce random state
        i += 1
    stat_p=str(state)


    for step in time:

        set_state()

        if timer==0:                             #saves initial status of system
            C_t.append(list(C_i))
            state_t.append(list(state))


            fig = plt.figure()
            fig.suptitle('Cell position and state', fontsize=16)



            star=plt.subplot(3, 1, 1)
            star.set_title('Inital state')
            star.axis([-1, x + 1, -1, x + 1])         #plot of state/cell position


            for i in pos.keys():
                if state[i] == 1:                    #if on red dot
                    plt.plot(pos[i][0], pos[i][1], 'ro')
                else:                                #else(if off) blue dot
                    plt.plot(pos[i][0], pos[i][1], 'bo')


        for i in range(len(C_i)):                 #calc actual c for cell
            calc_cval(timer,i)
        print(C_i)
        for j in range(len(C_i)):                 #determine cells behaviour
            switch(timer,j)


        state_t.append(list(state))              #saves status
        C_t.append(list(C_i))                    #saves set c of cells

        timer += 1
        if timer*2==len(time):

            mid=plt.subplot(3, 1, 2)
            mid.set_title('Halftime state')
            mid.axis([-1, x + 1, -1, x + 1])               #plot of state/cell position
            for i in pos.keys():
                if state[i] == 1:                         #if on red dot
                    plt.plot(pos[i][0], pos[i][1], 'ro')
                else:                                    #else(if off) blue dot
                    plt.plot(pos[i][0], pos[i][1], 'bo')



        if timer == len(time)-1:

            det=plt.subplot(3, 1, 3)
            det.set_title('End state')
            det.axis([-1, x + 1, -1, x + 1])  # plot of state/cell position
            for i in pos.keys():
                if state[i] == 1:  # if on red dot
                    plt.plot(pos[i][0], pos[i][1], 'ro')
                else:  # else(if off) blue dot
                    plt.plot(pos[i][0], pos[i][1], 'bo')
            fig.savefig(parameter, dpi=600, format='png', bbox_inches='tight')


    print(C_t)
    print(state_t)


print(parameter)
update(10)
plt.show()