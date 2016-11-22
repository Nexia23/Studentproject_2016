import numpy as np

class cell:
    """
    @type name: str(which bacteria)
    @type radius: float
    @type mid: int
    @type status: bool
    """

    def __init__(self, mid, name, radius, status, xcor, ycor, zcor):
        self.mid = mid
        self.name = name
        self.radius = radius
        #self.molcomp = molcomp
        self.status = status
        self.xcor = xcor
        self.ycor = ycor
        self.zcor = zcor

    @property
    def mid(self):
        return self.__mid

    @mid.setter
    def mid(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("radius must be numeric")
        else:
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
    def x_cor(self):
        return self.__x_cor

    @x_cor.setter
    def x_cor(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("coordinate must be numeric")
        else:
            self.__x_cor = value

    @property
    def y_cor(self):
        return self.__y_cor

    @y_cor.setter
    def y_cor(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("coordinate must be numeric")
        else:
            self.__y_cor = value

    @property
    def z_cor(self):
        return self.__z_cor

    @z_cor.setter
    def z_cor(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("coordinate must be numeric")
        else:
            self.__z_cor = value

    def __repr__(self):
        return self.name


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
"""""
    x =  sets gridsize
    n = set chance of cells n probability
    place  set on_state cells n probability
    C_on signalconcentration of activ cell
    K = threshold c#
    feedback = positiv(1) or negative(0) feedback
    #min_cell=5                             #set minimum of cellneigbors for new cellcreation#
    c_ary = c_ary
    gamma_ =  degradations constant#
    diff_const =  diffusions constant#

    lambda_ = float(np.sqrt(bruch))  radius of signalcloud of cell#

"""""
class c_grad:

    def __init__(self, c_num,x,n,place,C_on,K,feedback,c_ary):
        #Parametersettings#
        self.c_num = c_num
        self.x = x
        self.n = n
        self.place = place
        self.C_on = C_on
        self.K = K
        self.feedback = feedback
        self.c_ary = c_ary
        gamma_ = 7.0
        diff_const = 1.0
        bruch = float(diff_const / gamma_)
        lambda_ = float(np.sqrt(bruch))


        self.r = np.zeros(c_num)            #list of cellposition in space#
        self.state = np.zeros(c_num)        #list of default state of each cell#
        self.C_i = np.zeros(c_num)          #concentration of each cell at time i #
        self.C_print = np.zeros(c_num)      #actual concentrations at position cells + neighbor#

    @property
    def c_num(self):
        return self.__c_num

    @c_num.setter
    def c_num(self, value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise Exception("There must be cells")
        else:
            self.__c_num = value

    def calcDistances(self,c_num):

        for i in range(len(self.r)):
            self.r[i] = np.sqrt(np.square(self.c_ary[i].xcor - self.c_ary[c_num].xcor)
                           + np.square(self.c_ary[i].ycor - self.c_ary[c_num].ycor)
                           + np.square(self.c_ary[i].zcor - self.c_ary[c_num].zcor))
            # print(r[i])

        return self.r

    def calc_cval(self,step, i):
        c_neighbor = 0.0
        self.calcDistances(i)
        # print(r)

        for j in range(len(self.C_i)):  # nachbarzellen_c aufaddieren
            if j != i:
                c_neighbor = self.C_t[step][j] * np.exp(-self.r[j] / self.lambda_) + c_neighbor

        c_value = c_neighbor + self.C_t[step][i]

        self.C_i[i] = c_value
        self.C_print[i] = c_value



