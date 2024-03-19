import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.140.124.28"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()



    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() #reply from server
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            # No need to immediately receive a reply here
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            return None
