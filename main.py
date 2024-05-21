from tkinter import *
from random import *
from tkinter import messagebox
import tkinter.font as tkFont
import pygame
import pyglet,tkinter

class Case:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = "right"

    def displayCase(self):
        global canvas

        canvas.create_image(self.x*50 , self.y*50 , image = imageSnake["case"] , anchor ='nw')

    def updatePosition(self):
        if self.direction == "right":
            if self.x != 16:
                self.x = self.x + 1
            else:
                self.x = 0
        if self.direction == "left":
            if self.x != 0:
                self.x = self.x - 1
            else:
                self.x = 16
        if self.direction == "down":
            if self.y != 12:
                self.y = self.y + 1
            else:
                self.y = 0
        if self.direction == "up":
            if self.y != 0:
                self.y = self.y - 1
            else:
                self.y = 12
class Snake:

    def __init__(self):
        self.lst_case = [Case(x,3) for x in range(3,0,-1)]
        self.head = self.lst_case[0]
        self.tail = self.lst_case[len(self.lst_case)-1]
        self.alive = True
    def addCase(self):
        #last_case = self.lst_case[len(self.lst_case)-1]

        if self.tail.direction == "left":
            newCase = Case(self.tail.x+1, self.tail.y )
            newCase.direction = self.tail.direction
            self.lst_case.append(newCase)

        if self.tail.direction == "up":
            newCase = Case(self.tail.x,self.tail.y+1)
            newCase.direction = self.tail.direction
            self.lst_case.append(newCase)

        if self.tail.direction == "right":
            newCase = Case(self.tail.x-1, self.tail.y)
            newCase.direction = self.tail.direction
            self.lst_case.append(newCase)

        if self.tail.direction == "down":
            newCase = Case(self.tail.x,self.tail.y-1)
            newCase.direction = self.tail.direction
            self.lst_case.append(newCase)

        self.tail = self.lst_case[len(self.lst_case)-1]


    def displaySnake(self):

        for case in self.lst_case:
            if case == self.head:
                #canvas.create_rectangle(case.x * 50, case.y * 50, (case.x + 1) * 50, (case.y + 1) * 50,
                 #fill="red")
                canvas.create_image(case.x*50 , case.y*50 , image = imageSnake["head_"+case.direction] , anchor ='nw')
            else:
                case.displayCase()
    """
    def changeDirection(self,event):

        if self.head.direction == "left" or self.head.direction == "right":

            if event.keycode == 38:
                self.head.direction = "up"
            if event.keycode == 40:
                self.head.direction = "down"
        elif self.head.direction == "up" or self.head.direction == "down":
            if event.keycode == 37:
                self.head.direction = "left"

            if event.keycode == 39:
                self.head.direction = "right"
    """

    def updateSnake(self):

        for case in self.lst_case:
            case.updatePosition()
        for i in range(len(self.lst_case)-1,0,-1):

            self.lst_case[i].direction = self.lst_case[i-1].direction

class Apple:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def displayApple(self):
        global canvas

        canvas.create_image(self.x*50 ,self.y*50 , image = imageApple , anchor = "nw")

grille = [[0 for i in range(17)] for j in range(13)]

def afficheGrille():
    for y in range(len(grille)):
        for x in range(len(grille[y])):
            canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill='white')


def updateApple():
    global apple
    global snake
    global score
    if apple.x == snake.head.x and apple.y == snake.head.y:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/eatApple.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=0)
        apple = Apple(randint(0,16),randint(0,12))
        snake.addCase()
        score += 1
        print(score)
        #displayScore = Label(window, text=str(score))

def changeDirection(event):
    global snake
    if snake.head.direction == "left" or snake.head.direction == "right":
        if event.keycode == 25:
            snake.head.direction = "up"
        if event.keycode == 39:
            snake.head.direction = "down"

    elif snake.head.direction == "up" or snake.head.direction == "down":
        if event.keycode == 38:
            snake.head.direction = "left"
        if event.keycode == 40:
            snake.head.direction = "right"
    snake.displaySnake()
    apple.displayApple()
def checkHeadPosition():
    global snake
    global canvas
    for i in range(1,len(snake.lst_case)-1):
        if snake.head.x == snake.lst_case[i].x and snake.head.y == snake.lst_case[i].y:
            snake.alive = False

def update():
    global snake
    global apple
    global score
    snake.updateSnake()
    updateApple()
    checkHeadPosition()
    if snake.alive:
        canvas.delete("all")
        snake.displaySnake()
        apple.displayApple()
        displayScore = canvas.create_text(50, 50, text=str(score), fill="white",font=tkFont.Font(family='Retro Gaming', size=36, weight='bold'))
        window.after(100, update)
    else:
        MsgBox = messagebox.askquestion('PERDU :(', 'VOUS AVEZ PERDU ! \n VOULEZ VOUS REJOUER ?', icon="error")
        if MsgBox == 'yes':
            score = 3
            canvas.delete('all')
            snake = Snake()
            apple = Apple(randint(1,16),randint(1,12))
            window.after(100, update)
        else :
            window.destroy()

pyglet.font.add_file('assets/Retro Gaming.ttf')
score = 3
window = Tk()
window.geometry(str(17*50)+"x"+str(13*50))
window.resizable(False,False)
window.title("𝙎𝙣𝙖𝙠𝙚 !")
canvas = Canvas(window, width =17*50 , height = 13*50 ,borderwidth = 0, highlightthickness = 0, bg = "black")
canvas.grid(column=0,row=0)
canvas.create_text(50 , 50, text= str(score) , fill="black" , font= tkFont.Font(family='Retro Gaming', size=36, weight='bold'))

imageSnake = {
    "head_down" : PhotoImage(file="assets/snake_head_down.png"),
    "head_up" :PhotoImage(file="assets/snake_head_up.png"),
    "head_right" :PhotoImage(file="assets/snake_head_right.png"),
    "head_left" :PhotoImage(file="assets/snake_head_left.png"),
    "case" : PhotoImage(file="assets/snake_case.png")
}

snake = Snake()
snake.displaySnake()
imageApple = PhotoImage(file="assets/apple.png")
apple = Apple(randint(1,16),randint(1,12))
apple.displayApple()
window.bind("<Any-KeyPress>",changeDirection)
window.after(100,update)
window.mainloop()
