from util.singelton import SingletonMeta


class var_dict(metaclass=SingletonMeta):
    vars_dict = {}
    def getGlobals(self):
        return self.vars_dict
    def setGlobals(self, new_dict):
        self.vars_dict = new_dict
