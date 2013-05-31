import socket
from Tkinter import *
import threading
import json

class CentralChat:
    global room, nick

    room = "Home"
    nick = "Default"

    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack()
        self.server = "centralchat.zapto.org"
        self.port = 5124
        self.sock = socket.socket()
        threading.Thread(target=self.listen).start()
        self.user_input()
        self.gui()
        
    def gui(self):
        text = Frame(self.frame)
        self.text = Text(text, height=20, width=80, background='white')
        self.text.config(state=DISABLED)
        self.text.pack(side=LEFT)
        scroll = Scrollbar(text)
        scroll.pack(side=RIGHT, fill=Y)
        text.pack()

    def listen(self):
        global room
        self.sock.connect((self.server, self.port))
        while True:
            data = self.sock.recv(102400)
            if data:
                try:
                    data = json.loads(data)
                    if data['room'] == room and data['msg'] != '':
                        message = "{0}: {1}\n".format(data['nick'], data['msg'])
                        self.display(message)
                except Exception, error:
                    print error, data
            else:
                break
    def display(self, text):
        self.text.config(state=NORMAL)
        self.text.insert(END, text)
        self.text.config(state=DISABLED)

    def user_input(self):
        self.msg = Entry(self.root)
        self.msg.bind("<Return>", self.send)
        self.msg.pack(fill=X)
        b = Button(self.root, text="Send", command=self.send)
        b.pack(fill=X)

    def send(self, event=None):
        global nick, room
        check = self.msg.get()
        if check.startswith("/nick"):
            check = check.split()
            nick_ = ''.join(check[1:])
            msg=nick+" Changed his name to "+nick_
            nick = nick_
        elif check.startswith("/room"):
            check = check.split()
            room_ = ''.join(check[1:])
            msg=nick+" joined "+room_
            room = room_
        else:
            msg = check
        msg = json.dumps({"msg":msg, "nick":nick, "room":room})
        self.sock.send(msg)
        self.msg.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    CentralChat(root=root)
    root.title("Central Chat")
    root.mainloop()
