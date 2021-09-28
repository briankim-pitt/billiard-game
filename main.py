#main classes that are shared across gamemodes


from tkinter import *
import math

##########################################
# classes
##########################################

class Ball(object):
	def __init__(self, cx, cy, speed = 0, angle = 0):
		self.cx = cx
		self.cy = cy
		self.speed = speed
		self.isMoving = False
		self.angle = math.pi/2
		self.isBouncing = False
		self.bounceType = None
		self.impactX = None
		self.impactY = None

	def setSpeed(self, amount):
		self.speed = amount

	def setAngle(self, angle):
		self.angle = angle

	def move(self):
		self.cx+= math.cos(self.angle)*self.speed
		self.cy+= math.sin(self.angle)*self.speed
		self.friction()

	def isBallCollision(self,data, other):
		x0 = self.cx
		y0 = self.cy
		x1 = other.cx
		y1 = other.cy
		distance = math.sqrt((x1-x0)**2+(y1-y0)**2)
		# use center points of the two balls and the distance between them
		# to check collision
		if data.mode == "mp" and data.firstCollision and distance <= data.r*2:
		# # # 	if isinstance(self, CueBall) and isinstance(other, FlatBall):
		# # # 		if data.turn == "Player 1":
		# # # 			if data.player1.ballType == "StripedBall":
		# # # 				data.player2.turns = 2
		# # # 			else:
		# # # 				data.player2.turns = 1
		# # # 		else:
		# # # 			if data.player2.ballType == "StripedBall":
		# # # 				data.player1.turns = 2
		# # # 			else:
		# # # 				data.player1.turns = 1
			data.firstCollision = False
		return distance <= data.r*2

	def bounce(self):
		# wall bounce physics
		self.speed /= 1.15
		if self.bounceType == "horizontal":	
			self.angle = -self.angle
		else:
			self.angle = -self.angle + math.pi

	def friction(self):
		self.speed -= 0.08
		if self.speed < 0:
			self.speed = 0
			self.isMoving = False

	def midpoint(self, center0, center1):
		x0, y0 = center0
		x1, y1 = center1
		#midpoint formula
		midX = (x0+x1)/2
		midY = (y0+y1)/2
		return (midX, midY)

	def angleOfImpact(self, impactPoint, cx, cy):
		# impactPoint is the midpoint between the center points of 
		# the two colliding balls
		x, y = impactPoint
		dx, dy = (x - cx), (y - cy)
		angle = math.atan2(dy,dx)
		self.angle = angle + math.pi
		
	def checkBoundary(self, data, cx, cy):
		r = data.r
		for boundary in data.boundaries:	
			if boundary.boundaryType == "x":
				if not cx-r>boundary.start:
					self.cx = data.margin + r
					# vertical walls and horizontal walls have different angle
					# deflection properties
					self.bounceType = "vertical"
					self.bounce()
				elif not cx+r<boundary.end:
					self.cx = data.margin + data.tableWidth - r
					self.bounceType = "vertical"
					self.bounce()
			else:
				if not cy-r>boundary.start:
					self.cy = data.margin + r
					self.bounceType = "horizontal"
					self.bounce()
				elif not cy+r<boundary.end:
					self.cy = data.margin + data.tableHeight - r
					self.bounceType = "horizontal"
					self.bounce()

	def onTimerFired(self, data):
		self.checkBoundary(data, self.cx, self.cy)
		if self.isMoving:
			self.move()
		if data.mode == "mp" and data.cueBall.speed == 0: 
			data.firstCollision = True
		for ball in data.balls:
			if not ball == self and self.isBallCollision(data,ball):
				# calls midpoint to get the impact point between the two balls
				impactPoint = ball.midpoint((ball.cx, ball.cy),(self.cx,self.cy))
				ball.angleOfImpact(impactPoint, ball.cx, ball.cy)
				#ball collision physics
				ball.speed = self.speed/1.1
				self.angleOfImpact(impactPoint, self.cx, self.cy)
				self.speed /= 1.3
				ball.isMoving = True

