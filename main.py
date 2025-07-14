import json
import threading

from client import Client
import globals
from globals import var_dict
from gui.gui_main import VarEditorServer

if __name__ == "__main__":
    # print(json.loads('{"Dog": {"name": "Dog", "age": 0}}'))
    # print(json.loads('{"Dog": {"name": "Dog", "age": 0}}'))
    # print(json.loads('{"Dog": {"name": "Dog", "age": 0}}')["Dog"])
    # print(json.loads('{"Dog": {"name": "Dog", "age": 0}}')["Dog"]["name"])
    # var_dict().setGlobals(json.loads('{"Dog": {"name": "Dog", "age": 0.0},"Cat": {"name": "Dog", "age": 0}}'))
    threading.Thread(target=lambda :Client().run(),daemon=True).start()
    VarEditorServer("10.10.0.41",80).run()
    print("hello")
    while globals.run_globals().isRunning():
        pass
        # print(globals.var_dict().getOldGlobals())
        # print(globals.var_dict().getGlobals())

