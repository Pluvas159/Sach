import tkinter
from PIL import Image, ImageTk


h = 800
w = 800
orange = '#ff6633'
class Sach(tkinter.Frame):
    def __init__(self):
        master = tkinter.Tk()
        super().__init__(master)
        self.canvas = tkinter.Canvas(master, width = 800, height = 800)
        self.canvas.pack()
        self.draw_board()
        self.draw_entities()

        self.canvas.bind('<Button-1>', self.OnClick)
        self.canvas.bind('<Motion>', mouse.motion)

        self.moving = False
        self.turn = 0




    def draw_board(self):
        self.squares = []
        farba = '#ff6633'
        for i in range(8):
            for j in range(8):
                self.squares.append(Square(self.canvas.create_rectangle(0+(w/8)*j, 0+(h/8)*i, 100+(w/8)*j, 100+(h/8)*i, fill = farba), self.canvas, j+1, i+1, farba))
                if farba=='#ff6633':
                    farba = '#c4c4c4'
                else:
                    farba = '#ff6633'
            if farba=='#ff6633':
                    farba = '#c4c4c4'
            else:
                    farba = '#ff6633'


    def draw_entities(self):
        self.pesiaky()
        self.veze()
        self.kone()
        self.bishops()
        self.king()
        self.queen()

        self.entities = [self.pesiaky, self.veze, self.kone, self.bishops, self.queens, self.kings]
        self.b_entities = [self.b_pesiaky, self.b_veze, self.b_kone, self.b_bishops, self.b_queens, self.b_kings]


                  
    def pesiaky(self):
        self.pesiaky = []
        self.b_pesiaky = []
        for i in range(8):
            self.pesiaky.append(Pesiak(50+(w/8)*i,(h/8+50), self))
            self.b_pesiaky.append(b_pesiak(50+(w/8)*i,(h/8*6+50), self))



    def veze(self):
        self.veze = []
       	self.b_veze = []
        for i in range(2):
        	self.veze.append(Veza(50+700*i,50,self))
        	self.b_veze.append(b_veza(50+700*i,(h/8*7+50),self))

    def kone(self):
    	self.kone = []
    	self.b_kone = []
    	for i in range(2):
    		self.kone.append(Kon(150+500*i,50,self))
    		self.b_kone.append(b_kon(150+500*i,(h/8*7+50),self))

    def bishops(self):
    	self.bishops = []
    	self.b_bishops = []
    	for i in range(2):
    		self.bishops.append(Bishop(250+300*i,50,self))
    		self.b_bishops.append(b_bishop(250+300*i,(h/8*7+50),self))

    def king(self):
    	self.kings = []
    	self.b_kings = []
    	self.kings.append(King(450, 50, self))
    	self.b_kings.append(b_king(450, (h/8*7+50), self))

    def queen(self):
    	self.queens = []
    	self.b_queens = []
    	self.queens.append(Queen(350,50, self))
    	self.b_queens.append(b_queen(350,(h/8*7+50), self))



    def OnClick(self, event):
	    mouse.click = True
	    x = event.x
	    y = event.y
	    pozicia = [int(x//100+1), int(y//100+1)]
	    a = False
	    if self.turn%2==0:
		    for entities in self.entities:
		    	for entity in entities:
		    		if entity.pozicia == pozicia:
		    			if not self.moving:
		    				entity.move()
		    			break
	    else:
		    for entities in self.b_entities:
		    	for entity in entities:
		    		if entity.pozicia == pozicia:
		    			if not self.moving:
		    				entity.move()
		    			break



        
        

class User(Sach):
    def __init__(self):
        super().__init__()


class Square():
	def __init__(self, objekt, canvas, a, b, color):
		self.objekt = objekt
		self.canvas = canvas
		self.pozicia = [a,b]
		self.defaultcolor = color
		self.occupied = False
		self.b_occupied = False

	def change_color(self, color):
		self.canvas.itemconfig(self.objekt, fill=color)



        
    
        

class Pesiak():
    def __init__(self, x, y, board):
        self.image = ImageTk.PhotoImage(Image.open('pesiak.png'))
        self.objekt = board.canvas.create_image(x,y, image= self.image)
        self.pozicia = [int(x//100+1), int(y//100+1)]
        for square in board.squares:
        	if square.pozicia==self.pozicia:
        		square.occupied = True
        		self.sqr = square
        		break
        self.x = x
        self.y = y
        self.canvas = board.canvas
        self.board = board
        self.moving = False
        self.color = 'black'
        self.type = 'pesiak'

    def redraw(self):
        self.canvas.delete(self.objekt)
        self.objekt = self.canvas.create_image(self.x,self.y, image= self.image)
        self.canvas.update()


    def move(self):
        mouse.click=False
        for square in self.board.squares:
        	if square.pozicia==self.pozicia:
        		square.change_color('red')
        		break

       	self.available()
       	self.moving = True
       	self.board.moving = True
        while self.moving:
            #for squre in self.board.squares:
            #	if squre.occupied:
            #		squre.change_color('black')
            #	elif squre.b_occupied:
            #		squre.change_color('white')

            self.x = mouse.x
            self.y = mouse.y
            pozicia = [int(self.x//100+1), int(self.y//100+1)]
            self.redraw()
            if mouse.click:
            	mouse.click = False
            	for squar in self.available_l:
            			if squar.pozicia==pozicia:
            				if squar!=self.sqr:
		            			if self.color=='black':
		            				self.sqr.occupied = False
		            			else:
		            				self.sqr.b_occupied = False
		            			self.sqr = squar
		            			if self.color=='black':
		            				squar.occupied = True
		            			else:
		            				squar.b_occupied = True
		            			self.pozicia = pozicia
		            			self.board.turn +=1
		            		if self.color=='black':
		            			for e in self.board.b_entities:
		            				for s in e:
			            				if s.sqr==self.sqr: 
			            					s.kill()
		            		else:
		            			for e in self.board.entities:
		            				for s in e:
			            				if s.sqr == self.sqr:
			            					s.kill()
		            		self.moving = False


        square.change_color(square.defaultcolor)
        self.x = 100*(self.pozicia[0]-1)+50
        self.y = 100*(self.pozicia[1]-1)+50
        self.redraw()
        self.delete_available()
        self.board.moving = False

    def rule(self, square):
    	pozicia = square.pozicia
    	if pozicia[1]==self.pozicia[1]+1 and pozicia[0]==self.pozicia[0] and not square.b_occupied:
    		return True
    	if square.b_occupied:
    		if (square.pozicia[0]==self.pozicia[0]+1 or square.pozicia[0]==self.pozicia[0]-1) and square.pozicia[1]==self.pozicia[1]+1:
    			return True

    def available(self):
    	self.available_l = []
    	for square in self.board.squares:
    		if self.rule(square):
    			a = False
    			if not square.occupied and not square.b_occupied:
    				square.change_color('green')
    				self.available_l.append(square)

    			if square.b_occupied and self.sqr.occupied:
    					square.change_color('green')
    					self.available_l.append(square)

    			if square.occupied and self.sqr.b_occupied:
    					square.change_color('green')
    					self.available_l.append(square)




    	self.available_l.append(self.sqr)



    def delete_available(self):
    	for square in self.board.squares:
    		if square in self.available_l:
    			square.change_color(square.defaultcolor)

    def kill(self):
    	self.canvas.delete(self.objekt)
    	if self.color=='black':
    		self.sqr.occupied = False
    		for e in self.board.entities:
    			try:
    				e.remove(self)
    			except:
    				pass
    	else:
    		self.sqr.b_occupied = False
    		for e in self.board.b_entities:
    			try:
    				e.remove(self)
    			except:
    				pass

    def check_if_enemy(self, square):
    	if not square.occupied and not square.b_occupied:
    				square.change_color('green')
    				return 'OK'

    	elif square.b_occupied and self.sqr.occupied:
    				square.change_color('green')
    				return 'super'

    	elif square.occupied and self.sqr.b_occupied:
    				square.change_color('green')
    				return 'super'
    	else:
    		return 'end'




class Veza(Pesiak):
	def __init__(self, x, y, canvas):
		super().__init__(x, y, canvas)
		self.image = ImageTk.PhotoImage(Image.open('veza.png'))
		self.redraw()
		self.color = 'black'
		self.type = 'veza'

	def rule(self):
		available = []

		def check_below():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]+i+1 and square.pozicia[0]==self.pozicia[0]:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return
		def check_up():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]-i-1 and square.pozicia[0]==self.pozicia[0]:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return

		def check_right():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1] and square.pozicia[0]==self.pozicia[0]+i+1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return


		def check_left():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1] and square.pozicia[0]==self.pozicia[0]-i-1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return

		check_below()
		check_up()
		check_left()
		check_right()

		available.append(self.sqr)
		return available

	def available(self):
		self.available_l = self.rule()
 

class Kon(Pesiak):
    def __init__(self, x, y, canvas):
        super().__init__(x, y, canvas)
        self.image = ImageTk.PhotoImage(Image.open('kon.png'))
        self.redraw()
        self.color = 'black'
        self.type = 'kon'

    def rule(self, square):
    	a = square.pozicia[0]
    	b = square.pozicia[1]
    	x = self.pozicia[0]
    	y = self.pozicia[1]
    	if (a == x-1 or a == x+1) and (b == y-2 or b == y+2):
    		return True
    	elif (a == x-2 or a == x+2) and (b == y-1 or b == y+1):
    		return True

class Bishop(Pesiak):
	def __init__(self, x, y, canvas):
		super().__init__(x, y, canvas)
		self.image = ImageTk.PhotoImage(Image.open('bishop.png'))
		self.redraw()
		self.color = 'black'
		self.type = 'bishop'


	def rule(self):
		available = []

		def check_below():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]+i+1 and square.pozicia[0]==self.pozicia[0]+i+1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return 

		def check_up():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]-i-1 and square.pozicia[0]==self.pozicia[0]+i+1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return

		def check_right():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]-i-1 and square.pozicia[0]==self.pozicia[0]-i-1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return 

		def check_left():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]+i+1 and square.pozicia[0]==self.pozicia[0]-i-1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return 
		check_below()
		check_up()
		check_left()
		check_right()

		available.append(self.sqr)
		return available

	def available(self):
		self.available_l = self.rule()

