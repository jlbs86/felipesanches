RED=0
GREEN=1
YELLOW=2
BLUE=3
PURPLE=4
PINK=5
ORANGE=6
import random

class Board:
	def __init__(self):
		self.config={"repeat_colors":False, "num_colors":6}
		self.secret = None
		self.clean()

	def clean(self):
		self.lines = []
#		for _ in range(10):
#			self.lines.append(new Line())
		self.currentLine = 0

	def newGame(self, secret=None):
		self.clean()
		if secret:
			self.secret = secret
		else:
			self.randomGame()

	def randomGame(self):
		self.secret=[]
		for i in range(4):
			color = random.randint(0,6)
			if not self.config["repeat_colors"]:
				while color in self.secret:
					color = random.randint(0,6)
			self.secret.append(color)

	def guess(self, g):
		correct=0
		misplaced=0
		for i in range(4):
			if self.secret[i]==g[i]:
				correct+=1
			elif g[i] in self.secret:
				misplaced+=1
		if correct == 4:
			return True
		return correct, misplaced

b = Board()
b.newGame([RED, GREEN, BLUE, ORANGE])
assert(b.guess([RED,BLUE,PINK,PURPLE])==(1,1))
assert(b.guess([RED, GREEN, BLUE, ORANGE])==True)

