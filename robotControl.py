import socket
import time
import math
import random


class LineUs:
	"""An example class to show how to use the Line-us API"""

	def __init__(self, line_us_name):
		print('init the socket starts')
		self.__line_us = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__line_us.connect((line_us_name, 1337))
		self.__connected = True
		self.__hello_message = self.__read_response()

	def get_hello_string(self):
		if self.__connected:
			return self.__hello_message.decode()
		else:
			return 'Not connected'

	def disconnect(self):
		"""Close the connection to the Line-us"""
		self.__line_us.close()
		self.__connected = False

	#  Home Function
	#  Return to the HOME position which is (1000,1000,1000)
	def home(self):
		cmd = b'G28'
		self.__send_command(cmd)
		self.__read_response()

	#  Rapid Positioning function
	#  Move from current position to (X,Y,Z) at full speed
	#  Does not necessarily move in a straight line
	def g00(self, x, y, z):
		"""Send a G00 (interpolated move), and wait for the response before returning"""
		cmd = b'G00 X'
		cmd += str(x).encode()
		cmd += b' Y'
		cmd += str(y).encode()
		cmd += b' Z'
		cmd += str(z).encode()
		self.__send_command(cmd)
		self.__read_response()

	def g01(self, x, y, z):
		"""Send a G01 (interpolated move), and wait for the response before returning"""
		cmd = b'G01 X'
		cmd += str(x).encode()
		cmd += b' Y'
		cmd += str(y).encode()
		cmd += b' Z'
		cmd += str(z).encode()
		self.__send_command(cmd)
		self.__read_response()

	def __read_response(self):
		"""Read from the socket one byte at a time until we get a null"""
		line = b''
		while True:
			char = self.__line_us.recv(1)
			if char != b'\x00':
				line += char
			elif char == b'\x00':
				break
		return line

	def __send_command(self, command):
		"""Send the command to Line-us"""
		#print('Send the command to Line-us')
		command += b'\x00'
		self.__line_us.send(command)


def draw_Hi(my_line_us):

	print('Drawing Hi')
	my_line_us.g01(900, 300, 0)
	my_line_us.g01(900, -300, 0)
	my_line_us.g01(900, -300, 1000)

	my_line_us.g01(1200, 300, 0)
	my_line_us.g01(1200, -300, 0)
	my_line_us.g01(1200, -300, 1000)

	my_line_us.g01(900, 0, 0)
	my_line_us.g01(1200, 0, 0)
	my_line_us.g01(1200, 0, 1000)

	my_line_us.g01(1500, 150, 0)
	my_line_us.g01(1500, -300, 0)
	my_line_us.g01(1500, -300, 1000)

	my_line_us.g01(1500, 250, 0)
	my_line_us.g01(1500, 300, 0)
	my_line_us.g01(1500, 300, 1000)

def draw_CIRCLE(startX, startY, radius):
	my_line_us.g01(startX,startY,1000)
	for i in range(0,361):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX - radius + currX, startY + currY,500)
	my_line_us.g01(startX,startY+50,500)

#
# Draw '1'
#
def draw_1a(my_line_us):
	print('Drawing 1a')
	my_line_us.g01(1100, 800, 200)
	my_line_us.g01(1100, -900, 200)
	my_line_us.g01(1100, -900, 1000)

	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_1b(my_line_us):
	print('Drawing 1b')
	my_line_us.g01(1100, 800, 200)
	my_line_us.g01(1450, -900, 200)

	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_1c(my_line_us):
	print('Drawing 1c')
	my_line_us.g01(1100, 800, 200)
	my_line_us.g01(1100, -900, 200)
	my_line_us.g01(1100, 800, 1000)
	my_line_us.g01(650, 200, 0)

	# After each drawing, move back to the HOME position
	my_line_us.home()

def printOne():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("1a")
	elif selection == 2:
		draw_NUMBER("1b")
	else:
		draw_NUMBER("1c")

