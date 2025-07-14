from util.singelton import SingletonMeta



class run_globals(metaclass=SingletonMeta):
    run = True
    def stop(self):
        self.run = False
        print("Globals stopped")
    def isRunning(self):
        return self.run
class var_dict(metaclass=SingletonMeta):
    run = True
    vars_dict = {}
    old_vars_dict = {}
    def getGlobals(self):
        return self.vars_dict
    def setGlobals(self, new_dict):
        self.vars_dict = new_dict
    def getOldGlobals(self):
        return self.old_vars_dict
    def setOldGlobals(self, new_dict):
        # for key, value in new_dict.items():
        # self.vars_dict = new_dict.copy()
        self.old_vars_dict = new_dict.copy()
        # self.old_vars_dict = new_dict
        # self.vars_dict = new_dict
    def getChangedGlobals(self):
        changed = {}
        for key, value in self.vars_dict.items():
            if key not in self.old_vars_dict or self.old_vars_dict[key] != value:
                for sub_key, sub_value in value.items():
                    if key not in changed:
                        changed[key] = {}
                    if sub_key not in self.old_vars_dict.get(key, {}) or self.old_vars_dict[key][sub_key] != sub_value:
                        changed[key][sub_key] = sub_value
        print(changed)
        return changed
