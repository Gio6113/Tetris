#Tetris coded by Giorgio Sawaya
import pygame
from pygame import mixer
import random


##Global variables and default sizes
##--------------------------------------

##Window
wLength =  1000
wHeight = 750


## Gives empty 2d arrays
def gridMaker(rows,columns):
    grid = []
    temporary = []
    for i in range (rows):
         for j in range (columns):
                temporary.append(0)
         grid.append(temporary)
         temporary = []
    return grid

##Grid
columns = 12
rows = 18
blockSide = 28

border = 8
length = columns*blockSide
height = rows*blockSide
gridOriginX = (wLength - length) // 2
gridOriginY = wHeight - height - blockSide

grid2D = gridMaker(rows,columns)


## Grid showing next tetronimo
nRows = 3
nColumns = 4
nBorder = 10
nextX = wLength//10
nextY = wHeight//2
nLength = nColumns*blockSide
nHeight = nRows*blockSide

nextGrid2D =  gridMaker(nRows,nColumns)


##Starting window and main layout
##--------------------------------------

#Setting background
pygame.init()
screen = pygame.display.set_mode((wLength, wHeight))
background = pygame.image.load('Background.png')

#Fixing top bar of window
pygame.display.set_caption('Tetris')
block = pygame.image.load('block.png')
pygame.display.set_icon(block)

#initializing sounds
zoneSound = mixer.Sound("Zone.wav")
tetrisSound = mixer.Sound("Tetris!.wav")

#Displaying Tetris game title
title = pygame.image.load('Title.png')