#
# Draw '2'
#
def draw_2a(my_line_us):
	print('Drawing 2a')
	my_line_us.g01(700, 700, 300)
	my_line_us.g01(1500, 700, 300)
	my_line_us.g01(1500, 0, 300)
	my_line_us.g01(700, 0, 300)
	my_line_us.g01(700, -700, 300)
	my_line_us.g01(1500, -700, 300)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_2b(my_line_us):
	print('Drawing 2b')
	startX = 700
	startY = 500
	radius = 500
	my_line_us.g01(startX,startY,1000)
	for i in range(181,-45,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	my_line_us.g01(700,-750,500)
	my_line_us.g01(1500,-750,500)
	my_line_us.home()

def draw_2c(my_line_us):
	print('Drawing 2c')
	startX = 800
	startY = 500
	radius = 500
	my_line_us.g01(startX,startY,1000)
	for i in range(181,-45,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	my_line_us.g01(900,-700,500)
	startX = 900
	startY = -700
	radius = 200
	for j in range(270,90,-1):
		currRads = j * (3.14159/180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + currX, startY + radius + currY, 500)
	my_line_us.g01(1500,-750,500)
	my_line_us.home()

def printTwo():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("2a")
	elif selection == 2:
		draw_NUMBER("2b")
	else:
		draw_NUMBER("2c")

#
# Draw '3'
#
def draw_3a(my_line_us):
	print('Drawing 3a')
	my_line_us.g01(700, 700, 300)
	my_line_us.g01(1500, 700, 300)
	my_line_us.g01(1500, 0, 300)
	my_line_us.g01(700, 0, 300)
	my_line_us.g01(1500, 0, 300)
	my_line_us.g01(1500, -700, 300)
	my_line_us.g01(700, -700, 300)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_3b(my_line_us):
	print('Drawing 3b')
	startX = 700
	startY = 700
	radius = 500
	for i in range(135,-90,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + (radius*math.sin(45*3.14159/180)) + currX, startY - (radius*math.sin(45*3.14159/180)) + currY,500)

	startX = startX + (radius*math.sin(45*3.14159/180)) + radius*math.cos(-90 * (3.13159/180))
	startY = startY - (radius*math.sin(45*3.14159/180)) + radius*math.sin(-90 * (3.13159/180))
	for j in range(90,-135,-1):
		currRads = j * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + currX, startY - radius + currY,500)

	my_line_us.home()

def draw_3c(my_line_us):
	print('Drawing 3c')
	startX = 1000
	startY = 700
	radius = 300
	for i in range(135,-90,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + (radius*math.sin(45*3.14159/180)) + currX, startY - (radius*math.sin(45*3.14159/180)) + currY,500)

	startX = startX + (radius*math.sin(45*3.14159/180)) + radius*math.cos(-90 * (3.13159/180))
	startY = startY - (radius*math.sin(45*3.14159/180)) + radius*math.sin(-90 * (3.13159/180))
	radius = 600
	for j in range(90,-135,-1):
		currRads = j * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + currX, startY - radius + currY,500)

	my_line_us.home()

def printThree():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("3a")
	elif selection == 2:
		draw_NUMBER("3b")
	else:
		draw_NUMBER("3c")


#
# Draw '4'
#

