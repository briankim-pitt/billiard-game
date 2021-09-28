
from tkinter import *
import random
from main import *
from powerUps import *

def init(data):
	data.mode = "sp"
	file = open("Highscore.txt", "r")
	data.highscore = eval(file.read())
	file.close()
	data.powerUpColor = None
	data.currPowerUpName = "None"
	data.randomPower = random.choice([TimeBonus,DoublePower,EasyScoring,
		TimeLost,HalfPower,HardScoring])
	data.currPowerUp = data.randomPower
	data.powerUpTimer = 0
	data.start = False
	data.timer = 120
	data.score = 0
	data.startX = 0
	data.startY = 0
	data.dragX = 0
	data.dragY = 0
	data.isReleased = False
	data.isDragging = False
	data.slider = Slider()
	data.powerBar = PowerBar()
	data.cueBall = CueBall(300, data.height//2)
	data.cue = Cue((200,100), math.pi) 
	data.balls = []
	data.holes = []
	data.boundaries = []
	data.r = 15
	data.margin = 100
	data.tableWidth = 800
	data.tableHeight = 400
	data.wallWidth = 30
	startTable(data)

def startTable(data):
	wall = data.wallWidth
	margin = data.margin
	width = data.tableWidth
	height = data.tableHeight
	data.boundaries.append(Boundary(margin, margin + width, "x"))
	data.boundaries.append(Boundary(margin, margin + height, "y"))
	data.holes.append(Hole(margin, margin)) # top left
	data.holes.append(Hole(margin+width, margin)) #top right
	data.holes.append(Hole(margin, margin+height)) #bottom left
	data.holes.append(Hole(margin+width//2, margin)) #top mid
	data.holes.append(Hole(margin+width//2, margin+height)) #bottom mid
	data.holes.append(Hole(margin+width, margin+height)) #bottom right
	data.balls.append(FlatBall(600, data.height//2, 1))
	data.balls.append(StripedBall(628, data.height//2-16, 9))
	data.balls.append(FlatBall(628, data.height//2+16, 2))
	data.balls.append(StripedBall(656, data.height//2-32, 10))
	data.balls.append(EightBall(656, data.height//2, 8))
	data.balls.append(FlatBall(656, data.height//2+32, 3))
	data.balls.append(StripedBall(684, data.height//2-48, 11))
	data.balls.append(FlatBall(684, data.height//2-16, 7))
	data.balls.append(StripedBall(684, data.height//2+16, 14))
	data.balls.append(FlatBall(684, data.height//2+48, 4))
	data.balls.append(FlatBall(712, data.height//2-64, 5))
	data.balls.append(StripedBall(712, data.height//2-32, 13))
	data.balls.append(StripedBall(712, data.height//2, 15))
	data.balls.append(FlatBall(712, data.height//2+32, 6))
	data.balls.append(StripedBall(712, data.height//2+64, 12))

def drawTable(canvas, data):
	wallWidth = data.wallWidth
	margin = data.margin
	width = data.tableWidth
	height = data.tableHeight
	color = "#3d362b"
	canvas.create_rectangle(margin, margin, width+margin, 
		height+margin, fill="#1c1c1c")
	
	canvas.create_rectangle(margin-wallWidth, margin-wallWidth, margin+width+wallWidth, 
										margin, fill=color)
	canvas.create_rectangle(margin-wallWidth, margin+height, 
						margin+width+wallWidth, margin+height+wallWidth,fill=color)
	canvas.create_rectangle(margin-wallWidth, margin-wallWidth, margin, 
										margin+height+wallWidth, fill=color)
	canvas.create_rectangle(margin+width, margin-wallWidth, margin+width+wallWidth, 
										margin+height+wallWidth, fill=color)
	for hole in data.holes:
		r = hole.r
		x0,y0 = hole.cx-r, hole.cy-r
		x1,y1 = hole.cx+r, hole.cy+r
		canvas.create_oval(x0,y0,x1,y1, fill = hole.color)

def mousePressed(event, data):
	data.startX, data.startY = event.x, event.y
	x0,y0 = event.x, event.y
	x1, y1 = data.cueBall.cx, data.cueBall.cy
	distance = math.sqrt((x1-x0)**2+(y1-y0)**2)
	if data.cueBall.speed == 0 and distance <= data.r:
		data.cue.place()

#mouseMotion,leftReleased and leftMoved taken from previous 15-112 classes notes
#http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-tkinter-demos.html

def mouseMotion(event, data):
	#deals with moving the cue around the table
	data.cue.tip = (event.x, event.y)
	if not data.cue.isPlaced:
		data.cue.move(event.x, event.y)

def leftReleased(event, data):
	#deals with hitting cue ball
	data.isDragging = False
	if data.slider.clickInSlider(event.x, event.y) and data.cue.isPlaced:
		x = data.cueBall.cx+math.cos(math.pi+data.cue.angle)*(data.r+8)
		y = data.cueBall.cy+math.sin(math.pi+data.cue.angle)*(data.r+8)
		data.cue.move(x, y)

def drawTimer(canvas, data):
	r = 25
	increment = (math.pi*2)/370
	angle = 3*math.pi/2+(increment*data.powerUpTimer)
	endX = 955+(math.cos(angle)*r)
	endY = 565+(math.sin(angle)*r)
	canvas.create_line(955, 565, endX, endY, width=2, fill = "red")
	canvas.create_line(955, 565, 955, 565-r, width = 2)
	canvas.create_oval(955-r,565-r,955+r,565+r, width = 3)

def leftMoved(event, data):
	#deals with slider dragging
	data.startX = event.x
	data.startY = event.y
	if not data.isDragging and data.slider.clickInSlider(event.x, event.y):
		data.isDragging = True
	if data.isDragging:
		data.slider.drag(data)

def keyPressed(event, data):
	cueBall = data.balls[0]
	if event.keysym == "Left":
		if not data.cue.isPlaced:
			data.cue.changeAngle("Left")
	elif event.keysym == "Right":
		if not data.cue.isPlaced:
			data.cue.changeAngle("Right")
	elif event.char == " ":
		data.cue.isPlaced = False
	elif event.char == "r":
		init(data)


def timerFired(data):
	data.powerUpTimer += 1
	if data.powerUpTimer == 370:
		data.powerUpTimer = 0
		if not data.start:
			data.currPowerUp(data)
		else:
			data.currPowerUp(data)
			data.randomPower = random.choice([TimeBonus,DoublePower,EasyScoring,
		TimeLost,HalfPower,HardScoring])
			data.currPowerUp = data.randomPower
	data.timer -= 0.037
	data.timerDelay = 20
	data.cueBall.onTimerFired(data)
	for ball in data.balls:
		ball.onTimerFired(data)
	for hole in data.holes:
		hole.onTimerFired(data)
	data.cue.onTimerFired(data)
	if not data.isDragging:
		data.slider.reset()
	if data.timer <= 0:
		if data.highscore < data.score:
			file = open("Highscore.txt", "w")
			file.write(str(data.score))
			file.close()



def redrawAll(canvas, data):
	if 120 > data.timer > 0:
		canvas.create_rectangle(0,0,data.width,data.height, fill="#e5d5b5")
		drawTable(canvas, data)
		data.powerBar.draw(canvas, data)
		# x0,y0 = data.cueBall.cx-data.r, data.cueBall.cy-data.r
		# x1,y1 = data.cueBall.cx + data.r, data.cueBall.cy + data.r
		# canvas.create_oval(x0,y0,x1,y1, fill = data.cueBall.color)
		canvas.create_image(data.cueBall.cx, data.cueBall.cy, 
			image = data.cueBall.ballImage)
		for ball in data.balls:
			# x0,y0 = ball.cx-data.r, ball.cy-data.r
			# x1,y1 = ball.cx + data.r, ball.cy + data.r
			# canvas.create_oval(x0,y0,x1,y1, fill = ball.color)
			canvas.create_image(ball.cx,ball.cy,image=ball.ballImage)
		data.slider.drawSlider(canvas, data)
		data.cue.draw(canvas, data)
		canvas.create_text(10, 10, anchor ="nw", font = "Helvetica 16 bold", 
			text="Score = %d"%data.score)
		canvas.create_text(10, data.height-25, anchor ="sw", font = "Helvetica 16 bold", 
			text="Power Up = %s"%(data.currPowerUpName), fill = data.powerUpColor)
		canvas.create_text(data.width-80, data.height-25, anchor ="se", 
			font = "Helvetica 16 bold", text="Next Power Up in:")
		drawTimer(canvas,data)
		canvas.create_text(10, 40, anchor ="nw", font = "Helvetica 16 bold", 
			text="Highscore = %d"%(data.highscore))
		if data.timer > 10: color = "black"
		else: color = "red"
		canvas.create_text(data.width-10, 10, anchor = "ne", 
			font = "Helvetica 16 bold", text = "Time left: %d"%data.timer,
			fill = color)
		if data.cueBall.speed == 0 and not data.cue.isPlaced:
			canvas.create_text(data.width//2,data.margin//2,font=\
				"Helvetica 16 bold",
			text = "Change cue angle using left/right arrow keys, then rest the " +
			"cue by clicking the cue ball")
		elif data.cueBall.speed == 0 and data.cue.isPlaced:
			canvas.create_text(data.width//2,data.margin//2, font = "Helvetica 16\
			bold", text = "Drag the slider to hit the ball. " + 
			"The more you drag the slider, the more power you hit the ball with.\n"+
			"		Press spacebar to unrest the cue")
	else:
		canvas.create_text(data.width//2, data.height//2, font = "Helvetica 24\
			bold", text = "Game Over! Your score was: %d \n"%data.score +
				"	Press r to restart")
##########################################
# run function from class notes: 
# http://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
# and http://www.kosbie.net/cmu/fall-15/15-112/notes/notes-tkinter-demos.html
##########################################

def run(root, width=1000, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()
    def mouseWrapper(mouseFn, event, canvas, data):
        if data.mouseWrapperMutex: return
        data.mouseWrapperMutex = True
        mouseFn(event, data)
        redrawAllWrapper(canvas, data)
        data.mouseWrapperMutex = False

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def mouseMotionWrapper(event, canvas, data):
    	mouseMotion(event, data)
    	redrawAllWrapper(canvas, data)

    def leftMouseReleasedWrapper(event, canvas, data):
    	leftMouseReleased(event, data)
    	redrawAllWrapper(canvas, data)

    def leftMouseMovedWrapper(event, canvas, data):
    	leftMouseMoved(event, data)
    	redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.mouseWrapperMutex = False
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # root2 = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    canvas.bind("<Motion>", lambda event:
                            mouseWrapper(mouseMotion, event, canvas, data))
    canvas.bind("<B1-ButtonRelease>", lambda event:
    						mouseWrapper(leftReleased, event, canvas, data))
    canvas.bind("<B1-Motion>", lambda event:
    						mouseWrapper(leftMoved, event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run()