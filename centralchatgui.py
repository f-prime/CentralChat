import socket
from Tkinter import *
import threading
import json

class CentralChat:
    
    def __init__(self, root, nick="Test", room='t'):
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack()
        self.server = ""
        self.port = 5124
        self.sock = socket.socket()
        self.nick = nick
        self.room = room
        threading.Thread(target=self.listen).start()
        self.user_input()
        self.gui()
    
    def gui(self):
        text = Frame(self.frame)
        self.text = Text(text, height=20, width=50, background='white')
        self.text.config(state=DISABLED)
        self.text.pack(side=LEFT)
        scroll = Scrollbar(text)
        scroll.pack(side=RIGHT, fill=Y)
        text.pack()

    def listen(self):
        self.sock.connect((self.server, self.port))
        while True:
            data = self.sock.recv(102400)
            if data:
                try:
                    data = json.loads(data)
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
        self.msg.pack(fill=X)
        b = Button(self.root, text="Send", command=self.send)
        b.pack(fill=X)

    def send(self):
        msg = self.msg.get()
        msg = json.dumps({"msg":msg, "nick":self.nick, "room":self.room})
        self.sock.send(msg)
        self.msg.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    CentralChat(root=root)
    root.title("Central Chat")
    root.mainloop()
