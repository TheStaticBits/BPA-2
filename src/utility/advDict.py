class AdvDict:
    """ Provides an interface with >, >=, -=, += for dictionaries """

    def __init__(self, dict):
        self.pyDict = dict
    

    def checkType(self, obj):
        if not isinstance(obj, AdvDict): raise TypeError


    def __isub__(self, other):
        """ -= overload """
        self.checkType(other)
        
        for key, value in other.pyDict.items():
            self.pyDict[key] -= value

        return self
    
    def __iadd__(self, other):
        """ += overload """
        self.checkType(other)
        
        for key, value in other.pyDict.items():
            self.pyDict[key] += value

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
        """ [] overload"""
        return self.pyDict[key]
    
    def __setitem__(self, key, value):
        """ [] = value  overload"""
        self.pyDict[key] = value
    
    def __contains__(self, item):
        """ in operator overload """
    
    def items(self):
        return self.pyDict.items()
    

    def getDict(self): return self.pyDict
