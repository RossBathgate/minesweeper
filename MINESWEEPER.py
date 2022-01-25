#Ross Bathgate
#Minesweeper Challenge
#Started 11th March 2020

#Notes:
#1. Minimum Screen Width and Height is 500 x 500
#2. Game over and welcome screens 500 x 500

#--------------------

#import modules
import sys
import os
#hide the pygame welcome message
try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except Exception as e:
    pass
import pygame
import random
import time

"""
#make sure user is running in console
if 'idlelib.run' in sys.modules:
    print(">>ERROR>> Game must not be run from IDLE Shell")
    time.sleep(3)
    quit()
"""

#get size of board from user to base variable initialisation
def validate(user,valid):
    if user not in valid:
        return False
    return True

print("MINESWEEPER   |   By Ross Bathgate\n")
print("Before you play,")
boardSize = str(input("Please enter the board size you wish to use:\n>>'S' (5x5)\n>>'M' (7x7)\n>>'L'(10x10)\n>>'XL'(18x18)\n>>'secret'\n\n>>Your_answer>>"))
while not validate(boardSize,["S","M","L","XL","SECRET","s","m","l","xl","secret"]):
    boardSize = str(input("Invalid\n>>Your_answer>>"))

#intialise variables
if boardSize.upper() == "S":
    widthOfBox = 140
    numBoxesX, numBoxesY = 5,5
    textSize = 70
    bombFileSource = "large_bomb.png"
elif boardSize.upper() == "M":
    widthOfBox = 100
    numBoxesX, numBoxesY = 7,7
    textSize = 55
    bombFileSource = "medium_bomb.png"
elif boardSize.upper() == "L":
    widthOfBox = 70
    numBoxesX, numBoxesY = 10, 10
    textSize = 40
    bombFileSource = "small_bomb.png"
elif boardSize.upper() == "XL":
    widthOfBox = 40
    numBoxesX, numBoxesY = 18,18
    textSize = 20
    bombFileSource = "XS_bomb.png"
elif boardSize.upper() == "SECRET":
    b = str(input("\n>>'XXL' [!] (40x40)\n>>'XXXL' [! - 4K resolution] (100x100)\nNote: Options marked with [!] are not fully supported and will require a powerful processor"))
    while not validate(b,["xxl","xxxl","XXL","XXXL"]):
        b = str(input("Invalid\n>>Your_answer>>"))

    if b.upper() == "XXL":
        widthOfBox = 20
        numBoxesX, numBoxesY = 40,40
        textSize = 10
        bombFileSource = "secret_bomb.png"
    elif b.upper() == "XXXL":
        widthOfBox = 11
        numBoxesX, numBoxesY = 100,100
        textSize = 10
        bombFileSource = "XXXS_bomb.png"

lineWidth = 2
screenWidth, screenHeight = numBoxesX * (widthOfBox + lineWidth) + lineWidth, numBoxesY * (widthOfBox + lineWidth) + lineWidth
lineFill = (0,0,0)
backFill = (255,255,255)
flagFill = (22, 237, 123)
#2-D arrays to store all square and button objects
squares = [[0 for i in range(numBoxesY)] for j in range(numBoxesX)]
buttons = [[0 for i in range(numBoxesY)] for j in range(numBoxesX)]

#pygame intialisation
pygame.init()
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Minesweeper   |   By Ross Bathgate')
window.fill(backFill)

#used at the end of the game to reveal all the squares
def reveal_all():
    for a in range(numBoxesX):
        for b in range(numBoxesY):
            squares[a][b].reveal(end_of_game = True)