def displayBackground():
        screen.blit(background, (0, 0))
        screen.blit(title, ((wLength - title.get_width()) // 2, wHeight // 75))


##Tetronimos (game pieces)
##--------------------------------------

## Creating tetronimo shapes
singleSquare  =  [[1]]

doubleSquare  = [[1,1],
                 [1,1]]

tripleSquare  = [[1,1,1],
                 [1,1,1],
                 [1,1,1]]

tripleL   =      [[0,0,1],
                  [1,1,1]]

skinnyL   =      [[0,0,0,1],
                  [1,1,1,1]]

quadrupleL =     [[0,0,1,1],
                  [1,1,1,1]]

tripleJ =        [[1,0,0],
                  [1,1,1]]

skinnyJ =        [[1,0,0,0],
                  [1,1,1,1]]

quadrupleJ =     [[1,1,0,0],
                  [1,1,1,1]]

tripleStraight =  [[1,1,1]]

quadrupleStraight= [[1,1,1,1]]

brokenStraight =    [[1,1,0,1]]

blockT =            [[0,1,0],
                     [1,1,1]]

blockPlus =         [[0,1,0],
                     [1,1,1],
                     [0,1,0]]

blockGun =           [[1,1],
                      [1,0]]

chippedBrick =        [[0,1,1],
                       [1,1,1]]

spinnerBlock =         [[1,0,1],
                        [0,0,0],
                        [1,0,1]]

##List of all tetronimos (shapes)
tetronimos = [singleSquare, doubleSquare, tripleSquare, tripleL, skinnyL, quadrupleL,tripleJ, skinnyJ, quadrupleJ, \
tripleStraight, quadrupleStraight, brokenStraight, blockT, blockPlus, blockGun, chippedBrick, spinnerBlock]

##List of all colours
tetronimo_colours = [(235, 64, 52), (255, 153, 0), (37, 215, 220), (255, 238, 0),(59, 189, 30),(217, 11, 169)]


class Tetronimo(object):

    def __init__(self, posX, posY, shape):
        self.x = posX
        self.y = posY
        self.shape = shape
        ##Identification tag and colour
        self.number = tetronimos.index(shape)+1
        self.colour = tetronimo_colours[tetronimos.index(shape)%len(tetronimo_colours)]

    def rotate(self, shape):
        columns = len(self.shape[0])
        rows = len(self.shape)
        temp = []
        index = 0
        for i in range (columns) :
             row = []
             for j in range (rows-1, -1 ,-1):
                row.append(shape[j][i])
             temp.append(row)
        self.shape = temp






##Displaying pieces and grids
##--------------------------------------

##Updating and displaying main grid
def drawGrid(grid2D):
    #Drawing border
    pygame.draw.rect(background, (163, 15, 15), (gridOriginX-border//2, gridOriginY-border//2, length+border, height+border), border)

    ##Drawing the taken squares
    for row in range(len(grid2D)):
        for col in range(len(grid2D[row])):
            if grid2D[row][col]!=0:
                pygame.draw.rect(background,tetronimo_colours[grid2D[row][col]%len(tetronimo_colours)], (gridOriginX + col*blockSide,  gridOriginY + row*blockSide, blockSide, blockSide))

    ##Drawing the mesh
    for horizontalLine in range(rows+1):
        pygame.draw.line(background, (215,215,215), (gridOriginX, gridOriginY+ horizontalLine*blockSide), (gridOriginX + length, gridOriginY + horizontalLine * blockSide))
        for verticalLine in range(columns+1):
            pygame.draw.line(background, (215,215,215), (gridOriginX + verticalLine * blockSide, gridOriginY), (gridOriginX + verticalLine * blockSide, gridOriginY + height))


def showNextTetronimo(nextTetronimo):

    ## Label
    nextFont =  pygame.font.Font('Uniforme (Font).ttf', 25)
    nextText = nextFont.render('Next Shape', 1, (132, 92, 214))
    screen.blit(nextText, (wLength//10 , wHeight//2 - blockSide - 5))

    pygame.draw.rect(background, (163, 15, 15), (nextX-nBorder//2, nextY-nBorder//2, nLength+nBorder, nHeight+nBorder), nBorder)

    #Drawing the taken squares
    for horizontalLine in range(nRows+1):
        pygame.draw.line(background, (128,128,128), (nextX, nextY+ horizontalLine*blockSide), (nextX + nLength, nextY + horizontalLine * blockSide))
        for verticalLine in range(nColumns+1):
            pygame.draw.line(background, (128,128,128), (nextX + verticalLine * blockSide, nextY), (nextX + verticalLine * blockSide, nextY + nHeight))



def openSpace(currentTetronimo, grid2D):
    return

#Game controls
def moveLeft(self):
    self.x -=1
    if not openSpace(currentTetronimo, grid2D):
        self.x += 1

def moveRight(self):
    self.x +=1
    if not openSpace(currentTetronimo, grid2D):
        self.x -= 1

def moveDown(self):
    self.y +=1
    if not openSpace(currentTetronimo, grid2D):
        self.y -= 1












##Processing active and nextTetronimo
def getTetronimo():
    shape = random.choice(tetronimos)
    tetronimo = Tetronimo(4,-2,shape)
    return tetronimo


def stillFalling(currentTetronimo):
    i = 0
    ##check if tetronimo hits a block
    if i == 0:
        return True
    return False




##initializing scores
##--------------------------------------
score = 0
scoreText = pygame.font.Font('Uniforme (Font).ttf', 40)
addedScoreText = pygame.font.Font('Uniforme (Font).ttf', 20)

lines = 0
lineText = pygame.font.Font('Uniforme (Font).ttf', 30)

def displayScore(x, y):
    '''(x,y) --> None'''
    showScore = scoreText.render("Score " + str(score), True, (	132, 92, 214))
    screen.blit(showScore, (x, y))
    showLine = lineText.render("Lines cleared " + str(lines), True, (	132, 92, 214))
    screen.blit(showLine, (x, y+ 2*blockSide))

def displayAddedScore(addedScore,x, y):
    '''(x,y) --> None'''
    addScore = addedScoreText.render("+ " + str(addedScore), True, (215, 111, 0))
    screen.blit(addScore, (x, y))



##Calculating Zones, changing score and adjusting blocks above
##--------------------------------------

def fall():
    for i in range(rows-1):
        for j in range (columns):
            ##Check for taken square
            if grid2D[i][j] != 0:
                ## Check that the block is falling
                if grid2D[i+1][j] == 0:
                    grid2D[i+1][j]== grid2D[i][j]

def clearRow():
    return


def checkTetris():
    ## Check rows from bottom to top
    for i in range(rows-1,-1 ,-1):
        ## Check if the entire row does not contain a 0
        if grid2D[i][1:] == grid2D[i][:-1]: ## This is wrong
            i = 0

    tetrisSound.play()
    score += 1000
    ## Need new x,y coordinates
    displayAddedScore(100, 400)

def checkZone():
    zoneSound.play()
    score += 100
    ## Need new x,y coordinates
    displayAddedScore(100, 400)

def checkLoss():
    ##If a piece has stopped falling and is at the top than the game is over
    for j in range(columns):
        if grid2D[0][j] != 0 :
        while True:
            overFont = pygame.font.SysFont('comicsans', size,
            gameOver = font.render("Game Over, press space to play again", 1, (215,215,215))
            screen.blit(showLine, ((wLength - gameOver.get_width()) // 2, (wHeight - gameOver.get_height())//2)



            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid2D = gridMaker()
                    main()

    return False



##Main Function, Let's play
##--------------------------------------
def main():

    playing = True


    # initializing clock and setting fall speed
    clock = pygame.time.Clock()
    time = 0.1
    speed = 3  ##Change this speed to 1 for easy, 2 for medium, 3 for hard

    ## Picking first 2 pieces randomly
    currentTetronimo = getTetronimo()
    nextTetronimo = getTetronimo()

    while playing:
        displayBackground()
        drawGrid(grid2D)
        showNextTetronimo(nextTetronimo)

        ##Speed control
        time += clock.get_rawtime()
        clock.tick()

        if 1000/time <= speed:
                time = 0


        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                playing = False
            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_UP:
                    currentTetronimo.rotate(currentTetronimo.shape)
                elif evt.key== pygame.K_LEFT:
                    moveLeft(currentTetronimo)
                elif evt.key== pygame.K_RIGHT:
                    moveRight(currentTetronimo)
                elif  evt.key== pygame.K_DOWN:
                    moveDown(currentTeronimo)

        if not stillFalling(currentTetronimo):
            fall()
            checkTetris()
            checkLoss()
            currentTetronimo = nextTetronimo
            nextTetronimo = getTetronimo()
        displayScore(wLength*3//4,wHeight//10)
        pygame.display.update()
        pygame.time.delay(100)

    pygame.quit()

main()
