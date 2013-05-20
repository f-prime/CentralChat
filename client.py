import socket
import json
import threading
import random

class CentralClient:
    def __init__(self, room, nick):
        self.ip = "centralchat.zapto.org"
        self.port = 5124
        self.nick = nick
        self.sock = socket.socket()
        self.room = room
        self.id = str(random.random())

    def main(self):
        self.sock.connect((self.ip, self.port))
        threading.Thread(target=self.listen).start()
        while True:
            msg = raw_input(self.nick+": ")
            msg = json.dumps({"id":self.id,"nick":self.nick, "room":self.room, "msg":msg})
            self.sock.send(msg)

    def listen(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                try:
                    data = json.loads(data)
                except:
                    continue
                if data['room'] == self.room and data['id'] != self.id:
                    print data['nick']+": "+data['msg']
if __name__ == "__main__":
    nick = raw_input("Nick: ")
    room = raw_input("Room: ")
    CentralClient(room, nick).main()
