import socket
import threading, os
import time
import json

SERVER_ADRESS = ('192.168.100.41', 5050)
FORMAT = 'utf-8'
HEADER = 1024

players = {}

class Server():							#server start
	def __init__(self, inet, stream):
		self.inet = inet
		self.stream = stream
		self.server = socket.socket(self.inet, self.stream)
		self.server.bind(SERVER_ADRESS)
		self.clients = []
		self.players = 0
		threading.Thread(target = self.ex_input, daemon = True).start()	
		self.narade = 0


	def start(self):
		print('Awaiting user')
		self.server.listen()
		while True:
			client_socket, client_adress = self.server.accept()
			if self.players<2:
				send_ok(client_socket, 'ok')
				print(f'Client connected at {client_adress[0]}')
				self.clients.append(Client(client_socket, client_adress, self))
				threading.Thread(target = self.clients[-1].handle, daemon = True).start()
			else:
				client_socket.close()



	def close(self):
	    self.server.shutdown(socket.SHUT_RDWR)
	    self.server.close()
	    print ("closed")



	def ex_input(self):
		while True:
			try:
				if input()=='a':
					self.terminate()
					break
			except Exception as e:
				if e == EOFError:
					self.terminate()
					break
	

	def terminate(self):
		self.server.close()
		os._exit(0)

def send_ok(socket, msg):
	message = str(msg).encode(FORMAT)
	msg_len = len(message)
	message += b' '*(HEADER - msg_len)
	socket.send(message)








class Client():								#handles every client
	def __init__(self, socket, adress, server):
		self.socket = socket
		self.adress = adress
		self.server = server
		self.connected = True
		self.sendop = False
		self.moved = False
		self.opponent = None
		self.coords = []
		self.sent_coords = False


	def handle(self):
		self.username = self.receive_msg()
		self.server.players+=1
		if self.server.players == 1:
			self.send_msg('o1')
		elif self.server.players == 2:
			self.send_msg('o2')

		while self.connected:
			if not self.opponent and self.server.players==2:
				for c in self.server.clients:
					if c!=self:
						self.opponent = c

			if self.server.players==1:
				self.send_msg('1')
			elif not self.sendop:
				self.send_msg('2c')
				self.send_msg(self.opponent.username)
				self.sendop = True
			elif self.server.clients.index(self)==self.server.narade:
				self.send_msg('0')
				if not self.sent_coords:
					self.send_msg(self.coords)
					self.sent_coords = True
			elif self.server.clients.index(self)!=self.server.narade:
				self.sent_coords = False
				self.send_msg('2')




			msg = self.receive_msg()
			if msg=='1':
				pass
			elif msg == 'moving':
				pass
			elif msg == 'waiting':
				pass
			elif msg == 'ok':
				self.sendop = True
			elif msg == 'moved':
				self.opponent.coords = self.receive_msg()
				if self.server.narade == 0:
					self.server.narade = 1
				else:
					self.server.narade = 0
					self.moved = True

			#print(msg)

		


	def disconnect(self):
		self.socket.close()
		print('Client disconnected at',self.adress)
		self.server.clients.remove(self)
		self.server.players -= 1
		self.connected = False







	def send_msg(self, msg):					#essential for send and receive
		try:
			message = str(msg).encode(FORMAT)
			msg_len = len(message)
			message += b' '*(HEADER - msg_len)
			self.socket.send(message)
		except:
			self.disconnect()


	def receive_msg(self):
		try:
			message = self.socket.recv(HEADER).decode(FORMAT).strip()
			return message	
		except:
			self.disconnect()




if __name__=='__main__':
	s = Server(socket.AF_INET, socket.SOCK_STREAM).start()