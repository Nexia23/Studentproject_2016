import matplotlib.pyplot as plt
import numpy as np
import math

#Variablen fuer Cgradient#

gamma_ = 4                  #degradations constant#
print (gamma_)
diff_const = 1              #diffusions constant#
bruch = diff_const/gamma_
lambda_ = math.sqrt(bruch)  #radius of signalcloud of cell#

feedback = 1                #positiv(1) or negative(0) feedback#

r = [0,0.23,0.1]            #list of cellposition in space#

C_i = [1, 2, 9]               #momentary concentration of each cell#
state=[1,0,1]              #list of default state#

#Parameter
C_on=1                      #if on it has that concentration#
K = 17                      #threshold c#


print (lambda_)

def calc_cval(i):
    c_neighbor = 0
    for j in range(len(C_i)):                #nachbarzellen_c aufaddieren
        if j!=i:
            c_neighbor = C_i[j] * np.exp(-r[j] / lambda_) + c_neighbor

    c_value = c_neighbor + C_i[i]
    print(c_value)
    C_i[i]=c_value

def calc_expterm(i):
    f_n = 0

    for j in range(len(r)):          #calc the signal strengh f_n for cell ci #
        if j != i:
            f_n = np.exp(-r[j]/lambda_)+f_n
    return f_n

def get_state():                    #function to sum the current activated  cells#
    acti = 0
    for j, val in enumerate(state):
        if val == 1:
            acti += 1
    return acti

def switch (ci,acti):             # determine cell status for next step. acti value of active cells#
    print (ci)
    f_n = calc_expterm(ci)


    if feedback==1:

        A_0 = 1 + f_n - K
        A_n = C_i[ci] - K / f_n + (1 + (len(state) - acti) * f_n) / f_n
        D_0 = C_i[ci] - K + f_n
        D_n = C_i[ci] - K / (f_n + 1) + (1 + (acti) * f_n) / (1 + f_n)

        print('A_n ='+str(A_n))
        print('D_n ='+str(D_n))

        if C_i[ci]>= A_n:
            state[ci]=1
            C_i[ci]=C_on
            print('hier')

        if C_i[ci]<= D_n:
            state[ci]=0
            C_i[ci]=1
            print('nicht')




start=0
end= 10
time = np.linspace(start, end, 2)

for step in time:

    current = get_state()
    print(state)
    for i in range(len(C_i)):
        calc_cval(i)

    for j in range(len(C_i)):
        switch(j, current)



