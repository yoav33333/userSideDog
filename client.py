# client.py
import json
import socket
class Client:
    host = "10.10.0.41"
    port = 65432


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print("Connected to server.")
            print(client_socket.recv(1024).decode())
            while True:
                try:
                    message = input("Enter message (or 'quit' to exit): ")
                    if message.lower() == 'quit':
                        break
                    client_socket.sendall(message.encode())
                    data = client_socket.recv(1024)
                    print("Echo from server:", data.decode())
                    global vars_dict
                    vars_dict = json.loads(data.decode())
                except:
                    print("An error occurred. Exiting.")