#class for a square
class square():
    #constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_x = int(self.x / (widthOfBox + lineWidth))
        self.grid_y = int(self.y / (widthOfBox + lineWidth))
        self.revealed = False
        self.number = 0
        self.isFlagged = False
        randomNum = random.randint(0,4)
        if randomNum // 2 == 2:
            self.isBomb = True
        else:
            self.isBomb = False

    #determine the number if not a bomb
    def determineNumber(self):
        if not(self.isBomb):
            for i in range(-1,2):
                for j in range(-1,2):
                    x_to_test, y_to_test = self.grid_x + i, self.grid_y + j
                    #make sure the square to test for a bomb exists and is not outwith screen
                    if (x_to_test > -1 and y_to_test > -1) and (x_to_test < numBoxesX and y_to_test <numBoxesY):
                        if squares[x_to_test][y_to_test].isBomb:
                            self.number += 1

    #user can flag the square as a potential bomb
    def toggleFlag(self):
        if not(self.revealed):
            if self.isFlagged:
                pygame.draw.rect(window, backFill, (self.x+lineWidth,self.y+lineWidth,widthOfBox,widthOfBox))
                self.isFlagged = False
            else:
                pygame.draw.rect(window, flagFill, (self.x+lineWidth,self.y+lineWidth,widthOfBox,widthOfBox))
                self.isFlagged = True
        pygame.display.update()

    #reveal the contents of the current square object
    def reveal(self, end_of_game):
        self.revealed = True
        if not(end_of_game):
            if not(self.isBomb):
                #draw number
                font = pygame.font.SysFont('Century', textSize)
                text = font.render(str(self.number), False, (0, 0, 0))
                window.blit(text,(self.x+lineWidth + int(widthOfBox / 3),self.y+lineWidth + int(widthOfBox / 6)))
            else:
                #draw bomb
                pygame.draw.rect(window,(255,0,0),(self.x+lineWidth,self.y+lineWidth,widthOfBox,widthOfBox))
                img_x, img_y = self.x+lineWidth,self.y+lineWidth
                bombImg = pygame.image.load(bombFileSource)
                window.blit(bombImg, (img_x,img_y))
                pygame.display.update()
                reveal_all()
                time.sleep(1)
                img_x, img_y = int((screenWidth - 500) // 2), int((screenHeight - 500) // 2)  #-500 as image is 500px x 500px
                endImg = pygame.image.load('gameOver.png')
                window.blit(endImg, (img_x,img_y))
                pygame.display.update()
        else:
            #end of game
            if not(self.isBomb):
                #draw number
                font = pygame.font.SysFont('Century', textSize)
                text = font.render(str(self.number), False, (0, 0, 0))
                window.blit(text,(self.x+lineWidth + int(widthOfBox / 3),self.y+lineWidth + int(widthOfBox / 6)))
            else:
                #draw bomb
                pygame.draw.rect(window,(255,0,0),(self.x+lineWidth,self.y+lineWidth,widthOfBox,widthOfBox))
                img_x, img_y = self.x+lineWidth,self.y+lineWidth
                bombImg = pygame.image.load(bombFileSource)
                window.blit(bombImg, (img_x,img_y))
            pygame.display.update()

#class for clickable button
class button():
    #constructor
    def __init__(self,x,y):
        self.left_x = x
        self.right_x = x + widthOfBox
        self.top_y = y
        self.bottom_y = y + widthOfBox

    #test if the user has clicked on the current button
    def clicked(self,pos):
        mouseX,mouseY = pos
        if mouseX in range(self.left_x, self.right_x + 1):
            if mouseY in range(self.top_y, self.bottom_y + 1):
                return True
        return False

#draw the grid-pattern
def drawGridLines():
    for x in range(numBoxesX + 1): #+1 so that final line is drawn on screen
        pygame.draw.rect(window, lineFill, ((widthOfBox + lineWidth) * x, 0, lineWidth, screenHeight))

    for y in range(numBoxesY + 1):
        pygame.draw.rect(window, lineFill, (0, (widthOfBox + lineWidth) * y, screenWidth, lineWidth))

#test if a player has won the game
def playerWon():
    #determine the total number of bombs
    bombCount = 0
    for a in range(numBoxesX):
        for b in range(numBoxesY):
            if squares[a][b].isBomb:
                bombCount += 1
    #get number of squares which are not revealed
    counter = 0
    for a in range(numBoxesX):
        for b in range(numBoxesY):
            if not(squares[a][b].revealed):
                counter += 1
    if bombCount == counter:
        return True
    return False

#display winning screen to the user
def displayWin():
    img_x, img_y = int((screenWidth - 500) // 2), int((screenHeight - 500) // 2)  #-500 as image is 500px x 500px
    winImg = pygame.image.load('win.png')
    window.blit(winImg, (img_x,img_y))
    pygame.display.update()


#main program:
window.fill(backFill)
backImg = pygame.image.load('minefield.jpg')
window.blit(backImg, (0,0))
img_x, img_y = int((screenWidth - 500) // 2), int((screenHeight - 500) // 2)  #-500 as image is 500px x 500px
startImg = pygame.image.load('start.png')
window.blit(startImg, (img_x,img_y))
pygame.display.update()

#start screen - test for space click or user QUIT
run2 = True
while run2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run2 = False

#reset board
window.fill(backFill)

#initially, create all square and button objects
for x in range(numBoxesX):
    for y in range(numBoxesY):
        squares[x][y] = square((widthOfBox + lineWidth) * x, (widthOfBox + lineWidth) * y)
        buttons[x][y] = button((widthOfBox + lineWidth) * x, (widthOfBox + lineWidth) * y)

#determine the number each cell will hold:
for x in range(numBoxesX):
    for y in range(numBoxesY):
        squares[x][y].determineNumber()

#draw all grid lines
drawGridLines()

#main loop of program
run = True
while run:
    if playerWon():
        displayWin()
        run3 = True
        while run3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    #test for user QUIT and user click
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for a in range(numBoxesX):
                for b in range(numBoxesY):
                    if buttons[a][b].clicked(mouse_pos):
                        if not(squares[a][b].revealed):
                            if squares[a][b].isFlagged:
                                squares[a][b].toggleFlag()
                            squares[a][b].reveal(end_of_game = False)
        #flag a square
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                #user has pressed 'f' to toggle flag on a square
                mouse_pos = pygame.mouse.get_pos()
                for a in range(numBoxesX):
                    for b in range(numBoxesY):
                        #re-using the button class - clicked() has the same use here to determine which square should be toggled
                        if buttons[a][b].clicked(mouse_pos):
                            squares[a][b].toggleFlag()
    #update the display
    pygame.display.update()

# -----  game end  -----
