
from re import X


class Vect:
    """ Stores two digits """

    def __init__(self, *args):
        """ Init from either given x and y or a single list/tuple """
        if len(args) == 2: # Init from x and y
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1: # Init from list/tuple or one digit
            if isinstance(args[0], int) or isinstance(args[0], float):
                self.x = args[0]
                self.y = args[0]
            elif isinstance(args[0], Vect):
                self.x = args[0].x
                self.y = args[0].y
            else: # list/tuple
                self.x = args[0][0]
                self.y = args[0][1]
    
    def getTuple(self): 
        return (self.x, self.y)
    
    def abs(self): 
        return Vect(abs(self.x), abs(self.y))
    
    def copy(self):
        return Vect(self.x, self.y)
    
    def __str__(self): 
        return f"({self.x}, {self.y})"

    """ Operator overloading for ease of use """
    
    def __add__(self, other):
        """ Addition between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x + other, self.y + other)
        else: raise TypeError
        
    def __iadd__(self, other):
        """ += for other Vect or other int """
        if isinstance(other, Vect):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
        else: raise TypeError
        return self
    

    def __sub__(self, other):
        """ Subtraction between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x - other.x, self.y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x - other, self.y - other)
        else: raise TypeError

    def __isub__(self, other):
        """ -= for other Vect or other int """
        if isinstance(other, Vect):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
        else: raise TypeError
        return self


    def __mul__(self, other):
        """ Subtraction between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x * other, self.y * other)
        else: raise TypeError
    
    def __imul__(self, other):
        """ *= for other Vect or other int """
        if isinstance(other, Vect):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
        else: raise TypeError
        return self
    

    def __truediv__(self, other):
        """ Division between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x / other, self.y / other)
        else: raise TypeError
    
    def __itruediv__(self, other):
        """ /= for other Vect or other int """
        if isinstance(other, Vect):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
        else: raise TypeError
        return self
    
    def __floordiv__(self, other):
        """ FLOOR Division between Vect and Vect or Vect and int """
        if isinstance(other, Vect):
            return Vect(self.x // other.x, self.y // other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x // other, self.y // other)
        else: raise TypeError

    def __ifloordiv__(self, other):
        """ //= for other Vect or other int """
        if isinstance(other, Vect):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x //= other
            self.y //= other
        else: raise TypeError
        return self
    

    def __eq__(self, other):
        """ == overloading """
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        """ != overloading """
        return self.x != other.x or self.y != other.y
    
    def __ge__(self, other):
        """ >= overloading """
        return self.x >= other.x and self.y >= other.y
    def __gt__(self, other):
        """ > overloading """
        return self.x > other.x and self.y > other.y
    
    def __le__(self, other):
        """ <= overloading """
        return self.x <= other.x and self.y <= other.y
    def __lt__(self, other):
        """ < overloading """
        return self.x < other.x and self.y < other.y