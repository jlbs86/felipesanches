import math
BACKGROUND_COLOUR = (0.53, 0.63, 0.75)
BORDER_COLOUR = (0.808, 0.361, 0.0)

PIECE_COLOUR         = (0.0, 0.0, 0.0)
HOLE_COLOUR = (0.8, 0.8, 0.8)

hint_colors = [
(0.0, 0.0, 0.0), #BLACK=0
(1.0, 1.0, 1.0), #WHITE=0
]

colors = [
(1.0, 0.0, 0.0), #RED=0
(0.0, 1.0, 0.0), #GREEN=1
(1.0, 1.0, 0.0), #YELLOW=2
(0.0, 0.0, 1.0), #BLUE=3
(0.6, 0.0, 0.6), #PURPLE=4
(1.0, 0.2, 1.0), #PINK=5
(1.0, 0.5, 0.0), #ORANGE=6
]

from senha import Board
class Scene():
	BORDER = 6.0
	PIECE_BORDER = 2.0

	def __init__(self, viewWidget):
		"""Constructor for a Cairo scene"""
		self.viewWidget        = viewWidget
		self.pieces          = []
		self.redrawStatic    = True
		self.showNumbering   = False
		self.currentColor		 = None
		self.currentRow		 = 0
		self.guesses = [[None,None,None,None]]
		self.hints = []
		self.game = Board()
		self.game.newGame()
		print "the secret:", self.game.secret
		self.secret = self.game.secret
		self.game_over=False

	def nextRow(self):
		if self.currentRow == 9:
			self.game_over=True
			return #TODO game over FAIL

		#print "self.guesses[self.currentRow]: ", self.guesses[self.currentRow]
		hints = self.game.guess(self.guesses[self.currentRow])
		if hints==True:
			self.game_over=True
			self.hints.append([0,0,0,0])
			#TODO: game over WINNER
		else:
			h=[]
			for _ in range(hints[0]):
				h.append(0)
			for _ in range(hints[1]):
				h.append(1)
			#print "h:",h
			self.hints.append(h)
			self.currentRow+=1
			self.guesses.append([None,None,None,None])

	def addPiece(self, color, position, row):
		"""Add a piece model into the scene.

		Returns a reference to this piece or raises an exception.
		"""

		if color in [BLACK, WHITE]:
			piece = ColorPiece(self, color, position, row)
		else:
			piece = HintPiece(self, color, position, row)

		self.pieces.append(piece)
		
		# Redraw the scene
		self.redrawStatic = True
		self.viewWidget.redraw()

		return piece

	def reshape(self, width, height):
		"""Resize the viewport into the scene.

		'width' is the width of the viewport in pixels.
		'height' is the width of the viewport in pixels.
		"""
		self.width = width
		self.height = height

		# Make the squares as large as possible while still pixel aligned
		shortEdge = min(self.width, self.height)
		self.squareSize = math.floor((shortEdge - 2.0*self.BORDER) / 9.0)
		self.pieceSize = self.squareSize - 2.0*self.PIECE_BORDER

		boardHeight = shortEdge
		boardWidth = shortEdge/2.0
		PERCENTAGE=0.7 #TODO
		self.padding = boardWidth/15.0

		self.hole_spacing = (boardWidth*PERCENTAGE - 2.0*self.padding) / 4.0
		self.hint_spacing = (boardWidth*(1.0-PERCENTAGE) - 2.0*self.padding) / 2.0
		self.row_spacing = (boardHeight - 2.0*self.padding) / (10.0 + 1 + 1)

		self.piece_radius=self.hole_spacing*0.4
		self.hint_radius=self.piece_radius*0.5

		self.hole_radius=self.piece_radius*0.3
		self.minihole_radius=self.hole_radius*0.5

		self.redrawStatic = True
		self.viewWidget.redraw()

	#Just in case we might want to render these differently...
	def render_secret_piece(self, context, x, y, c):
		self.render_guess_piece(context, x, y, c)

	def render_guess_piece(self, context, x, y, c):
		context.set_source_rgb(*colors[c])
		context.arc(x, y, self.piece_radius,0,2*3.1415)
		context.fill()

		context.set_line_width(2)
		context.set_source_rgb(0,0,0)
		context.arc(x, y, self.piece_radius,0,2*3.1415)
		context.stroke()

	def render_guess_hole(self, context, x, y):
		context.set_source_rgb(*HOLE_COLOUR)
		context.arc(x, y, self.hole_radius,0,2*3.1415)
		context.fill()

	def render_hint_piece(self, context, x, y, c):
		context.set_source_rgb(*hint_colors[c])
		context.arc(x, y, self.hint_radius,0,2*3.1415)
		context.fill()

	def render_hint_hole(self, context, x, y):
		context.set_source_rgb(*HOLE_COLOUR)
		context.arc(x, y, self.minihole_radius,0,2*3.1415)
		context.fill()

	def render_color_picker(self, context):
		x = self.colorpicker_x(0)
		y = self.colorpicker_y(0)
		y2 = self.colorpicker_y(6)
		context.set_source_rgb(0,0,0)
		context.rectangle(x-1.3*self.piece_radius, y-1.3*self.piece_radius, 2.6*self.piece_radius,y2+1.3*self.piece_radius)
		context.fill()

		for c in xrange(7):
			x = self.colorpicker_x(c)
			y = self.colorpicker_y(c)

			context.set_source_rgb(*colors[c])
			context.rectangle(x-self.piece_radius, y-self.piece_radius, 2*self.piece_radius,2*self.piece_radius)
			context.fill()

	def renderStatic(self, context):
		"""Render the static elements in a scene.
		"""
		if self.redrawStatic is False:
				return False
		self.redrawStatic = False

		context.save()

		# Clear background
		context.set_source_rgb(*BACKGROUND_COLOUR)
		context.paint()
				    
		# Draw border
		context.set_source_rgb(*BORDER_COLOUR)
		borderSize = math.ceil(self.squareSize * 9)

		context.rectangle(self.BORDER, self.BORDER, borderSize/2, borderSize)
		context.fill()

		if self.game_over:
			for i in xrange(4):
				x,y = self.secret_x(i), self.secret_y(i)
				c=self.secret[i]
				self.render_secret_piece(context, x,y,c)

		# Draw color picker:
		self.render_color_picker(context)
			
		# Draw guess rows
		for row in xrange(10):
			for i in xrange(4):
				x = self.guess_x(row,i)
				y = self.row_y(row)

				if len(self.guesses)>row and self.guesses[row][i] != None:
					c = self.guesses[row][i]
					self.render_guess_piece(context, x,y,c)

				else:
					self.render_guess_hole(context, x,y)

		# Draw hints
			for i in xrange(4):
				x = self.hint_x(row,i) 
				y = self.hint_y(row,i)

				if len(self.hints)>row and i<len(self.hints[row]):
					c = self.hints[row][i]
					self.render_hint_piece(context, x,y,c)
				else:
					self.render_hint_hole(context, x,y)

		context.restore()
		return True

	def renderDynamic(self, context):
		"""Render the dynamic elements in a scene.

		This requires a Cairo context.
		"""
		pass

	def mouse_down(self, x, y):
		piece = self.getPiece(x,y)
		self.currentColor = None
		if piece[0] == "pick":
			self.currentColor = piece[1]
			#print "selected color: ", self.currentColor
		#print "from: ", piece

	def mouse_up(self, x, y):
		piece = self.getPiece(x,y)
		#print "to: ", piece
		#print "guesses:", self.guesses
		#print "currentRow:",self.currentRow
		if piece[0] == "guess" and piece[2] == self.currentRow:
			self.guesses[self.currentRow][piece[1]] = self.currentColor
			if not None in self.guesses[self.currentRow]:
				self.nextRow()
			# Redraw the scene
			self.redrawStatic = True
			self.viewWidget.redraw()


	def colorpicker_x(self, c):
		return 4*self.BORDER + 4*self.padding + 4*self.hole_spacing + 2*self.hint_spacing

	def colorpicker_y(self, c):
		return 2*self.BORDER + self.piece_radius + c*self.hole_spacing

	def secret_x(self, i):
		return self.BORDER + self.padding + (i+0.5) * self.hole_spacing

	def secret_y(self, i):
		return self.BORDER + self.padding + (0.5) * self.row_spacing

	def row_y(self, r):
		return self.BORDER + self.padding + (r+2.5) * self.row_spacing

	def hint_x(self, row,i):
		return self.BORDER + 3*self.padding + 4 * self.hole_spacing + (i%2+0.5) * self.hint_spacing

	def hint_y(self, row,i):
		return self.row_y(row) + (i/2-0.5) * self.hint_spacing

	def guess_x(self, row,i):
		return self.BORDER + self.padding + (i+0.5) * self.hole_spacing

	def getPiece(self, x, y):
		"""Find the slot at a given 2D location.

		'x' is the number of pixels from the left of the scene to select.
		'y' is the number of pixels from the bottom of the scene to select.
		"""

		for c in xrange(7):
			x_min = self.colorpicker_x(c)-self.piece_radius
			y_min = self.colorpicker_y(c)-self.piece_radius
			x_max = x_min + 2*self.piece_radius
			y_max = y_min + 2*self.piece_radius
			if x>x_min and x<=x_max and y>y_min and y<=y_max:
				return "pick", c
	
		selected_row=None
		for row in xrange(10):
			y_row_min = self.row_y(row) - 0.5*self.row_spacing
			y_row_max = y_row_min + self.row_spacing
			if y > y_row_min and y<=y_row_max:
				selected_row=row

		if selected_row==None:
			return None

		for i in xrange(4):
			x_min = self.guess_x(selected_row, i) - 0.5*self.hole_spacing
			x_max = x_min + self.hole_spacing
			if x>x_min and x<=x_max:
				return "guess", i,selected_row

			x_min = self.hint_x(selected_row, i) - 0.5*self.hint_spacing
			x_max = x_min + self.hint_spacing

			y_min = self.hint_y(selected_row,i) - 0.5*self.hint_spacing
			y_max = y_min + self.hint_spacing

			if x>x_min and x<=x_max and y>y_min and y<=y_max:
				return "hint", i,selected_row

