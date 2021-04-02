import socket, threading
import json

FORMAT = 'utf-8'
HEADER = 1024

w = 300
h = 150


class Connection():
	def __init__(self, socket, username, canvas):
		import sach
		self.socket = socket
		if self.receive_msg()=='ok':
			self.main = sach.User('online')
			canvas.create_text(w/2,h/2, text='connected')
		else:
			canvas.create_text(w/2,h/2, text='Server full', font = 'Arial 20 bold')
		self.username = username
		self.canvas = canvas
		self.send_msg(self.username)
		self.rcv_coords = False
		threading.Thread(target = self.handle, daemon = True).start()



	def handle(self):
		msg = self.receive_msg()
		if msg == 'o1':
			self.main.order = 1
			self.canvas.create_text(50, 50,text = 'Si biely', font = 'Arial 15 bold')
			self.main.draw_entities()
		elif msg == 'o2':
			self.main.order = 2
			self.canvas.create_text(50, 50,text = 'Si čierny', font = 'Arial 15 bold')
			self.main.draw_entities()

		while True:
			msg = self.receive_msg()
			if msg=='1':
				self.send_msg('1')
			elif msg=='2c':
				self.opponent = self.receive_msg()
				self.main.draw_opponent()
				self.canvas.create_text(50,130,text= 'Opponent: {}'.format(self.opponent))
				self.send_msg('ok')
			elif msg=='2':
				self.main.o_moved = False
				self.main.o_turn = False
				self.send_msg('waiting')
				self.rcv_coords = False

			elif msg=='0':
				if not self.rcv_coords:
					coords = self.receive_msg()
					if coords !='[]':
						to_coords = json.loads(coords[coords.index('  '):])
						f_coords = json.loads(coords[:coords.index('  ')])
						if self.main.order == 1:
							for entities in self.main.entities:
								for entity in entities:
									#print(f'{entity.pozicia} = {f_coords}')
									if entity.pozicia == f_coords:
										entity.artificial_move(to_coords)
										break
						else:
							for entities in self.main.b_entities:
								for entity in entities:
									if entity.pozicia == f_coords:
										entity.artificial_move(to_coords)
										print('x')
										break

					self.rcv_coords = True
				if self.main.o_moved:
					print('moved')
					self.send_msg(f'moved')
					self.send_msg(f'{self.main.moving_from}  {self.main.moved_to}')
				else:
					self.main.o_turn = True
					self.send_msg('moving')  







	def send_msg(self, msg):					#essential for send and receive
			message = str(msg).encode(FORMAT)
			msg_len = len(message)
			message += b' '*(HEADER - msg_len)
			self.socket.send(message)


	def receive_msg(self):
		message = self.socket.recv(HEADER).decode(FORMAT).strip()
		return message