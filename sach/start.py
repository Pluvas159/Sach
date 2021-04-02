import tkinter
from time import sleep
import threading

w = 300
h = 150

canvas = tkinter.Canvas(width = w, height = h)
canvas.pack()

ip_ = ('178.143.5.230', 5050)



def start_off():
	import sach as sach
	username = ent.get()
	main = sach.User('offline')
	main.draw_entities()
	#main.username = username



def start_on():
	username = ent.get()
	if username!='':
		ips = (ip.get(), 5050)
		if ips!='':
			import socket
			client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			while True:
				try:
					client.connect(ip_)
					break
				except Exception as e:
					canvas.create_text(w/2,h/2, text='server offline')
					canvas.update()
					

			import connection as c
			c.Connection(client, username, canvas)
			canvas.update()




ent = tkinter.Entry() 
ent.pack(side = tkinter.LEFT)

btf = tkinter.Button(text = 'offline', command = start_off)
btf.pack(side = tkinter.LEFT)

bto = tkinter.Button(text = 'online', command = start_on)
bto.pack(side = tkinter.LEFT)

ip = tkinter.Entry()
ip.place(x= w/2, y = 130)
ip.insert(0, ip_[0])

canvas.create_text(w/2-15, 138, text = 'IP:')

canvas.create_text(30,145, text = 'Username: ')


canvas.mainloop()
