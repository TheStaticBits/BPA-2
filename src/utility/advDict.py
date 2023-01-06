class AdvDict:
    """ Provides an interface with >, >=, -=, += for dictionaries """

    def __init__(self, dict):
        self.pyDict = dict
    

    def checkType(self, obj):
        if not isinstance(obj, AdvDict): raise TypeError


    def __isub__(self, other):
        """ -= overload, subtracts the values of the other dictionary"""
        self.checkType(other)
        
        for key, value in other.pyDict.items():
            self.pyDict[key] -= value

        return self
    
    def __iadd__(self, other):
        """ += overloading, adds the values of the other dictionary """
        self.checkType(other)
        
        for key, value in other.pyDict.items():
            self.pyDict[key] += value

        return self
    
    def __imul__(self, other):
        """ *= overloading, allows for int/float or another dictionary """
        if isinstance(other, int) or isinstance(other, float):
            for key in self.pyDict.keys():
                self.pyDict[key] *= other
        
        else:
            for key, value in other.pyDict.items():
                self.pyDict[key] *= value
        
        return self


    def __gt__(self, other):
        """ > overload """
        self.checkType(other)
        
        for key, value in other.pyDict.items():
            if self.pyDict[key] <= value:
                return False
        
        return True
    
    def __ge__(self, other):
        """ >= overload """
        self.checkType(other)
        
        for key, value in other.pyDict.items():
            if self.pyDict[key] < value:
                return False
        
        return True
    

    def __getitem__(self, key):
        """ [] overload """
        return self.pyDict[key]
    
    def __setitem__(self, key, value):
        """ [] = value  overload """
        self.pyDict[key] = value
    
    def __contains__(self, item):
        """ in operator overload """
    

    def items(self):
        return self.pyDict.items()
        
    def keys(self):
        return self.pyDict.keys()
    
    
    def int(self):
        """ Casts all values in the dictionary to int """
        for key in self.pyDict.keys():
            self.pyDict[key] = int(self.pyDict[key])
    

    def getDict(self): return self.pyDict
    def copy(self): return AdvDict(self.pyDict.copy())