def draw_4a(my_line_us):
	print('Drawing 4a')
	my_line_us.g01(700, 700, 300)
	my_line_us.g01(700, 0, 300)
	my_line_us.g01(1500, 0, 300)
	my_line_us.g01(1100, 700, -500)
	my_line_us.g01(1100, 700, 300)
	my_line_us.g01(1100, -700, 300)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_4b(my_line_us):
	print('Drawing 4b')
	my_line_us.g01(1100, 700, 1000)
	my_line_us.g01(700, 0, 500)
	my_line_us.g01(1500, 0, 500)
	my_line_us.g01(1100, 700, 1000)
	my_line_us.g01(1100, -700, 500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_4c(my_line_us):
	print('Drawing 4c')
	my_line_us.g01(1100, 700, 1000)
	my_line_us.g01(1100, -700, 500)
	my_line_us.g01(1100, 700, 1000)
	my_line_us.g01(700, 0, 500)
	my_line_us.g01(1500, 0, 500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def printFour():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("4a")
	elif selection == 2:
		draw_NUMBER("4b")
	else:
		draw_NUMBER("4c")


#
# Draw '5'
#
def draw_5a(my_line_us):
	print('Drawing 5a')
	my_line_us.g01(1500, 700, -300)
	my_line_us.g01(700, 700, 500)
	my_line_us.g01(700, 0, 500)
	my_line_us.g01(1500, 0, 500)
	my_line_us.g01(1500, -700, 500)
	my_line_us.g01(700, -700, 500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_5b(my_line_us):
	print('Drawing 5b')
	my_line_us.g01(1500,700,1000)
	my_line_us.g01(700,700,500)
	my_line_us.g01(700,-100,500)
	startX = 700
	startY = -100
	radius = 400
	for i in range(180,-135,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	my_line_us.home()

def draw_5c(my_line_us):
	print('Drawing 5c')
	my_line_us.g01(1500,700,1000)
	my_line_us.g01(700,700,500)
	my_line_us.g01(700,-250,500)
	startX = 700
	startY = -100
	radius = 400
	my_line_us.g01(700,-100,1000)
	for i in range(180,-90,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	my_line_us.home()

def printFive():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("5a")
	elif selection == 2:
		draw_NUMBER("5b")
	else:
		draw_NUMBER("5c")

#
# Draw '6'
#
def draw_6a(my_line_us):
	print('Drawing 6a')
	my_line_us.g01(1000,700,1000)
	my_line_us.g01(800,-350,500)

	startX = 800
	startY = -350
	radius = 400
	my_line_us.g01(startX,startY,1000)
	for i in range(180,541):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_6b(my_line_us):
	print('Drawing 6b')
	my_line_us.g01(1000,700,1000)
	my_line_us.g01(1000,-250,500)

	startX = 1000
	startY = -250
	radius = 400
	my_line_us.g01(startX,startY,1000)
	for i in range(180,541):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_6c(my_line_us):
	print('Drawing 6c')
	startX = 800
	startY = -350
	radius = 400
	my_line_us.g01(startX,startY,1000)
	for i in range(180,-181,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		my_line_us.g01(startX + radius + currX, startY + currY,500)
	# After each drawing, move back to the HOME position
	my_line_us.g01(1000,700,500)
	my_line_us.home()

def printSix():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("6a")
	elif selection == 2:
		draw_NUMBER("6b")
	else:
		draw_NUMBER("6c")

#
# Draw '7'
#
def draw_7a(my_line_us):
	print('Drawing 7a')
	my_line_us.g01(700, 700, 1000)
	my_line_us.g01(1600, 700, 500)
	my_line_us.g01(1150, -700, 500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_7b(my_line_us):
	print('Drawing 7b')
	my_line_us.g01(700, 700, 1000)
	my_line_us.g01(1600, 700, 500)
	my_line_us.g01(900, -700, 500)
	my_line_us.g01(1000,0,1000)
	my_line_us.g01(1500,0,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_7c(my_line_us):
	print('Drawing 7c')
	my_line_us.g01(750, 550, 1000)
	my_line_us.g01(700, 700, 500)
	my_line_us.g01(1600, 700, 500)
	my_line_us.g01(1150, -700, 500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def printSeven():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("7a")
	elif selection == 2:
		draw_NUMBER("7b")
	else:
		draw_NUMBER("7c")

#
# Draw '8'
#
def draw_8a(my_line_us):
	print('Drawing 8a')
	startX = 1600
	startY = 350
	radius = 400
	my_line_us.g01(startX,startY,1000)
	for i in range(0,361):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		if i == 270:
			for j in range(450,91,-1):
				radsLower = j * (3.14159 / 180)
				lowerX = radius * math.cos(radsLower)
				lowerY = radius * math.sin(radsLower)
				my_line_us.g01(startX - radius + currX + lowerX, startY + currY - radius + lowerY,500)
		my_line_us.g01(startX - radius + currX, startY + currY,500)
	my_line_us.g01(startX,startY+50,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_8b(my_line_us):
	print('Drawing 8b')
	draw_CIRCLE(1500,700,400)
	draw_CIRCLE(1500,-150,400)
	my_line_us.home()

def draw_8c(my_line_us):
	print('Drawing 8c')
	startX = 1600
	startY = 350
	radius = 400
	my_line_us.g01(startX,startY,1000)
	for i in range(0,-361,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		if i == -90:
			for j in range(90,451):
				radsLower = j * (3.14159 / 180)
				lowerX = radius * math.cos(radsLower)
				lowerY = radius * math.sin(radsLower)
				my_line_us.g01(startX - radius + currX + lowerX, startY + currY - radius + lowerY,500)
		my_line_us.g01(startX - radius + currX, startY + currY,500)
	my_line_us.g01(startX,startY+50,500)

def printEight():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("8a")
	elif selection == 2:
		draw_NUMBER("8b")
	else:
		draw_NUMBER("8c")


#
# Draw '9'
#
def draw_9a(my_line_us):
	print('Drawing 9a')
	draw_CIRCLE(1600,350,400)
	my_line_us.g01(1600,-700,500)
	my_line_us.g01(1600,-700,1000)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_9b(my_line_us):
	print('Drawing 9b')
	draw_CIRCLE(1600,350,400)
	my_line_us.g01(1600,-700,500)
	my_line_us.g01(1200,-900,500)
	my_line_us.home()

def draw_9c(my_line_us):
	print('Drawing 9c')
	my_line_us.g01(1600,800,1000)
	my_line_us.g01(1600,-700,500)
	draw_CIRCLE(1600,350,400)
	my_line_us.home()

def printNine():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("9a")
	elif selection == 2:
		draw_NUMBER("9b")
	else:
		draw_NUMBER("9c")


#
# Draw '0'
#
def draw_0a(my_line_us):
	print('Drawing 0a')
	startX = 1800
	startY = 0
	radius = 500
	my_line_us.g01(startX,startY,1000)
	for i in range(0,361):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		if startY + currY > 0:
			my_line_us.g01(startX - radius + currX, startY + currY + 100,500)
		else:
			my_line_us.g01(startX - radius + currX, startY + currY - 100,500)
	my_line_us.g01(startX,startY+50,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_0b(my_line_us):
	print('Drawing 0b')
	startX = 1800
	startY = 0
	radius = 500
	my_line_us.g01(startX,startY,1000)
	for i in range(0,361):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		if startY + currY > 0:
			my_line_us.g01(startX - radius + currX, startY + currY + 100,500)
		else:
			my_line_us.g01(startX - radius + currX, startY + currY - 100,500)
	my_line_us.g01(startX,startY+50,500)
	my_line_us.g01(startX - radius + (radius * math.cos(45*3.14159/180)), startY + (radius * math.sin(45*3.14159/180)) + 100, 1000)
	my_line_us.g01(startX - radius + (radius * math.cos(225*3.14159/180)),startY + (radius * math.sin(225*3.14159/180)) - 100,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def draw_0c(my_line_us):
	print('Drawing 0c')
	startX = 800
	startY = 0
	radius = 500
	my_line_us.g01(startX,startY,1000)
	for i in range(180,-181,-1):
		currRads = i * (3.14159 / 180)
		currX = radius * math.cos(currRads)
		currY = radius * math.sin(currRads)
		if startY + currY > 0:
			my_line_us.g01(startX + radius + currX, startY + currY + 100,500)
		else:
			my_line_us.g01(startX + radius + currX, startY + currY - 100,500)
	my_line_us.g01(startX,startY+50,500)
	# After each drawing, move back to the HOME position
	my_line_us.home()

def printZero():
	selection = random.randint(1,3)
	if selection == 1:
		draw_NUMBER("0a")
	elif selection == 2:
		draw_NUMBER("0b")
	else:
		draw_NUMBER("0c")


#
# Sequence and Number Selection for Various Testing
#
def draw_Sequence(inpt):
	for c in inpt:
		if c == "0":
			printZero()
		elif c == "1":
			printOne()
		elif c == "2":
			printTwo()
		elif c == "3":
			printThree()
		elif c == "4":
			printFour()
		elif c == "5":
			printFive()
		elif c == "6":
			printSix()
		elif c == "7":
			printSeven()
		elif c == "8":
			printEight()
		elif c == "9":
			printNine()

def draw_NUMBER(numToDraw):
	if numToDraw == "0a":
		draw_0a(my_line_us)
	elif numToDraw == "0b":
		draw_0b(my_line_us)
	elif numToDraw == "0c":
		draw_0c(my_line_us)
	elif numToDraw == "1a":
		draw_1a(my_line_us)
	elif numToDraw == "1b":
		draw_1b(my_line_us)
	elif numToDraw == "1c":
		draw_1c(my_line_us)
	elif numToDraw == "2a":
		draw_2a(my_line_us)
	elif numToDraw == "2b":
		draw_2b(my_line_us)
	elif numToDraw == "2c":
		draw_2c(my_line_us)
	elif numToDraw == "3a":
		draw_3a(my_line_us)
	elif numToDraw == "3b":
		draw_3b(my_line_us)
	elif numToDraw == "3c":
		draw_3c(my_line_us)
	elif numToDraw == "4a":
		draw_4a(my_line_us)
	elif numToDraw == "4b":
		draw_4b(my_line_us)
	elif numToDraw == "4c":
		draw_4c(my_line_us)
	elif numToDraw == "5a":
		draw_5a(my_line_us)
	elif numToDraw == "5b":
		draw_5b(my_line_us)
	elif numToDraw == "5c":
		draw_5c(my_line_us)
	elif numToDraw == "6a":
		draw_6a(my_line_us)
	elif numToDraw == "6b":
		draw_6b(my_line_us)
	elif numToDraw == "6c":
		draw_6c(my_line_us)
	elif numToDraw == "7a":
		draw_7a(my_line_us)
	elif numToDraw == "7b":
		draw_7b(my_line_us)
	elif numToDraw == "7c":
		draw_7c(my_line_us)
	elif numToDraw == "8a":
		draw_8a(my_line_us)
	elif numToDraw == "8b":
		draw_8b(my_line_us)
	elif numToDraw == "8c":
		draw_8c(my_line_us)
	elif numToDraw == "9a":
		draw_9a(my_line_us)
	elif numToDraw == "9b":
		draw_9b(my_line_us)
	elif numToDraw == "9c":
		draw_9c(my_line_us)
	else:
		print('WRONG INPUT NUMBER')

#
#  The Main Function starts here
#

print('Main function starts')

#my_line_us = LineUs('line-us.local')
my_line_us = LineUs('192.168.4.1') ## The address may change. Check the address if the connection failed
print(my_line_us.get_hello_string())
time.sleep(1)

numToDraw = "2c"
drawTimeMax = 1
currentDrawTime = 1
sleepTime = 1

#draw_Sequence("9088723170")

print('Draw number '+ str(numToDraw) + ', ' + str(drawTimeMax) + ' times')

while currentDrawTime <= drawTimeMax:
	#time.sleep(1)
	#Initiate the pen to the HOME position
	my_line_us.home()
	# Call the drawing function
	draw_NUMBER(numToDraw)
	# Delay sometime before the next drawing
	time.sleep(sleepTime)
	currentDrawTime += 1

print('Drawing finished!')

my_line_us.disconnect()