# ball type subclasses, only some are implemented for singleplayer
class CueBall(Ball):
	def __init__(self, cx, cy, speed = 0, angle = 0):
		super().__init__(cx, cy, speed, angle)
		self.ballImage = PhotoImage(file="./images/ballcue.png")

class EightBall(Ball):
	def __init__(self, cx, cy, number, speed = 0, angle = 0):
		super().__init__(cx, cy, speed, angle)
		self.number = number
		self.fileName = "./images/ball%02d.png"%(number)
		self.ballImage = PhotoImage(file=self.fileName)

class StripedBall(Ball):
	def __init__(self, cx, cy, number, speed = 0, angle = 0):
		super().__init__(cx, cy, speed, angle)
		self.number = number
		self.fileName = "./images/ball%02d.png"%(number)
		self.ballImage = PhotoImage(file=self.fileName)
		
class FlatBall(Ball):
	def __init__(self, cx, cy, number, speed = 0, angle = 0):
		super().__init__(cx, cy, speed, angle)
		self.number = number
		self.fileName = "./images/ball%02d.png"%(number)
		self.ballImage = PhotoImage(file=self.fileName)

class Boundary(object):
	def __init__(self, start, end, boundaryType):
		self.start = start
		self.end = end
		self.boundaryType = boundaryType

class Cue(object):
	def __init__(self, tip, angle, length = 400):
		self.angle = angle
		self.tip = tip
		self.tipX, self.tipY = self.tip
		self.length = length
		self.cueTipX = self.tipX+math.cos(self.angle)*35
		self.cueTipY = self.tipY+math.sin(self.angle)*35
		x,y = self.tip
		self.endX = x + math.cos(self.angle)*self.length
		self.endY = y + math.sin(self.angle)*self.length
		self.isPlaced = False

	def move(self, x, y):
		self.tip = (x,y)
		self.cueTipX = x+math.cos(self.angle)*35
		self.cueTipY = y+math.sin(self.angle)*35
		self.endX = x + math.cos(self.angle)*self.length
		self.endY = y + math.sin(self.angle)*self.length

	def place(self):
		self.isPlaced = True

	def changeAngle(self, side):
		if side == "Left":
			#rotate cue to the left or to the right
			self.angle += math.pi/40
		else: self.angle -= math.pi/40
		x,y = self.tip
		self.cueTipX = x+math.cos(self.angle)*35
		self.cueTipY = y+math.sin(self.angle)*35
		self.endX = x + math.cos(self.angle)*self.length
		self.endY = y + math.sin(self.angle)*self.length

	def draw(self, canvas, data):
		x0,y0 = self.cueTipX, self.cueTipY
		canvas.create_line(x0,y0,self.endX, self.endY, width=8, fill="#edb274")

	def onTimerFired(self, data):
		x0, y0 = self.cueTipX, self.cueTipY
		x1, y1 = data.cueBall.cx, data.cueBall.cy
		distance = math.sqrt((x1-x0)**2+(y1-y0)**2)
		if distance <= data.r and self.isPlaced:
			#check if cue tip hits the cue ball
			data.cueBall.angleOfImpact((self.cueTipX,self.cueTipY), x1, y1)
			#the angle the cue ball deflects uses the same principle of 
			#ball collisions, it uses the impact point between the 
			#cue tip and the ball instead
			data.cueBall.speed = data.slider.power
			data.cueBall.isMoving = True
			data.cue.isPlaced = False
			data.setTurn = False
			data.qBalls = len(data.balls)