class King(Pesiak):
    def __init__(self, x, y, canvas):
        super().__init__(x, y, canvas)
        self.image = ImageTk.PhotoImage(Image.open('king.png'))
        self.redraw()
        self.color = 'black'
        self.type = 'king'

    def rule(self, square):
    	pozicia = square.pozicia
    	if (pozicia[0]==self.pozicia[0]+1 or pozicia[0] == self.pozicia[0] or pozicia[0]==self.pozicia[0]-1) and (pozicia[1]==self.pozicia[1]+1 or pozicia[1]==self.pozicia[1] or pozicia[1]==self.pozicia[1]-1):
    			return True


class Queen(Pesiak):
	def __init__(self, x, y, canvas):
		super().__init__(x, y, canvas)
		self.image = ImageTk.PhotoImage(Image.open('queen.png'))
		self.redraw()
		self.color = 'black'
		self.type = 'queen'


	def rule(self):
		available = []

		def check_below():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]+i+1 and square.pozicia[0]==self.pozicia[0]+i+1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return 

		def check_up():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]-i-1 and square.pozicia[0]==self.pozicia[0]+i+1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return

		def check_right():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]-i-1 and square.pozicia[0]==self.pozicia[0]-i-1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return 

		def check_left():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]+i+1 and square.pozicia[0]==self.pozicia[0]-i-1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return 
		check_below()
		check_up()
		check_left()
		check_right()

		def check_below():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]+i+1 and square.pozicia[0]==self.pozicia[0]:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return
		def check_up():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1]-i-1 and square.pozicia[0]==self.pozicia[0]:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return

		def check_right():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1] and square.pozicia[0]==self.pozicia[0]+i+1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return


		def check_left():
				for i in range(8):
					for square in self.board.squares:
						if square.pozicia[1]==self.pozicia[1] and square.pozicia[0]==self.pozicia[0]-i-1:
							a = self.check_if_enemy(square)
							if a=='OK':
								available.append(square)
							elif a=='super':
								available.append(square)
								return 
							else:
								return

		check_below()
		check_up()
		check_left()
		check_right()


		available.append(self.sqr)
		return available

	def available(self):
		self.available_l = self.rule()



