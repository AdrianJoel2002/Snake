#IMPORTS
import math 
import random                                                               #For the random placement of the Food
import pygame                                                               #Program for the 
import tkinter as tk                                                        #Message box once the game is over
from tkinter import messagebox

#INPUTS AND CHOICES
Choice = int(input('''                              
        Welcome to my Snake Game
          made by Adrian Jaspa

Please choose the size of you game:
1.)10x10 GRID - Quick Game
2.)20x20 GRID - Normal Game
3.)35x35 GRID - Long Game

Choice(1/2/3): '''))                                                        #A quick instroduction whether the person specifically want a cerain size of a Grid

name = input("Please Type in your name: ")                                  #Name to be put in the Leaderboards.

                                                                            #Choices to Specify what Grid they have played.
if Choice == 1:
    des = "15x15"
elif Choice == 2:
    des = "20x20"
elif Choice == 3:
    des = "35x35"
    
#CREATING THE TEXTURES
class cubes(object):                                                        #Changes the Grid Size
    if Choice == 1:                                                         #If Choice is equal to the chosen number:
        x = 15                                                              #Amount of rows will be x
        y = 390                                                             #The size of the Screen will be y
        des = "15x15"
    elif Choice == 2:
        x = 20
        y = 500
        des = "20x20"
    elif Choice == 3:
        x = 35
        y = 700
        des = "35X35"
        
    row = x                                                                 #Rows in the program.
    w = y                                                                   #The size of the Program
    def __init__(player,start,dirnx=1,dirny=0,color=(15,56,15)):
        player.pos = start                                                  #Init programs the player's bocy by cubes.
        player.dirnx = 1                            
        player.dirny = 0
        player.color = color
 
    def step(player, dirnx, dirny):                                         #Step determines the player's location
        player.dirnx = dirnx
        player.dirny = dirny
        player.pos = (player.pos[0] + player.dirnx, player.pos[1] + player.dirny)
 
    def draw(player, surface, eyes=False):                                  #The placement of the player
        dis = player.w // player.row
        i = player.pos[0]
        j = player.pos[1]
 
        pygame.draw.rect(surface, player.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:                                                            #Draws eyes in cubes to make the snake more realistic.
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)                    #This accurately determine where the eyes go the same way when the snake moves.
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)                #Same but move a little bit more
            pygame.draw.circle(surface, (155,188,15), circleMiddle, radius) #Color and Location of the Eyes
            pygame.draw.circle(surface, (155,188,15), circleMiddle2, radius)# Color and Location of the other eye