class PowerBar(object):
	def __init__(self, width = 500, height = 50):
		self.width = width
		self.height = height
		self.power = 0

	def draw(self, canvas, data):
		x0,y0 = 250, data.margin+data.tableHeight+data.wallWidth+10
		x1, y1 = x0 + self.width, y0 + self.height
		if 13 < data.slider.power < 15:
			color = "#e8ffd1"
		elif 15< data.slider.power < 20:
			color = "#ffffd1"
		elif 20<data.slider.power < 25:
			color = "#ffead1"
		elif 25<data.slider.power <= 35:
			color = "#ffd7d1"
		else: color = "#c0cde2"
		canvas.create_rectangle(x0,y0,x1,y1, fill = color)

class Slider(object):
	def __init__(self):
		self.sliderWidth = 70
		self.sliderHeight = 50
		self.sliderCX = 745
		self.sliderCY = 565
		self.power = 0
		self.multiplier = 35

	def drawSlider(self, canvas, data):
		width = self.sliderWidth
		height = self.sliderHeight
		x0, y0 = self.sliderCX - width//2, self.sliderCY - height//2
		x1, y1 = self.sliderCX + width//2, self.sliderCY + height//2
		canvas.create_rectangle(x0, y0, x1, y1, fill= "#e84a27")

	def reset(self):
		self.sliderCX = 720
		self.sliderCY = 565
		self.power = 0

	def clickInSlider(self, x, y):
		width = self.sliderWidth
		height = self.sliderHeight
		x0, y0 = self.sliderCX - width//2, self.sliderCY - height//2
		x1, y1 = self.sliderCX + width//2, self.sliderCY + height//2
		return x0<x<x1 and y0<y<y1

	def drag(self, data):
		#changes the x value of the slider depending on 
		#how far you drag the slider
		x0 = data.startX
		x1 = data.dragX
		boundLeft = 255
		boundRight = 755
		if boundLeft<self.sliderCX<boundRight and x0 - x1 > 0:
			self.sliderCX = x0 - x1
			self.power = self.multiplier*(254/(x0-x1))

class Hole(object):
	def __init__(self, cx, cy, r = 22):
		self.cx = cx
		self.cy = cy
		self.color = "gray8"
		self.r = r

	def onTimerFired(self, data):
		for ball in data.balls:
			x0, y0 = ball.cx, ball.cy
			x1, y1 = self.cx, self.cy
			distance = math.sqrt((x1-x0)**2+(y1-y0)**2)
			if distance <= self.r:
				data.balls.remove(ball)
				if data.mode == "sp":
					data.score += 1
				else:
					if data.hasScored == False:
						data.hasScored = True
						if isinstance(ball, FlatBall):
							data.player1.ballType = "Flat"
							data.player2.ballType = "Striped"
						elif isinstance(ball, StripedBall):
							data.player1.ballType = "Striped"
							data.player2.ballType = "Flat"
					if isinstance(ball, EightBall):
						if data.player1.hasScoredAll:
							if data.turn == "Player 1":
								data.winner = "Player 1"
							else:
								data.winner = "Player 2"
						elif data.player2.hasScoredAll:
							if data.turn == "Player 2":
								data.winner = "Player 2"
							else:
								data.winner = "Player 1"
						else:
							if data.turn == "Player 1":
								data.winner = "Player 2"
							else: data.winner = "Player 1"
						data.gameOver = True
					if isinstance(ball, FlatBall):
						if data.turn == "Player 1":
							if data.player1.ballType == "Flat":
								data.scored = True
							else: data.scored = False
						else:
							if data.player2.ballType == "Flat":
								data.scored = True
							else:data.scored = False
					elif isinstance(ball, StripedBall):
						if data.turn == "Player 1":
							if data.player1.ballType == "Striped":
								data.scored = True
							else: data.scored = False
						else:
							if data.player2.ballType == "Striped":
								data.scored = True
							else:data.scored = False
		x0, y0 = data.cueBall.cx, data.cueBall.cy
		x1, y1 = self.cx, self.cy	
		distance = math.sqrt((x1-x0)**2+(y1-y0)**2)
		if distance <= self.r:		
			data.cueBall.speed = 0
			data.cueBall.cx, data.cueBall.cy = 300, data.height//2

