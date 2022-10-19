
class Vect:
    """ Stores two digits """

    def __init__(self, list):
        """ Init from list/tuple """
        self.x = list[0]
        self.y = list[1]
    

    def __init__(self, x, y):
        """ Init from given x & y"""
        self.x = x
        self.y = y

    
    def getTuple(self): return (x, y)


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
        return Vect(abs(x), abs(y))