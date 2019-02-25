import socket
import ast

class Utility():
    def __init__(self):
        self.address = ''
        self.socket = ''
        self.user  = ''

    def sendTokenToServer(self,token,email):
        #This method is where you format on how you want
        #to send your stripe token to your server.
        msg = ast.literal_eval(
         '{"function": "client_token", "token":"' + token + '", "email":"' + email + '"}')
        rsp = self.connectToServer(self.host, self.port, msg)
        if rsp['rsp'] == 'Created new user succesfully.':
            return True
        else:
            return False

    def connectToServer(self,msg):
        s = None
        addrinfo = socket.getaddrinfo(self.address, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for res in addrinfo:
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as message:
                s = None
                continue
            try:
                s.connect(sa)
            except socket.error as message:
                s.close()
                s = None
                continue
            break

        rsp = ''
        s.send(msg)
        while True:
            data = s.recv(1024)
            if not data:
                s.close()
                break
            rsp += data

        return rsp
