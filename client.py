# client.py
import json
import socket
import threading
import time

from globals import var_dict, run_globals
from util.singelton import SingletonMeta


class Client(metaclass=SingletonMeta):
    host = "10.10.0.41"
    port = 65432
    pocket_size = 1024
    update_server = False
    reset_flag = False
    def getDataFromServer(self, client_socket):
        while run_globals().isRunning() and not self.reset_flag:
            time.sleep(5)
            try:
                data = client_socket.recv(self.pocket_size)
                print("Echo from server:", data.decode())
                var_dict().setOldGlobals(json.loads(data.decode()))
                var_dict().setGlobals(json.loads(data.decode()))
            except socket.error as e:
                print(f"Socket error: {e}")
                self.reset_flag = True

    def giveUpdatedDataToServer(self, client_socket):
        while run_globals().isRunning() and not self.reset_flag:
            # time.sleep(1.5)
            try:
                # print(self.update_server)
                if self.update_server:
                    print(var_dict().getChangedGlobals())
                    print(var_dict().getChangedGlobals())
                    print(var_dict().getChangedGlobals())
                    print(var_dict().getChangedGlobals())
                    print(var_dict().getChangedGlobals())
                    print(var_dict().getChangedGlobals())
                    print(var_dict().getChangedGlobals())
                    client_socket.sendall(json.dumps(var_dict().getChangedGlobals()).encode())
                    self.update_server = False
            except socket.error as e:
                print(f"Socket error: {e}")
                self.reset_flag = True


    def run(self):
        while run_globals().isRunning():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.host, self.port))
                    self.reset_flag = False
                    print("Connected to server.")
                    # self.getDataFromServer(client_socket)
                    threading.Thread(target = lambda:self.getDataFromServer(client_socket),daemon=True).start()
                    threading.Thread(target = lambda:self.giveUpdatedDataToServer(client_socket),daemon=True).start()
                    while run_globals().isRunning() and not self.reset_flag:
                        pass

                    #     try:
                    #         print(var_dict().getChangedGlobals())
                    #     except:
                    #         print("An error occurred. Exiting.")
                    #         self.run()
            except Exception as e:
                print(f"Error connecting to server: {e}")
    def updateServer(self):
        print(json.dumps(var_dict().getChangedGlobals()))
        print(json.dumps(var_dict().getGlobals()))
        print(json.dumps(var_dict().getOldGlobals()))
        self.update_server = True
        print(self.update_server)


