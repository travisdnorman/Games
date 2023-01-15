#"C:\Program Files (x86)\IronPython 2.7\ipy64.exe" BattleShip.py

import string
import random

rows = ['A','B','C','D','E','F','G','H','I','J']
			
ships = {5:'Carrier',4:'Cruiser',3:'Submarine',2:'Destroyer'} #,4:'Cruiser',3:'Submarine',2:'Destroyer'

class Player:
			
	def place_ship(self,length):
		start_cord, dir = get_coord_and_dir(length)
		while(not self.check_placement(start_cord,dir,length)):
			print('Invalid Placement')
			start_cord, dir = get_coord_and_dir(length)	
		if(len(start_cord) == 3):
			column = 9
		else:
			column = int(start_cord[1])-1
		row = rows.index(start_cord[0].upper())
		if(dir == 'L'):
			self.defend_board[row][column-length+1:column+1] = ['O'] * length
		elif(dir == 'R'):
			self.defend_board[row][column:column+length] = ['O'] * length
		elif(dir == 'D'):
			for r in range(row,row+length):
				self.defend_board[r][column] = 'O'
		else:
			for r in range(row-length+1,row+1):
				self.defend_board[r][column] = 'O'
		print_board(self.defend_board)
		self.track_ship(length,row,column,dir)
		print(ships[length] + ' Placed Successfully')
		
	def track_ship(self,length,row,column,dir):
		if(dir == 'L'):
			for i in range(length):
				self.ships[length].append((row,column-i))
		elif(dir == 'R'):
			for i in range(length):
				self.ships[length].append((row,column+i))
		elif(dir == 'D'):
			for i in range(length):
				self.ships[length].append((row+i,column))
		else:
			for i in range(length):
				self.ships[length].append((row-i,column))
				
	def log_hit(self,row,col):
		for k in self.ships.keys():
			if (row,col) in self.ships[k]:
				self.ships[k].remove((row,col))
				if(len(self.ships[k]) == 0):
					self.ships.pop(k)
					return k
				else:
					return 0
		
	def check_placement(self,start_cord,dir,ship_length):
		if(len(start_cord) == 3):
			column = 9
		else:
			column = int(start_cord[1])-1
		row = rows.index(start_cord[0].upper())
		if(dir == 'L'):
			if((column - ship_length) < 0):
				return False
			for offset in range(ship_length):
				if(self.defend_board[row][column - offset] == 'O'):
					return False
		elif(dir == 'R'):
			if(column + ship_length > 9):
				return False
			for offset in range(ship_length):
				if(self.defend_board[row][column + offset] == 'O'):
					return False
		elif(dir == 'D'):
			if((row + ship_length) > 9):
				return False
			for offset in range(ship_length):
				if(self.defend_board[row + offset][column] == 'O'):
					return False
		else:
			if((row - ship_length) < 0):
				return False
			for offset in range(ship_length):
				if(self.defend_board[row - offset][column] == 'O'):
					return False
		return True	
		
	def __init__(self,name):
		self.attack_board = create_blank_board()
		self.defend_board = create_blank_board()
		self.points = 0
		self.name = name
		self.ships = {}
		print_board(self.defend_board)
		for ship in ships.keys():
			self.ships[ship] = []
			self.place_ship(ship)
			
	def attack(self, p):
		print_board(self.attack_board)
		while(True):
			attack_coord = input('Enter which Coordinate to attack\n')
			if(not check_valid_cord(attack_coord)):
				print('Invalid Coordinate')
				continue
			if(len(attack_coord) == 3):
				column = 9
			else:
				column = int(attack_coord[1])-1
			row = rows.index(attack_coord[0].upper())
			if(self.attack_board[row][column] == ' '):
				break
		if(self.attack_board[row][column] != ' '):
			print('Coordinate previously attacked, please choose different coordinate')
		if(p.defend_board[row][column] == 'O'):
			self.points += 1
			print ('HIT ' + self.name + ' Points: ' + str(self.points))
			p.defend_board[row][column] = 'X'
			self.attack_board[row][column] = 'X'
			h = p.log_hit(row,column)
			if(h != 0):
				print (p.name + '\'s ' + ships[h] + ' has been SUNK')
		else:
			print ('MISS')
			self.attack_board[row][column] = '*'
			
