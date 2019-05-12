# This file provides the runtime support for running a basic program
# Assumes the program has been parsed using basparse.py

import sys
import math
import random

class MyInterpreter:
	
	# Initialize the interpreter. prog is a dictionary
	# containing (line,statement) mappings
	def __init__(self, prog):
		self.prog = prog

		self.functions = {           # Built-in function table
			'INT': lambda z: int(self.eval(z)),
			'RND': lambda z: random.random()
		}
		

	# Collecting all data statements
	def collect_data(self):
		self.data = []
		for lineno in self.stat:
			if self.prog[lineno][0] == 'DATA':
				self.data = self.data + self.prog[lineno][1]
		self.dc = 0                  # Initialize the data counter


	  # Check for finish statements


	# Checking finish statement in the prog
	def check_finish(self):
		has_end = 0
		for lineno in self.stat:
			if self.prog[lineno][0] == 'FINISH' and not has_end:
				has_end = lineno
		if not has_end:
			print("NO FINISH INSTRUCTION")
			self.error = 1
			return
		if has_end != lineno:
			print("FINISH IS NOT LAST")
			self.error = 1


	#Checking the correct number of fucntions and returns
	def check_functions_correctness(self):
		print('OKAY')


	#Creating a robot
	def create_robot(self, cord1, cord2):
		self.robot.append(cord1)
		self.robot.append(cord2)
		self.robot.append('RIGHT')
		self.path.append((cord1, cord2))
		self.sc.append(self.cells[cord1][cord2])
		self.sc.append(self.cells[cord1][cord2])
		self.cells[cord1][cord2] = 'R'


	#Creating a cell
	def create_cell(self):
		temp = ['*'] * 7
		v = []
		for i in range(7):
			v.append(temp[:])
		self.cells = v
		labirinth = (
		('0', '0', '0', '0', '0'), ('0', '0', '?', '0', '0'), ('0', '0', '@', '0', '0'), ('0', '0', '0', '0', '0'),
		('0', '0', '|', '0', '0'))
		for i in range(len(labirinth)):
			for j in range(len(labirinth[i])):
				if labirinth[i][j] == '0':
					self.cells[i + 1][j + 1] = '0'
				elif labirinth[i][j] == '|':
					self.cells[i + 1][j + 1] = '|'
				elif labirinth[i][j] == 'E':
					self.cells[i + 1][j + 1] = 'E'
				elif labirinth[i][j] == '*':
					self.cells[i + 1][j + 1] = '*'
				elif labirinth[i][j] == '$':
					self.cells[i + 1][j + 1] = '$'
				elif labirinth[i][j] == '+':
					self.cells[i + 1][j + 1] = '+'
				elif labirinth[i][j] == '~':
					self.cells[i + 1][j + 1] = '~'
				elif labirinth[i][j] == '@':
					self.cells[i + 1][j + 1] = '@'
				elif labirinth[i][j] == '%':
					self.cells[i + 1][j + 1] = '%'
				elif labirinth[i][j] == '?':
					self.cells[i + 1][j + 1] = '?'


	# Creating a list of walls (special materials)
	def create_walls(self):
		d = {
		"$": 60,  	#steel
		"~": 10,	#plastic
		"+": 20,		#glass	
		"@": 40,		#concrete
		"%": 110,	#steel-glass-plastic-glass
		"?": 30,		#plastic-glass
		"|": 5
		}	
		self.walls.update(d)
   

	#Printing a cell
	def print_cell(self):
		i = 0
		j = 0
		for i in range(len(self.cells)):
			print self.cells[i][0],self.cells[i][1],self.cells[i][2],self.cells[i][3],self.cells[i][4],self.cells[i][5],self.cells[i][6]
		print " "


	#Going forward
	def forward(self):
		if self.robot[2] == 'RIGHT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1][cord2 + 1] != '|' and self.cells[cord1][cord2 + 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 + 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 + 1] = 'R'
				self.robot[1] = self.robot[1] + 1   
				print("right - go_forward")
				return True
			else:
				print("right - go_forward")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'LEFT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1][cord2 - 1] != '|' and self.cells[cord1][cord2 - 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 - 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 - 1] = 'R'
				self.robot[1] = self.robot[1] - 1     
				print("left - go_forward")
				return True
			else:
				print("left - go_forward")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'FORWARD':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1 - 1][cord2] != '|' and self.cells[cord1 - 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 -1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 - 1][cord2] = 'R'
				self.robot[0] = self.robot[0] - 1    
				print("forward - go_forward")
				return True
			else:
				print("forward - go_forward")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'BACK':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1 + 1][cord2] != '|' and self.cells[cord1 + 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 + 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 + 1][cord2] = 'R'
				self.robot[0] = self.robot[0] + 1	
				print("back - go_forward")
				return True
			else:
				print("back - go_forward")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False


	#Going backwards
	def back(self):
		if self.robot[2] == 'RIGHT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1][self.robot[1] - 1] != '|' and self.cells[cord1][self.robot[1] - 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 - 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 - 1] = 'R'
				self.robot[1] = self.robot[1] - 1
				print("right - go_back")
				return True
			else:
				print("right - go_back")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'LEFT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1][cord2 + 1] != '|' and self.cells[cord1][cord2 + 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 + 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 + 1] = 'R'
				self.robot[1] = self.robot[1] + 1
				print("left - go_back")
				return True
			else:
				print("left - go_back")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'FORWARD':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			if self.cells[cord1 + 1][cord2] != '|' and self.cells[cord1 + 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 + 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 + 1][cord2] = 'R'
				self.robot[0] = self.robot[0] + 1
				print("forward - go_back")
				return True
			else:
				print("forward - go_back")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'BACK':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			if self.cells[cord1 - 1][cord2] != '|' and self.cells[cord1 - 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 + 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 - 1][cord2] = 'R'
				self.robot[0] = self.robot[0] - 1
				print("back - go_back")
				return True
			else:
				print("back - go_back")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		

	#Going to the right side
	def right(self):
		if self.robot[2] == 'RIGHT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1 + 1][cord2] != '|' and self.cells[cord1 + 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 + 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 + 1][cord2] = 'R'
				self.robot[0] = self.robot[0] + 1
				print("right - go_right")
				return True
			else:
				print("right - go_right")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'LEFT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1 - 1][cord2] != '|' and self.cells[cord1 - 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 - 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 - 1][cord2] = 'R'
				self.robot[0] = self.robot[0] - 1
				print("left - go_right")
				return True
			else:
				print("left - go_right")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'FORWARD':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			if self.cells[cord1][cord2 + 1] != '|' and self.cells[cord1][cord2 + 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 + 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 + 1] = 'R'
				self.robot[1] = self.robot[1] + 1
				print("forward - go_right")
				return True
			else:
				print("forward - go_right")				
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'BACK':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			if self.cells[cord1][cord2 + 1] != '|' and self.cells[cord1][cord2 + 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 - 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 + 1] = 'R'
				self.robot[1] = self.robot[1] + 1
				print("back - go_right")
				return True
			else:
				print("back - go_right")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False


	#Going to the left side
	def left(self):
		if self.robot[2] == 'RIGHT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1 - 1][cord2] != '|' and self.cells[cord1 - 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 - 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 - 1][cord2] = 'R'
				self.robot[0] = self.robot[0] - 1
				print("right - go_left")
				return True
			else:
				print("right - go_left")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'LEFT':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			if self.cells[cord1 + 1][cord2] != '|' and self.cells[cord1 + 1][cord2] != '*':
				self.sc[1] = self.cells[cord1 + 1][cord2]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1 + 1][cord2] = 'R'
				self.robot[0] = self.robot[0] + 1
				print("left - go_left")
				return True
			else:
				print("left - go_left")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'FORWARD':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			if self.cells[cord1][cord2 - 1] != '|' and self.cells[cord1][cord2 - 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 - 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 - 1] = 'R'
				self.robot[1] = self.robot[1] - 1
				print("forward - go_left")
				return True
			else:
				print("forward - go_left")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False
		elif self.robot[2] == 'BACK':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			if self.cells[cord1][cord2 - 1] != '|' and self.cells[cord1][cord2 - 1] != '*':
				self.sc[1] = self.cells[cord1][cord2 - 1]
				self.cells[cord1][cord2] = self.sc[0]
				self.sc[0] = self.sc[1]
				self.cells[cord1][cord2 - 1] = 'R'
				self.robot[1] = self.robot[1] - 1
				print("back - go_left")
				return True
			else:
				print("back - go_left")
				print("ROBOT CANNOT GO THIS WAY, TURN THE OTHER WAY")
				return False


	#Function which defines the rotation to the left side
	def rotate_left(self):   
		if self.robot[2] == 'RIGHT':   		#now
			self.robot[2] = 'FORWARD'		#then
			print ("turn: right->forward")
		elif self.robot[2] == 'FORWARD':
			self.robot[2] = 'LEFT'
			print ("turn: forward->left")
		elif self.robot[2] == 'LEFT':
			self.robot[2] = 'BACK'
			print("turn: left->back")
		elif self.robot[2] == 'BACK':
			self.robot[2] = 'RIGHT'
			print("turn: back->right")
		return True


	#Function which defines the rotation to the right side
	def rotate_right(self):
		if self.robot[2] == 'RIGHT':
			self.robot[2] = 'BACK'
			print ("turn: right->back")
		elif self.robot[2] == 'BACK':
			self.robot[2] == 'LEFT'
			print ("turn: back->left")
		elif self.robot[2] == 'LEFT':
			self.robot[2] = 'FORWARD'
			print ("turn: left->forward")
		elif self.robot[2] == 'FORWARD':
			self.robot[2] = 'RIGHT'
			print ("turn: forward->right")
		return True


	#Check finish cell in the labyrinth
	def check_finish_in_lab(self):
		if self.sc[0] == 'E':
			print("ROBOT FOUND EXIT FROM LABIRINTH AWESOME!!!!")
			return 1


	#This is how my radar is working
	def lms(self):
		walls = ['?', '@', '%', '+', '*', '$', '~']
		if self.robot[2] == 'RIGHT':   
			x = self.robot[0]
			y = self.robot[1]
			counter = 0
			for i in range(y, len(self.cells[x])):
				if self.cells[x][i] in walls:
					print counter
					print ' '
					return 0
				counter = counter + 1   

		elif self.robot[2] == 'LEFT':		
			x = self.robot[0]
			y = self.robot[1]
			counter = 0
			rev_list = []
			for item in reversed(self.cells[x]):
				rev_list.append(str(item))
			k = rev_list.index('R')	
			for i in range(k, len(rev_list)):
				if rev_list[i] in walls:
					print counter
					return 0
				counter = counter + 1

		elif self.robot[2] == 'FORWARD': 
			x = self.robot[0]
			y = self.robot[1]
			counter = 0
			rev_list = []
			good_list = []
			for item in range(len(self.cells[x])):
				rev_list.append(self.cells[item][y])
			for item in reversed(rev_list):
				good_list.append(str(item))
			k = good_list.index('R')	
			for i in range(k, len(good_list)):
				if good_list[i] in walls:
					print counter
					print ' '
					return 0
				counter = counter + 1

		elif self.robot[2] == 'BACK':	
			x = self.robot[0]
			y = self.robot[1]
			counter = 0
			for i in range(x, len(self.cells[x])):
				if self.cells[i][y] in walls:
					print  counter
					print ' '
					return 0
				counter = counter + 1


	#Defining the material of the wall
	def reflect(self):
		if self.robot[2] == 'RIGHT':
			x = self.robot[0]
			y = self.robot[1]
			if self.cells[x][y+1] == '|':
				print('WALL')
				return 0
			elif self.cells[x][y+1] == '*':
				print('UNDEF')
				return 0
			elif self.cells[x][y+1] == '$':
				print('STEEL')
				return 0
			elif self.cells[x][y+1] == '~':
				print('PLASTIC')
				return 0
			elif self.cells[x][y+1] == '+':
				print('GLASS')
				return 0
			elif self.cells[x][y+1] == '@':
				print('CONCRETE')
				return 0
			elif self.cells[x][y+1] == '%':
				print('STEEL-GLASS-PLASTIC-GLASS')
				return 0
			elif self.cells[x][y+1] == '?':
				print('PLASTIC-GLASS')
				return 0
			elif self.cells[x][y+1] in self.walls.keys():
				print('SOME KIND OF WALL')
				return 0
		elif self.robot[2] == 'LEFT':
			x = self.robot[0]
			y = self.robot[1]
			if self.cells[x][y-1] == '|' :
				print('WALL')
				return 0
			elif self.cells[x][y-1] == '*':
				print('UNDEF')
				return 0
			elif self.cells[x][y-1] == '$':
				print('STEEL')
				return 0
			elif self.cells[x][y-1] == '~':
				print('PLASTIC')
				return 0
			elif self.cells[x][y-1] == '+':
				print('GLASS')
				return 0
			elif self.cells[x][y-1] == '@':
				print('CONCRETE')
				return 0
			elif self.cells[x][y-1] == '%':
				print('STEEL-GLASS-PLASTIC-GLASS')
				return 0
			elif self.cells[x][y-1] == '?':
				print('PLASTIC-GLASS')
				return 0
			elif self.cells[x][y-1] in self.walls.keys():
				print('SOME KIND OF WALL')
				return 0
		elif self.robot[2] == 'FORWARD':
			x = self.robot[0]
			y = self.robot[1]
			if self.cells[x-1][y] == '|' :
				print('WALL')
				return 0
			elif self.cells[x-1][y] == '*':
				print('UNDEF')
				return 0
			elif self.cells[x-1][y] == '$':
				print('STEEL')
				return 0
			elif self.cells[x-1][y] == '~':
				print('PLASTIC')
				return 0
			elif self.cells[x-1][y] == '+':
				print('GLASS')
				return 0
			elif self.cells[x-1][y] == '@':
				print('CONCRETE')
				return 0
			elif self.cells[x-1][y] == '%':
				print('STEEL-GLASS-PLASTIC-GLASS')
				return 0
			elif self.cells[x-1][y] == '?':
				print('PLASTIC-GLASS')
				return 0
			elif self.cells[x-1][y] in self.walls.keys():
				print('SOME KIND OF WALL')
				return 0
		elif self.robot[2] == 'BACK':
			x = self.robot[0]
			y = self.robot[1]
			if self.cells[x+1][y] == '|' :
				print('WALL')
				return 0
			elif self.cells[x+1][y] == '*':
				print('UNDEF')
				return 0
			elif self.cells[x+1][y] == '$':
				print('STEEL')
				return 0
			elif self.cells[x+1][y] == '~':
				print('PLASTIC')
				return 0
			elif self.cells[x+1][y] == '+':
				print('GLASS')
				return 0
			elif self.cells[x+1][y] == '@':
				print('CONCRETE')
				return 0
			elif self.cells[x+1][y] == '%':
				print('STEEL-GLASS-PLASTIC-GLASS')
				return 0
			elif self.cells[x+1][y] == '?':
				print('PLASTIC-GLASS')
				return 0
			elif self.cells[x+1][y] in self.walls.keys():
				print('SOME KIND OF WALL')
				return 0


	# Drilling the wall in the labyrinth
	def drill(self):
		if self.robot[2] == 'RIGHT':
			cord1 = self.robot[0]
			cord2 = self.robot[1]
			print("right - drill")
			if self.cells[cord1][cord2 + 1] == '*':
				print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
			elif self.cells[cord1][cord2 + 1] in self.walls:
				wall = self.cells[cord1][cord2 + 1]
				print wall
				k = self.walls[wall]
				if k < self.drill_cap:
					self.sc[1] = self.cells[cord1][cord2 + 1]
					self.cells[cord1][cord2] = self.sc[0]
					self.sc[0] = self.sc[1]
					self.cells[cord1][cord2 + 1] = 'R'
					self.robot[1] = self.robot[1] + 1
					self.drill_cap = self.drill_cap - k 
				else:
					print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
					self.drill_cap = 0
			else:
				print("ROBOT DOESNT KNOW WHAT TO DESTROY")  
				
		elif self.robot[2] == 'LEFT':
			cord1 = self.robot[0]
			cord2 = self.robot[1] 
			print("left - drill")
			if self.cells[cord1][cord2 - 1] == '*':
				print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
			elif self.cells[cord1][cord2 - 1] in self.walls:
				wall = self.cells[cord1][cord2 - 1]
				print wall
				k = self.walls[wall]
				if k < self.drill_cap:
					self.sc[1] = self.cells[cord1][cord2 - 1]
					self.cells[cord1][cord2] = self.sc[0]
					self.sc[0] = self.sc[1]
					self.cells[cord1][cord2 - 1] = 'R'
					self.robot[1] = self.robot[1] - 1  
					self.drill_cap = self.drill_cap - k
				else:
					print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
					self.drill_cap = 0
			else:
				print("ROBOT DOESNT KNOW WHAT TO DESTROY")

		elif self.robot[2] == 'FORWARD':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			print("forward - drill")
			if self.cells[cord1 - 1][cord2] == '*':
				print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")	
			elif self.cells[cord1 - 1][cord2] in self.walls:
				wall = self.cells[cord1 - 1][cord2]
				print wall
				k = self.walls[wall]
				if k <= self.drill_cap:
					self.sc[1] = self.cells[cord1 -1][cord2]
					self.cells[cord1][cord2] = self.sc[0]
					self.sc[0] = self.sc[1]
					self.cells[cord1 - 1][cord2] = 'R'
					self.robot[0] = self.robot[0] - 1   
					self.drill_cap = self.drill_cap - k
				else:
					print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
					self.drill_cap = 0
			else:
				print("ROBOT DOESNT KNOW WHAT TO DESTROY")	

		elif self.robot[2] == 'BACK':
			cord1 = self.robot[0]
			cord2 =  self.robot[1]
			print("back - drill")
			if self.cells[cord1 + 1][cord2] == '*':
				print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
			elif self.cells[cord1 + 1][cord2] in self.walls:
				wall = self.cells[cord1 + 1][cord2]
				print wall
				k = self.walls[wall]
				if k < self.drill_cap:
					self.sc[1] = self.cells[cord1 + 1][cord2]
					self.cells[cord1][cord2] = self.sc[0]
					self.sc[0] = self.sc[1]
					self.cells[cord1 + 1][cord2] = 'R'
					self.robot[0] = self.robot[0] + 1
					self.drill_cap = self.drill_cap - k
				else:
					print("ROBOT CANNOT DESTROY THIS WALL, TURN THE OTHER WAY")
					self.drill_cap = 0
			else:
				print("ROBOT DOESNT KNOW WHAT TO DESTROY")

			print 'CAPACITY OF DRILL:', self.drill_cap


	#Evaluate an expression
	def eval(self, expr):
		if type(expr) == int:
			return expr
		else:
			expr_type = expr[0]
			if expr_type == 'INTEGER':
				return expr[1]
			elif expr_type == 'STRING':
				return expr[1]
			elif expr_type == 'BOOLEAN':
				return expr[1]
			elif expr_type == 'TRUE':
				return expr[1]
			elif expr_type == 'FALSE':
				return expr[1]
			elif expr_type == 'UNDEFINED':
				return expr[1]
			elif expr_type == 'UNARY':
				if expr[1] == '-':		
					return -self.eval(expr[2])
			elif expr_type == 'BINOP':
				if expr[1] == '+':
					eval1 = self.eval(expr[2])
					eval2 = self.eval(expr[3])
					b=[]
					if (type(eval1) is int or eval1[1] == 'NUMERIC_VAR') and (type(eval2) is int or eval2[1]=='NUMERIC_VAR'):
						if type(eval2) is int and type(eval1) is int:
							b.append(eval1+eval2)
						elif type(eval2) is int and not type(eval1) is int:
							if eval1[0]=='UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval1[0]+eval2)
						elif not type(eval2) is int and type(eval1) is int:
							if eval2[0]=='UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval2[0]+eval1)
						elif not type(eval2) is int and not type(eval1) is int:
							if eval1[0] =='UNDEFINED' or eval2[0] == 'UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval1[0]+eval2[0])
						b.append('NUMERIC_VAR')
						return b

					if (type(eval1) is bool or eval1[1] == 'BOOLEAN') and (type(eval2) is bool or eval2[0] == 'BOOLEAN'):
						if (eval1[0] == 'FALSE') and (eval2[0] == 'FALSE'):
							b.append('FALSE')
						if (eval1[0] == 'FALSE') and (eval2[0] == 'TRUE'):
							b.append('TRUE')
						if (eval1[0] == 'TRUE') and (eval2[0] == 'FALSE'):
							b.append('TRUE')
						if (eval1[0] == 'TRUE') and (eval2[0] == 'TRUE'):
							b.append('TRUE')
						if (eval1[0] == 'FALSE') and (eval2[0] == 'UNDEFINED'):
							b.append('UNDEFINED')
						if (eval1[0] == 'UNDEFINED') and (eval2[0] == 'FALSE'):
							b.append('UNDEFINED')
						if (eval1[0] == 'TRUE') and (eval2[0] == 'UNDEFINED'):
							b.append('TRUE')
						if (eval1[0] == 'UNDEFINED') and (eval2[0] == 'TRUE'):
							b.append('TRUE')
						if (eval1[0] == 'UNDEFINED') and (eval2[0] == 'UNDEFINED'):
							b.append('UNDEFINED')
						b.append('BOOLEAN')
						return b
					
					if (type(eval1) is str or eval1[1] == 'STRING_VAR') and (type(eval1) is str or eval2[0] == 'STRING_VAR'):
						if type(eval2) is str and type(eval1) is int:
							b.append(eval1+eval2)
						elif type(eval2) is str and not type(eval1) is str:
							if eval1[0]=='UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval1[0]+eval2)
						elif not type(eval2) is str and type(eval1) is str:
							if eval2[0]=='UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval2[0]+eval1)
						elif not type(eval2) is str and not type(eval1) is str:
							if eval1[0] =='UNDEFINED' or eval2[0] == 'UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval1[0]+eval2[0])
						b.append('STRING_VAR')
						return b

				if expr[1] == '-':
					eval1 = self.eval(expr[2])
					eval2 = self.eval(expr[3])
					b=[]
					if (type(eval1) is int or eval1[1] == 'NUMERIC_VAR') and (type(eval2) is int or eval2[1]=='NUMERIC_VAR'):
						if type(eval2) is int and type(eval1) is int:
							b.append(eval1-eval2)
					elif type(eval2) is int and not type(eval1) is int:
						if eval1[0]=='UNDEFINED':
							b.append('UNDEFINED')
						else:
							b.append(eval1[0]+eval2)
					elif not type(eval2) is int and type(eval1) is int:
						if eval2[0]=='UNDEFINED':
							b.append('UNDEFINED')
						else:
							b.append(eval2[0]-eval1)
					elif not type(eval2) is int and not type(eval1) is int:
						if eval1[0] =='UNDEFINED' or eval2[0] == 'UNDEFINED':
							b.append('UNDEFINED')
						else:
							b.append(eval1[0]-eval2[0])
					b.append('NUMERIC_VAR')
					return b

					if (eval1[1] == 'BOOLEAN') and (eval2[0] == 'BOOLEAN'):
						if (eval1[0] == 'FALSE') and (eval2[0] == 'FALSE'):
							b.append('TRUE') 
						if (eval1[0] == 'FALSE') and (eval2[0] == 'TRUE'):
							b.append('FALSE')
						if (eval1[0] == 'TRUE') and (eval2[0] == 'FALSE'):
							b.append('FALSE')
						if (eval1[0] == 'TRUE') and (eval2[0] == 'TRUE'):
							b.append('FALSE')
						if (eval1[0] == 'FALSE') and (eval2[0] == 'UNDEFINED'):
							b.append('UNDEFINED')
						if (eval1[0] == 'UNDEFINED') and (eval2[0] == 'FALSE'):
							b.append('UNDEFINED')
						if (eval1[0] == 'TRUE') and (eval2[0] == 'UNDEFINED'):
							b.append('UNDEFINED')
						if (eval1[0] == 'UNDEFINED') and (eval2[0] == 'TRUE'):
							b.append('UNDEFINED')
						if (eval1[0] == 'UNDEFINED') and (eval2[0] == 'UNDEFINED'):
							b.append('UNDEFINED')
						b.append('BOOLEAN')
						return b

					if (eval1[1] == 'STRING_VAR') and (eval2[0] == 'STRING_VAR'):
						if type(eval2) is str and type(eval1) is int:
							b.append(eval1-eval2)
						elif type(eval2) is str and not type(eval1) is str:
							if eval1[0]=='UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval1[0]-eval2)
						elif not type(eval2) is str and type(eval1) is str:
							if eval2[0]=='UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval2[0]-eval1)
						elif not type(eval2) is str and not type(eval1) is str:
							if eval1[0] =='UNDEFINED' or eval2[0] == 'UNDEFINED':
								b.append('UNDEFINED')
							else:
								b.append(eval1[0]-eval2[0])
						b.append('STRING_VAR')
						return b

	# Evaluate a relational expression
	def releval(self, expr):
			expr_type = expr[1]
			lhs = self.eval(expr[2])
			rhs = self.eval(expr[3])
			if expr_type == '<':
				if lhs < rhs:
					return True
				else:
					return False

			elif expr_type == '>':
				if lhs > rhs:
					return True
				else:
					return False

			elif expr_type == '=':
				if lhs == rhs:
					return True
				else:
					return False

			elif expr_type == '<>':
				if lhs != rhs:
					return True
				else:
					return False

	# Assignment
	def assign(self, target, value, types):
		print '\t\tFunction assign'
		i = len(target) 
		k = 0 
		while i != 0:
			var = target[k][0]
			s = []
			a = value
			s.append(a)
			s.append(types)
			if types == 'BOOLEAN':
				self.bool[var] = s
			elif types == 'INTEGER':
				self.int[var] = s
				print var, s
			elif types == 'STRING':
				self.str[var] = s
			self.vars[var] = s 	# so we wont have same names of different variables
			i = i - 1
			k = k + 1


	def run(self):
		self.vars = {}			# all variables
		self.int = {}			# all int variables
		self.bool = {}			# all bool variables
		self.str = {}			# all string variables
		self.arrays = {}		# arrays variables
		self.tables = {}			# tables
		self.loops = []            # Currently active loops
		self.loopend = {}            # Mapping saying where loops end
		self.error = 0              # Indicates program error
		self.fucn = {}
		self.path = []
		self.cord1 = 0
		self.cord2 = 0
		self.parameters = {}
		self.global_parameters = 0
		self.ret = 0
		self.lists = {}

		self.stat = list(self.prog)  # Ordered list of all line numbers
		self.stat.sort()
		self.pc = 0                  # Current program counter
		self.robot = []
		self.walls = {}
		self.drill_cap = 50
		self.sc = []


		# Processing prior to running

		self.collect_data()          # Collect all of the data statements
		self.check_functions_correctness()
		self.check_finish()
		self.create_walls()
		self.create_cell()

		if self.error:
			raise RuntimeError

		while 1:
			line = self.stat[self.pc]
			instr = self.prog[line]
			self.ret = 0
			op = instr[0]
			#print '\t\tMy first instruction', op
		
		#FINISH
			if op == 'FINISH':
				break;   # We are done
			
		# PRINT statement
			elif op == 'PRINT':
				plist = instr[1]
				out = ""
				for label, val in plist:
					if out:
						out += ' ' * (15 - (len(out) % 15))
					out += label
					if val:
						if label:
							out += " "
						eval = self.eval(val)
						out += str(eval[0])
				sys.stdout.write(out)
				sys.stdout.write("\n")	

		# VARIABLE DECLARATION statement
			if op == 'INTEGER':
				target = instr[1]
				value = 0
				self.assign(target, value, op)
			elif op == 'STRING':
				target = instr[1]
				value = ''
				self.assign(target, value, op)
			elif op == 'BOOLEAN':
				target = instr[1]
				value = 'UNDEFINED'
				self.assign(target, value, op)
			
		# ASSIGN statement
			if op == 'ASSIGN':
				target = instr[1][0]
				value = instr[2]
				s = []
				i = []
				if target in self.vars:
					print 'target', 'this is my variable', instr[1][0]
					print 'its value', instr[2]
					s.append(target)
					s.append(value)
					if value[0] == 'BOOL':
						self.bool[target] = s
						print target, s
					elif value[0] == 'STR':
						self.str[target] = s
						print target, s
					elif value[0] == 'NUM':
						self.int[target] = s
						print target, s
					else:
						 print("UNDEFINED VARIABLE %s" % instr[1][0])
						 raise RuntimeError
				else:
					print ("VARIABLE NOT INITIALIZED %s" % instr[1][0])

				if target in self.lists:
					place = instr[1][1][1]
					var = value[1]
					if not target in self.lists:
						self.lists[var] = [0] * 10

						if place > len(self.lists[target]):
							print ("DIMENSION TOO LARGE AT LINE %s" % self.stat[self.pc])
							raise RuntimeError
						self.lists[target][place - 1] = self.eval(var)
					else:
						print("UNDEFINED VARIABLE %s" % instr[1][0])
						raise RuntimeError


			elif op == 'IF':
				loopvar = instr[1]
				print loopvar
				initval = instr[2]
				print initval
				if self.releval(loopvar) == True:
					print loopvar[2][0]
					if loopvar[2][0] == 'INTEGER':
						var1 = loopvar[2][1][0]
						if var1 in self.vars:
							self.ex(initval)
						else:
							print("UNDEFINED VARIABLE ")
							raise RuntimeError


			elif op == 'DO-UNTIL':
				loopvar = instr[1]
				initval = instr[2]
				a = len(initval)
				while self.releval(loopvar) == 1:
					if loopvar[2][0] == 'INTEGER':
						var1 = loopvar[2][1][0]
						if var1 in self.vars:
							b = self.vars[var1][0]
							b = b + 1
							self.vars[var1][0] = b
							self.int[var1][0] = b
						else:
							print("UNDEFINED VARIABLE ")
							raise RuntimeError
					self.ex(initval)
			# FUNCTION STATEMENT

			elif op == 'FUNCTION START':
				k = 0
				g = {}
				while k < len(self.func):
					if instr[1] in self.func:
					   self.ex(self.func[instr[1]])
					elif (k + 1) == len(self.func):
						print(" FUNCTION NOT DESCRIBED")
						raise RuntimeError
					k = k + 1

			elif op == 'FUNCTION':
				self.func[instr[1]] = instr[3]		

		# ROBOT STATEMENT

			elif op == 'ROBOT':
				self.create_robot(instr[1], instr[2])
				print("ROBOT CREATED")
				self.print_cell()


			elif op == 'FORWARD':
				i = 0
				#while i != instr[1]:
				self.forward()
				self.print_cell()
				i = i + 1
				if self.check_finish_in_lab() == 1:
					i = instr[1]
					break

			elif op == 'BACK':
				i = 0
				#while i != instr[1]:
				self.back()
				self.print_cell()
				i = i + 1
				if self.check_finish_in_lab() == 1:
					i = instr[1]
					break

			elif op == 'LEFT':
				i = 0
				#while i != instr[1]:
				self.left()
				self.print_cell()
				i = i + 1
				if self.check_finish_in_lab() == 1:
					i = instr[1]
					break

			elif op == 'RIGHT':
				i = 0
				#while i != instr[1]:
				self.right()
				self.print_cell()
				i = i + 1
				if self.check_finish_in_lab() == 1:
					i = instr[1]
					break

			elif op == 'ROTATE_LEFT':
				self.rotate_left()
				self.print_cell()

			elif op == 'ROTATE_RIGHT':
				self.rotate_right()
				self.print_cell()

			elif op == 'LMS':
				print 'LMS ACTIVATED'
				self.lms()

			elif op == 'REFLECT':
				print 'REFLECTOR ACTIVATED'
				self.reflect()

			elif op == 'DRILL':
				print 'DRILL ACTIVATED'
				self.drill()
				self.print_cell()

			elif op == 'RETURN':
				print("BIG ERROR")
				raise RuntimeError

			self.pc += 1


   # Erase the current program
	def new(self):
		self.prog = {}

	# Insert statements
	def add_statements(self, prog):
		for line, stat in prog.items():
			self.prog[line] = stat

	# Delete a statement
	def del_line(self, lineno):
		try:
			del self.prog[lineno]
		except KeyError:
			pass
