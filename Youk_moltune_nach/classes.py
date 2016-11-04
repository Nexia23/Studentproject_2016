
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