class Bot(Player):
	def __init__(self,name):
		self.attack_board = create_blank_board()
		self.defend_board = create_blank_board()
		self.points = 0
		self.name = name
		self.attack_coordinates = []
		self.last_play = 'miss'
		self.dirs = []
		self.make_dirs()
		self.hits = []
		self.ships = {}
		for row in range(0,10):
				if(row % 2 == 0):
					for column in range(0,9,2):
						self.attack_coordinates.append((row,column))
				else:
					for column in range(1,10,2):
						self.attack_coordinates.append((row,column))
		random.shuffle(self.attack_coordinates)
		print_board(self.defend_board)
		for ship in ships.keys():
			self.ships[ship] = []
			self.place_ship(ship)
		
	def place_ship(self,length):
		while(True):
			start_cord = random.choice(rows) + str(random.randint(1,10))
			dir = random.choice(self.dirs)
			if(self.check_placement(start_cord,dir,length)):
				break
		if(len(start_cord) == 3):
			column = 9
		else:
			column = int(start_cord[1])-1
		row = rows.index(start_cord[0].upper())
		if(dir == 'L'):
			self.defend_board[row][column-length+1:column+1] = ['O'] * length
		elif(dir == 'R'):
			self.defend_board[row][column:column+length] = ['O'] * length
		elif(dir == 'D'):
			for r in range(row,row+length):
				self.defend_board[r][column] = 'O'
		else:
			for r in range(row-length+1,row+1):
				self.defend_board[r][column] = 'O'
		print_board(self.defend_board)
		self.track_ship(length,row,column,dir)
		print(ships[length] + ' Placed Successfully')
		
	def attack(self, p):
		while(True):
			if(len(self.hits) == 0):
				if(len(self.attack_coordinates) == 0):
					for row in range(0,10):
						for column in range(0,10):
							if(self.attack_board[row][column] == 'X'):
								self.attack_coordinates.append((row+1,column))
								self.attack_coordinates.append((row-1,column))
								self.attack_coordinates.append((row,column+1))
								self.attack_coordinates.append((row,column-1))
					random.shuffle(self.attack_coordinates)
				coord = self.attack_coordinates.pop()
				row = coord[0]
				column = coord[1]	
			else:
				last_hit = self.hits[-1]
				if(self.dirs[0] == 'U'):
					row = last_hit[0] - 1
					column = last_hit[1]
				elif(self.dirs[0] == 'D'):
					row = last_hit[0] + 1
					column = last_hit[1]
				elif(self.dirs[0] == 'R'):
					row = last_hit[0]
					column = last_hit[1] + 1
				else:
					row = last_hit[0]
					column = last_hit[1] - 1
			if(0 <= row <= 9 and 0 <= column <= 9):
				if(self.attack_board[row][column] == ' '):
					break
				elif(self.attack_board[row][column] == 'X'):
					self.hits.append((row,column))
					continue
			self.adjust_attack(0)
		print ('Bot ' + self.name + ' attacks coordinate: ' + rows[row] + str(column+1))
		if((row,column) in self.attack_coordinates):
			self.attack_coordinates.remove((row,column))
		if(p.defend_board[row][column] == 'O'):
			self.points += 1
			print ('HIT ' + self.name + ' Points: ' + str(self.points))
			p.defend_board[row][column] = 'X'
			self.attack_board[row][column] = 'X'
			self.hits.append((row,column))
			self.last_play = 'hit'
			h = p.log_hit(row,column)
			if(h != 0):
				print (p.name + '\'s ' + ships[h] + ' has been SANK')
				self.detect_stray_hits(h)
				self.adjust_attack(1)
		else:
			print ('MISS')
			self.attack_board[row][column] = '*'
			self.adjust_attack(0)
			self.last_play = 'miss'
		print_board(self.attack_board)
		
	def make_dirs(self):
		self.dirs = ['U','D','R','L']
		random.shuffle(self.dirs)
	
	def adjust_attack(self, cause):
		if(cause == 1):
			self.hits = []
			self.make_dirs()
			self.last_play = 'miss'
		elif(len(self.hits) == 1 and len(self.dirs) != 1):
			del self.dirs[0]
		elif(self.last_play == 'hit'):
			if(self.dirs[0] == 'U'):
				if('D' in self.dirs):
					self.dirs.remove('D')
					self.dirs[0] = 'D'
					self.hits.append(self.hits[0])
					del self.hits[0]
				else:
					self.detect_stray_hits(0)
					self.hits = []
					self.make_dirs()
					self.last_play = 'miss'
			elif(self.dirs[0] == 'D'):
				if('U' in self.dirs):
					self.dirs.remove('U')
					self.dirs[0] = 'U'
					self.hits.append(self.hits[0])
					del self.hits[0]
				else:
					self.detect_stray_hits(0)
					self.hits = []
					self.make_dirs()
					self.last_play = 'miss'
			elif(self.dirs[0] == 'R'):
				if('L' in self.dirs):
					self.dirs.remove('L')
					self.dirs[0] = 'L'
					self.hits.append(self.hits[0])
					del self.hits[0]	
				else:
					self.detect_stray_hits(0)
					self.hits = []
					self.make_dirs()
					self.last_play = 'miss'
			else:
				if('R' in self.dirs):
					self.dirs.remove('R')
					self.dirs[0] = 'R'
					self.hits.append(self.hits[0])
					del self.hits[0]
				else:
					self.detect_stray_hits(0)
					self.hits = []
					self.make_dirs()
					self.last_play = 'miss'
		else:
			self.hits = []
			self.make_dirs()

	def detect_stray_hits(self, len_ship_sank):
		if(len_ship_sank == 0):
			if(self.hits[0][0] == self.hits[-1][0]):
				for hit in self.hits:
					self.attack_coordinates.append((hit[0]+1,hit[1]))
					self.attack_coordinates.append((hit[0]-1,hit[1]))
			else:
				for hit in self.hits:
					self.attack_coordinates.append((hit[0],hit[1]+1))
					self.attack_coordinates.append((hit[0],hit[1]-1))
		elif(len_ship_sank < len(self.hits)):
			if(self.hits[-1][0] == self.hits[-2][0]):
				row = self.hits[-1][0]
				if(self.hits[-1][1] < self.hits[0][1]):
					column = self.hits[-1][1]+len(self.hits)-1
					self.attack_coordinates.append((row,column))
					for i in range(len(self.hits)-len_ship_sank):
						column = self.hits[-1][1] + len_ship_sank + i
						self.attack_coordinates.append((row+1,column))
						self.attack_coordinates.append((row-1,column))
				else:
					column = self.hits[-1][1]-len(self.hits)+1
					self.attack_coordinates.append((row,column))
					for i in range(len(self.hits)-len_ship_sank):
						column = self.hits[-1][1] - len_ship_sank - i
						self.attack_coordinates.append((row+1,column))
						self.attack_coordinates.append((row-1,column))
			else:
				column = self.hits[-1][1]
				if(self.hits[-1][0] < self.hits[0][0]):
					row = self.hits[-1][0]+len(self.hits)-1
					self.attack_coordinates.append((row,column))
					for i in range(len(self.hits)-len_ship_sank):
						row = self.hits[-1][0] + len_ship_sank + i
						self.attack_coordinates.append((row,column+1))
						self.attack_coordinates.append((row,column-1))
				else:
					column = self.hits[-1][0]-len(self.hits)+1
					self.attack_coordinates.append((row,column))
					for i in range(len(self.hits)-len_ship_sank):
						row = self.hits[-1][0] - len_ship_sank - i
						self.attack_coordinates.append((row,column+1))
						self.attack_coordinates.append((row,column-1))



