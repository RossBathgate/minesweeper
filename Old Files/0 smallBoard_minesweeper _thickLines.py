#Ross Bathgate
#Minesweeper Challenge
#Started 11th March 2020


#Notes:
#1. Minimum Screen Width and Height is 500 x 500
#2. Game over and welcome screens 500 x 500

#import modules
import pygame
import random
import time

#intialise variables
widthOfBox = 140
lineWidth = 7
numBoxesX, numBoxesY = 5,5 #ideal is 10,10
screenWidth, screenHeight = numBoxesX * (widthOfBox + lineWidth) + lineWidth, numBoxesY * (widthOfBox + lineWidth) + lineWidth
lineFill = (0,0,0)
backFill = (255,255,255)

#2d array to store all squares
squares = [[0 for i in range(numBoxesY)] for j in range(numBoxesX)]
buttons = [[0 for i in range(numBoxesY)] for j in range(numBoxesX)]


#pygame intialisation
pygame.init()
#pygame.font.init()
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Minesweeper   |   By Ross Bathgate')
window.fill(backFill)

def reveal_all():
    for a in range(numBoxesX):
        for b in range(numBoxesY):
            squares[a][b].reveal(end_of_game = True)
#class for a square
class square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid_x = int(self.x / (widthOfBox + lineWidth))
        self.grid_y = int(self.y / (widthOfBox + lineWidth))
        self.revealed = False
        self.number = 0
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


    def reveal(self, end_of_game):
        self.revealed = True

        if not(end_of_game):
            if not(self.isBomb):
                #draw number
                font = pygame.font.SysFont('Century', 70)
                text = font.render(str(self.number), False, (0, 0, 0))
                window.blit(text,(self.x+lineWidth + int(widthOfBox / 3),self.y+lineWidth + int(widthOfBox / 6)))
            else:
                #draw bomb
                pygame.draw.rect(window,(255,0,0),(self.x+lineWidth,self.y+lineWidth,widthOfBox,widthOfBox))
                img_x, img_y = self.x+lineWidth,self.y+lineWidth
                bombImg = pygame.image.load('large_bomb.png')
                window.blit(bombImg, (img_x,img_y))


                pygame.display.update()
                reveal_all()
                time.sleep(1.5)

                img_x, img_y = int((screenWidth - 500) // 2), int((screenHeight - 500) // 2)  #-500 as image is 500px x 500px
                endImg = pygame.image.load('gameOver.png')
                window.blit(endImg, (img_x,img_y))
                pygame.display.update()
        else:
            #end of game
            if not(self.isBomb):
                #draw number
                font = pygame.font.SysFont('Century', 70)
                text = font.render(str(self.number), False, (0, 0, 0))
                window.blit(text,(self.x+lineWidth + int(widthOfBox / 3),self.y+lineWidth + int(widthOfBox / 6)))
            else:
                #draw bomb
                pygame.draw.rect(window,(255,0,0),(self.x+lineWidth,self.y+lineWidth,widthOfBox,widthOfBox))
                img_x, img_y = self.x+lineWidth,self.y+lineWidth
                bombImg = pygame.image.load('large_bomb.png')
                window.blit(bombImg, (img_x,img_y))
            pygame.display.update()


#class for clickable button
class button():
    def __init__(self,x,y):
        self.left_x = x
        self.right_x = x + widthOfBox
        self.top_y = y
        self.bottom_y = y + widthOfBox

    def clicked(self,pos):
        mouseX,mouseY = pos
        if mouseX in range(self.left_x, self.right_x + 1):
            if mouseY in range(self.top_y, self.bottom_y + 1):
                return True
        return False


def drawGridLines():
    for x in range(numBoxesX + 1): #+1 so that final line is drawn on screen
        pygame.draw.rect(window, lineFill, ((widthOfBox + lineWidth) * x, 0, lineWidth, screenHeight))

    for y in range(numBoxesY + 1):
        pygame.draw.rect(window, lineFill, (0, (widthOfBox + lineWidth) * y, screenWidth, lineWidth))


#main loop:

backImg = pygame.image.load('minefield.jpg')
window.blit(backImg, (0,0))
img_x, img_y = int((screenWidth - 500) // 2), int((screenHeight - 500) // 2)  #-500 as image is 500px x 500px
startImg = pygame.image.load('start.png')
window.blit(startImg, (img_x,img_y))
pygame.display.update()

run2 = True
quit = False
while run2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run2 = False
            quit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run2 = False

window.fill(backFill)

#initially, fill all squares and create clickable buttons
for x in range(numBoxesX):
    for y in range(numBoxesY):
        squares[x][y] = square((widthOfBox + lineWidth) * x, (widthOfBox + lineWidth) * y)
        buttons[x][y] = button((widthOfBox + lineWidth) * x, (widthOfBox + lineWidth) * y)


#determine the number each cell will hold:
for x in range(numBoxesX):
    for y in range(numBoxesY):
        squares[x][y].determineNumber()

run = False
if not(quit):
    run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for a in range(numBoxesX):
                for b in range(numBoxesY):
                    if buttons[a][b].clicked(mouse_pos):
                        if not(squares[a][b].revealed):
                            squares[a][b].reveal(end_of_game = False)

    drawGridLines()
    pygame.display.update()
