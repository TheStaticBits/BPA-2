
from re import X


class Vect:
    """ Stores two digits """

    def __init__(self, *args):
        """ Init from either given x and y or a single list/tuple """
        if len(args) == 2: # Init from x and y
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1: # Init from list/tuple
            self.x = args[0][0]
            self.y = args[0][1]
    
    def getTuple(self): 
        return (self.x, self.y)


    """ Operator overloading for ease of use """
    
    def __add__(self, other):
        """ Addition between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Vect(self.x + other, self.y + other)
        
    def __iadd__(self, other):
        """ += for other Vect or other int """
        if isinstance(other, Vect):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int):
            self.x += other
            self.y += other
    

    def __sub__(self, other):
        """ Subtraction between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Vect(self.x - other, self.y - other)

    def __isub__(self, other):
        """ -= for other Vect or other int """
        if isinstance(other, Vect):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int):
            self.x -= other
            self.y -= other


    def __mul__(self, other):
        """ Subtraction between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Vect(self.x * other, self.y * other)
    
    def __imul__(self, other):
        """ *= for other Vect or other int """
        if isinstance(other, Vect):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int):
            self.x *= other
            self.y *= other
    

    def __truediv__(self, other):
        """ Division between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x / other.x, self.y / other.y)
        elif isinstance(other, int):
            return Vect(self.x / other, self.y / other)
    
    def __itruediv__(self, other):
        """ /= for other Vect or other int """
        if isinstance(other, Vect):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, int):
            self.x /= other
            self.y /= other
    
    def __floordiv__(self, other):
        """ FLOOR Division between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x // other.x, self.y // other.y)
        elif isinstance(other, int):
            return Vect(self.x // other, self.y // other)

    def __ifloordiv__(self, other):
        """ //= for other Vect or other int """
        if isinstance(other, Vect):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, int):
            self.x //= other
            self.y //= other
    

    def abs(self):
        return Vect(abs(self.x), abs(self.y))