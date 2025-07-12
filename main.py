import json

from client import Client
import globals
from globals import var_dict
from gui.gui_main import VarEditorServer

if __name__ == "__main__":
    print(json.loads('{"Dog": {"name": "Dog", "age": 0}}'))
    print(json.loads('{"Dog": {"name": "Dog", "age": 0}}'))
    print(json.loads('{"Dog": {"name": "Dog", "age": 0}}')["Dog"])
    print(json.loads('{"Dog": {"name": "Dog", "age": 0}}')["Dog"]["name"])
    var_dict().setGlobals(json.loads('{"Dog": {"name": "Dog", "age": 0.0},"Cat": {"name": "Dog", "age": 0}}'))
    VarEditorServer(var_dict().getGlobals(),"10.10.0.41",80).run()
    print("hello")
    while True:
        print(var_dict().getGlobals())
        try:
            var_dict().getGlobals()["Dog"]["age"]+= 1
        except KeyError:
            pass
        pass
    # Client().run()