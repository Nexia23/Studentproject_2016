import numpy
import random as rd
import numpy as np
class cell:
    """
    @type name: str(which bacteria)
    @type radius: float
    @type molcomp: dict
    @type status: bool
    """

    def __init__(self, mid, name, radius, status, posi):
        self.mid = mid
        self.name = name
        self.radius = radius
        #self.molcomp = molcomp
        self.status = status
        self.posi = posi

    @property
    def mid(self):
        return self.__mid

    @mid.setter
    def mid(self, value):
        self.__mid = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("radius must be numeric")
        else:
            self.__radius = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self,value):
        self.__status = value

    @property
    def posi(self):
        return self.__posi

    @posi.setter
    def posi(self,value):
        self.__posi = value

    def __repr__(self):
        return self.name

#Parametersettings#

x=10                              #sets gridsize
n=0.3                             #set chance of cells n probability
place=0.5                         #set on_state cells n probability
C_on=13.0                         #signalconcentration of activ cel#
K =  18.0                         #threshold c#
feedback = 0                      #positiv(1) or negative(0) feedback#
min_cell=5                        #set minimum of cellneigbors for new cellcreation#


ce=0                              #for pos_dic entrykey
pos={}                            #dic for grid and cells in a list [0]=row [1]=col [2] if cell there or not
num=0

for row in range(x+1):
    for col in range(x+1):
        put=rd.random()
        if put<= n:
            num+=1
            loc = [row,col]
            pos[ce]= cell(ce,'ecoli '+str(num),2,True,loc)     #dict for cell positions#
            ce+=1
        else:
            pos[ce]=[row,col,False]
            ce+=1



r = np.zeros(len(pos))        #list of cellposition in space#
state=np.arange(len(pos))     #list of default state of each cell#
C_i = np.zeros(len(pos))      # concentration of each cell at time i #
C_print=np.zeros(len(pos))    #actual concentrations at position cells + neighbor#
resident=np.zeros(len(pos))   #spot has cell or not#
print(pos)



class Molecule:
    """

    @type name: str
    @type mass: float
    """

    def __init__(self, mid, name, mass=0):
        self.mid = mid
        self.name = name
        self.mass = mass

    @property
    def mid(self):
        return self.__mid

    @mid.setter
    def mid(self, value):
        self.__mid = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("mass must be numeric")
        else:
            self.__mass = value

    def __repr__(self): #string "self.name"		#print(list(object))
        return self.name