class b_pesiak(Pesiak):
	def __init__(self, x, y, board):
		super().__init__(x, y, board)
		self.image = ImageTk.PhotoImage(Image.open('b_pesiak.png'))
		self.objekt = board.canvas.create_image(x,y, image= self.image)
		self.pozicia = [int(x//100+1), int(y//100+1)]
		self.color = 'white'
		self.sqr.occupied = False
		self.sqr.b_occupied = True

	def rule(self, square):
		pozicia = square.pozicia
		if pozicia[1]==self.pozicia[1]-1 and pozicia[0]==self.pozicia[0] and not square.occupied:
			return True
		if square.occupied:
			if (pozicia[0]==self.pozicia[0]+1 or pozicia[0]==self.pozicia[0]-1) and pozicia[1]==self.pozicia[1]-1:
				return True

class b_veza(Veza):
	def __init__(self, x, y, board):
		super().__init__(x, y, board)
		self.image = ImageTk.PhotoImage(Image.open('b_veza.png'))
		self.objekt = board.canvas.create_image(x,y, image= self.image)
		self.pozicia = [int(x//100+1), int(y//100+1)]
		self.color = 'white'
		self.sqr.occupied = False
		self.sqr.b_occupied = True

class b_kon(Kon):
	def __init__(self, x, y, board):
		super().__init__(x, y, board)
		self.image = ImageTk.PhotoImage(Image.open('b_kon.png'))
		self.objekt = board.canvas.create_image(x,y, image= self.image)
		self.pozicia = [int(x//100+1), int(y//100+1)]
		self.color = 'white'
		self.sqr.occupied = False
		self.sqr.b_occupied = True


class b_bishop(Bishop):
	def __init__(self, x, y, board):
		super().__init__(x, y, board)
		self.image = ImageTk.PhotoImage(Image.open('b_bishop.png'))
		self.objekt = board.canvas.create_image(x,y, image= self.image)
		self.pozicia = [int(x//100+1), int(y//100+1)]
		self.color = 'white'
		self.sqr.occupied = False
		self.sqr.b_occupied = True

class b_king(King):
	def __init__(self, x, y, board):
		super().__init__(x, y, board)
		self.image = ImageTk.PhotoImage(Image.open('b_king.png'))
		self.objekt = board.canvas.create_image(x,y, image= self.image)
		self.pozicia = [int(x//100+1), int(y//100+1)]
		self.color = 'white'
		self.sqr.occupied = False
		self.sqr.b_occupied = True

class b_queen(Queen):
	def __init__(self, x, y, board):
		super().__init__(x, y, board)
		self.image = ImageTk.PhotoImage(Image.open('b_queen.png'))
		self.objekt = board.canvas.create_image(x,y, image= self.image)
		self.pozicia = [int(x//100+1), int(y//100+1)]    
		self.color = 'white'	
		self.sqr.occupied = False
		self.sqr.b_occupied = True	




        
        
        


class Mouse():
    def __init__(self):
        self.click = False
    
    def motion(self, event):
        self.x = event.x
        self.y = event.y

        


                    


mouse = Mouse()
main = User()
main.mainloop()
