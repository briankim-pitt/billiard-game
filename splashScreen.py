#creates splash screen where player can select the different gamemodes

from tkinter import *
from mode import singleplayer
from mode import newMultiplayer


#to solve the image crash problem for singleplayer and multiplayer, I used the Toplevel() method from: 
#https://stackoverflow.com/questions/35434654/closing-current-window-when-opening-another-window?rq=1
def button1Pressed():
    root2 = Toplevel()
    singleplayer.run(root2)

def button2Pressed():
    root2 = Toplevel()
    newMultiplayer.run(root2)
    
def inButton1(x,y):
    return 66<x<234 and 105<y<145

def inButton2(x,y):
    return 66<x<234 and 155<y<195


    
    

####################################
# run function from http://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
####################################

def init(data):
    # load data.xyz as appropriate
    data.spImage = PhotoImage(file="./images/singleplayer.png")
    data.mpImage = PhotoImage(file="./images/multiplayer.png")

def mousePressed(event, data):
    # use event.x and event.y
    if inButton1(event.x, event.y):
        button1Pressed()
    elif inButton2(event.x, event.y):
        button2Pressed()

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(-1,-1,data.width,data.height, fill="#e5d5b5")
    # draw in canvas
    canvas.create_image(150,125,image=data.spImage)
    canvas.create_image(150,175,image=data.mpImage)
    canvas.create_text(150, 40, anchor = "n", text = "Pool", font="Helvetica 42 bold")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(300, 300)