def create_blank_board():
	return [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
			[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]
			
def get_coord_and_dir(length):
	selected = False
	while(not selected):
		start_cord = input("Enter coordinate to begin placement of " + ships[length] + '(' + str(length) + ')\n')
		if(not check_valid_cord(start_cord)):
			print("coordinate not valid")
			continue
		direction_selected = False
		while(not direction_selected):
			direction = input('Enter the direction you would the ship to be placed\n' \
									'U = Up\n' \
									'D = Down\n' \
									'R = Right\n' \
									'L = Left\n' \
									'X = Select Start Coordinate Agian\n').upper()
			if(check_valid_direction(direction)):
				if(direction == 'X'):
					break
				direction_selected = True
			else:
				print ('Invalid Direction\n' \
						'Please Try Again')
		selected = True
	return start_cord,direction
			
def print_board(board):
		print ('|'.join([' ','1','2','3','4','5','6','7','8','9','10','']))
		for i in range(len(board)):
			print ('|'.join([rows[i]] + board[i] + ['']))
		print ('')
				
def check_valid_cord(coordinate):
	if(0 == len(coordinate) or len(coordinate) > 3): 
		return False
	if(not coordinate[0].isalpha() or not coordinate[1].isdigit()):
		return False
	if(not coordinate[0].upper() in rows or int(coordinate[1]) == 0):
		return False
	if(len(coordinate) == 3 and (not coordinate[2].isdigit() or int(coordinate[2]) > 0)):
		return False
	return True
	
def check_valid_direction(dir):
	valid_dirs = ['U','D','R','L','X']
	if(len(dir) != 1 or not dir in valid_dirs):
		return False
	return True	
	
if __name__ == '__main__':
	while True:
		p1 = Player('P1')
		p2 = Bot('P2')
		while(p1.points != 14 and p2.points != 14):
			# cont = raw_input('Would you like to continue\n'\
								# 'Y = yes\n'\
								# 'N = no\n'\
								# '1 = Print Player 1\'s Board\n'\
								# '2 = Print Player 2\'s Board\n').upper()
			# if(cont == 'N'):
				# break
			# if(cont == '1'):
				# print_board(p1.defend_board)
			# elif(cont == '2'):
				# print_board(p2.defend_board)
			
			p1.attack(p2)
			p2.attack(p1)
		if(p1.points == 14):
			print ('\n' + p1.name + ' WINS\n')
		else:
			print ('\n' + p2.name + ' WINS\n')
		print ('P1\'s Board')
		print_board(p1.defend_board)
		print ('P2\'s Board')
		print_board(p2.defend_board)
		answer	= input('Would you like to play again?\n').upper()
		if(answer[0] == 'N'):
			print ('Thank You for Playing')
			break
			