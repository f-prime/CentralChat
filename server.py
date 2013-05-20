import socket
import threading

class CentralServer:
    def __init__(self):
        self.nodes = []
        self.sock = socket.socket()
    def main(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", 5124)
        self.sock.listen(5)
        while True:
            obj, conn = self.sock.accept()
            self.nodes.append(obj)
            threading.Thread(target=self.handle, args=(obj,)).start()
    
    def handle(self, obj):
        while True:
            data = obj.recv(1024)
            if not data:
                self.nodes.remove(obj)
                break
            else:
                for x in self.nodes:
                    x.send(data)
if __name__ == "__main__":
    CentralServer().main()
