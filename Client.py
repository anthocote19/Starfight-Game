import socket
import pickle

MyIP = socket.gethostbyname(socket.gethostname())


class Network:
    def __init__(self, ip=""):
        if ip:
            self.serverip = ip
        else:
            self.serverip = MyIP
        self.port = 12345
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.speedclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.speedclient.bind((MyIP, self.port))
        self.id = self.connect()

    def connect(self):

        try:
            self.client.connect((self.serverip, self.port))
            return pickle.loads(self.client.recv(4096))
        except:
            return

    def send(self, info):
        try:
            self.client.send(pickle.dumps(info))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)

    def send_sol(self, info):
        try:
            self.client.send(pickle.dumps(info))
        except socket.error as e:
            print(e)

    def recv_sol(self):
        return pickle.loads(self.client.recv(2048))

    def speedsend(self, info):
        self.speedclient.sendto(pickle.dumps(info), (self.serverip, self.port))
        data = self.speedclient.recvfrom(2048)[0]
        data = pickle.loads(data)
        # print(data)
        return data