#CREATING THE PLAYER
class character(object):                                                    #The properties of the Player
    body = []                                                               #This will be the cubes that the player will get
    turns = {}                                                              #Turns will be put here
    def __init__(player, color, pos):                                       #Determines the player once cubes is determined.
        player.color = color                                                #This are the components of what the game will happen once it starts
        player.head = cubes(pos)            
        player.body.append(player.head)
        player.dirnx = 0
        player.dirny = 1
 
    def step(player):                                                       #Moves the the player make by presseing Keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                   #Game Ends
                pygame.quit()
 
            keys = pygame.key.get_pressed()                                 #Pygame system whether specific buttons are pressed
 
            for key in keys:                                                #If Keys are pressed
                if keys[pygame.K_LEFT]:                                     #if Left Key is pressed it moves left
                    player.dirnx = -1
                    player.dirny = 0
                    player.turns[player.head.pos[:]] = [player.dirnx, player.dirny]
 
                elif keys[pygame.K_RIGHT]:                                  #If Right Key is pressed it moves right
                    player.dirnx = 1
                    player.dirny = 0
                    player.turns[player.head.pos[:]] = [player.dirnx, player.dirny]
 
                elif keys[pygame.K_UP]:                                     #If Up key is pressed it moves up
                    player.dirnx = 0
                    player.dirny = -1
                    player.turns[player.head.pos[:]] = [player.dirnx, player.dirny]
 
                elif keys[pygame.K_DOWN]:                                   #If down key is press moves down
                    player.dirnx = 0
                    player.dirny = 1
                    player.turns[player.head.pos[:]] = [player.dirnx, player.dirny]

                                                                            #This is similar on how a cartesian plane works with the answer is in the form
                                                                            #of (x,y) which determines on what location the player is located, but imagining
                                                                            #it on Quadrant four and all sides are positive.
 
        for i, c in enumerate(player.body):                                 #This determine the turns of the body if the player pressed a key
            p = c.pos[:]
            if p in player.turns:
                turn = player.turns[p]
                c.step(turn[0],turn[1])
                if i == len(player.body)-1:
                    player.turns.pop(p)
            else:                                                           #Thus affecting the Food taken and the turns the will take
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.row-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.row-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.row-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.row-1)
                else: c.step(c.dirnx,c.dirny)
       
    def reset(player, pos):                                                 #If the game is over the funstion will reset the player in a back to the position
        player.head = cubes(pos)
        player.body = []
        player.body.append(player.head)
        player.turns = {}
        player.dirnx = 0
        player.dirny = 1
 
    def addCube(player):                                                    #Once food is consumed
        tail = player.body[-1]                                              #Adding a tail
        dx, dy = tail.dirnx, tail.dirny                                     #Specifically putting the tail behind the snake and trail it.

        #These if statements are have the same function but only specified when the snake have eaten a food in a specific direction
        if dx == 1 and dy == 0:
            player.body.append(cubes((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            player.body.append(cubes((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            player.body.append(cubes((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            player.body.append(cubes((tail.pos[0],tail.pos[1]+1)))
 
        player.body[-1].dirnx = dx
        player.body[-1].dirny = dy
       
    def draw(player, surface):                      
        for i, c in enumerate(player.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
def drawGrid(w, row, surface):
    sizeBtwn = w // row                                                     #The Space between the line
 
    x = 0
    y = 0
    for l in range(row):                                                    #The number of LINES vertically and horizontally and the Location
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (15,56,15), (x,0),(x,w))                  #Specifies the color and location of the Grid(Vertical)
        pygame.draw.line(surface, (48,98,48), (0,y),(w,y))                  #Specifies the color and location of the Grid(Horizontal)

def redrawWindow(surface):                                                  #It will show what are the things being displayed on the Program
    global row, width, s, snack                                             #Globally use the same variables
    surface.fill((156, 160, 76))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, row, surface)
    pygame.display.update()
 
def randomSnack(row, item):                                                 #Summons Food in a Once game started or eaten
 
    positions = item.body
 
    while True:                                                             #This randomize the placement of the food once the food is summoned
        x = random.randrange(row)                   
        y = random.randrange(row)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       #In the Main() function They Dnack will automatically reset since it has its own prgram once the snack and the player insteracted in the same range.
    return (x,y)
 
def message_box(subject, content):                                          #Message box from tkinter.
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
def main():
#IF STATEMENTS - Determine the size of the Game
    if Choice == 1:                                                         #Variables changes the Size into 15x15
        x = 15
        y = 400
    elif Choice == 2:                                                       #Variables changes the Size into 20x20
        x = 20
        y = 500
    elif Choice == 3:                                                       #Variables changes the Size into 20x20
        x = 35
        y = 700
        
    global width, row, s, snack
    width = y                                                               #Size of the Window.
    row = x                                                                 #The Number of rows, Also applies as columns since the snake game is square.
    win = pygame.display.set_mode((width, width))                           #Display is a window size, width and width is the same since its a square.
    s = character((15,56,15), (10,10))                                      # Implies the color of the player and where the character is placed at the start of the game.
    snack = cubes(randomSnack(row, s), color=(15,56,15))                    #Randomly changes the Postion of the Food and Color of the 2nd and more snack's color.
    flag = True
    
    clock = pygame.time.Clock()                                             #The close will determine the speed of the player. Speed is constant
   
    while flag:
        pygame.time.delay(50)                                               # Controls the Frames                                               
        clock.tick(10)                                                      #Frames per second (which is 10)
        s.step()                                                            #Takes a step
        if s.body[0].pos == snack.pos:                                      #Looping once the next step is the same or equal to the same tile with the food
            s.addCube()                                                     #Add another Food
            snack = cubes(randomSnack(row, s), color=(15,56,15))            #Determines the Cube in a random set and the color
 
        for x in range(len(s.body)):                                        #Looping in case the 
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):     #Statement specification whether the Player Does something wrong i.e. Hitting yourself or pressing the key of the opposite direction.
                file1 = open("Leaderboards.txt", "a")
                print("NAME: ", name, file=file1)
                print("GRID: ", des, file=file1)
                print("SCORE: ", len(s.body) * 10,file=file1)               #Prints the score to the leaderboards.
                print("\n", file=file1)
                file1.close()
                message_box("You Lost!", "SCORE: {0} \n Check the Leaderboards for you previous scores. \n Would you like to play Again?".format(len(s.body)*10))
                                                                            #Popups, clicking okay will restart the game. Shows the Score.
                s.reset((10,10))                                            #Reset the player in position (10,10) of the grid.
                
                break
        
        redrawWindow(win)

    
    pass

main()                                                                      #Triggers main system, but must encounter the inputs required first

