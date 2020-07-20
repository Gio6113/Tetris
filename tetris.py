#Tetris coded by Giorgio Sawaya
import pygame
from pygame import mixer
import random


##Global variables and default sizes
##--------------------------------------

##Window
wLength =  1000
wHeight = 750

##Grid

##change the following 3 for your personalized board
columns = 12
rows = 18
blockSide = 29  #recommanded range 25-35

border = 8
length = columns*blockSide
height = rows*blockSide
gridOriginX = (wLength - length) // 2
gridOriginY = wHeight - height - blockSide

grid2D = [[-1 for x in range(columns)] for x in range(rows)]


## Grid showing next tetronimo
nRows = 3
nColumns = 4
nBorder = 6
nextX = wLength//10
nextY = wHeight//2
nLength = nColumns*blockSide
nHeight = nRows*blockSide


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

## Creating tetronimo shapes. You can easily make a new shape by creating a 2D array and using "1" to indicate a filled block in the
## layout (check examples below). Don't forget to update the list of tetronimos if you added or/and removed some.

singleSquare  =   [[1]]

doubleSquare  =   [[1,1],
                   [1,1]]

tripleSquare  =   [[1,1,1],
                   [1,1,1],
                   [1,1,1]]

tripleL   =       [[0,0,1],
                   [1,1,1]]

skinnyL   =       [[0,0,0,1],
                   [1,1,1,1]]

quadrupleL =      [[0,0,1,1],
                   [1,1,1,1]]

tripleJ =         [[1,0,0],
                   [1,1,1]]

skinnyJ =         [[1,0,0,0],
                   [1,1,1,1]]

quadrupleJ =      [[1,1,0,0],
                   [1,1,1,1]]

tripleStraight =   [[1,1,1]]

quadrupleStraight = [[1,1,1,1]]

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

spinnerBlock =         [[1,0,0],
                        [1,0,0],
                        [1,0,1]]

twoByFour =            [[1,1,1,1],
                        [1,1,1,1]]

twoByOne  =            [[1,1]]

superS    =            [[0,0,1,1],
                        [1,1,1,0]]

superZ      =          [[1,1,0,0],
                        [0,1,1,1]]

bridgeBlock =          [[1,0,1],
                        [1,0,1],
                        [1,1,1]]

miniBridge =           [[1,0,1],
                        [1,1,1]]




##List of all tetronimos (shapes)
tetronimos = [singleSquare, doubleSquare, tripleSquare, tripleL, skinnyL, quadrupleL, tripleJ, skinnyJ, quadrupleJ, bridgeBlock, \
tripleStraight, quadrupleStraight, brokenStraight,blockT, blockPlus, blockGun, chippedBrick, spinnerBlock, twoByFour, \
twoByOne, miniBridge, bridgeBlock, superZ, superS ]

##List of all colours
tetronimoColours = [(235, 64, 52), (255, 153, 0), (37, 215, 220), (255, 238, 0),(59, 189, 30),(217, 11, 169)]


class Tetronimo(object):

    def __init__(self, posX, posY, shape):
        self.x = posX
        self.y = posY
        self.shape = shape
        ##Identification tag and colour
        self.number = tetronimos.index(shape)
        self.colour = tetronimoColours[self.number%len(tetronimoColours)]

    def rotate(self, shape):
        columns = len(self.shape[0])
        rows = len(self.shape)
        nextPos = []
        index = 0
        for i in range (columns) :
             row = []
             for j in range (rows-1, -1 ,-1):
                row.append(shape[j][i])
             nextPos.append(row)
        self.shape = nextPos


def getTetronimo():
    shape = random.choice(tetronimos)
    tetronimo = Tetronimo(4,-2,shape)
    return tetronimo



##Displaying pieces and grids
##--------------------------------------

#displaying main grid
def drawGrid(grid2D):

    #Drawing border
    pygame.draw.rect(screen, (163, 15, 15), (gridOriginX-border//2, gridOriginY-border//2, length+border, height+border), border)

    ##Drawing the taken squares
    for row in range(len(grid2D)):
        for col in range(len(grid2D[row])):
            if grid2D[row][col]!=-1:
                pygame.draw.rect(screen,tetronimoColours[grid2D[row][col]%len(tetronimoColours)], (gridOriginX + col*blockSide,  gridOriginY + row*blockSide, blockSide, blockSide))

    ##Drawing the mesh
    for horizontalLine in range(rows+1):
        pygame.draw.line(screen, (215,215,215), (gridOriginX, gridOriginY+ horizontalLine*blockSide), (gridOriginX + length, gridOriginY + horizontalLine * blockSide))
        for verticalLine in range(columns+1):
            pygame.draw.line(screen, (215,215,215), (gridOriginX + verticalLine * blockSide, gridOriginY), (gridOriginX + verticalLine * blockSide, gridOriginY + height))

#Drawing the moving piece.
def drawCurrentPiece(currentPos, colour):
    for pos in currentPos:
        y, x = pos
        if (y>= 0 and y<rows) and (x>= 0 and x < columns):
            pygame.draw.rect(screen, colour, (gridOriginX + x*blockSide,  gridOriginY + y*blockSide, blockSide, blockSide))


#Updating main grid after piece stops FALLING
def updateGrid(currentPos, number):
    global grid2D, columns, rows
    for pos in currentPos:
        y, x = pos
        if (y>= 0 and y<rows) and (x>= 0 and x <columns):
            grid2D[y][x] = number


##Updating and displaying next grid in same fashion as the main grid
def showNextTetronimo(nextTetronimo):

    ## Label
    nextFont =  pygame.font.Font('Uniforme (Font).ttf', 25)
    nextText = nextFont.render('Next Shape', 1, (132, 92, 214))
    screen.blit(nextText, (wLength//10 , wHeight//2 - blockSide - 5))

    pygame.draw.rect(screen, (163, 15, 15), (nextX-nBorder//2, nextY-nBorder//2, nLength+nBorder, nHeight+nBorder), nBorder)

    #Drawing the taken squares
    rows = len(nextTetronimo.shape)
    columns = len(nextTetronimo.shape[0])
    ## Go through the tetronimos shape to find all blocks that make it
    for row in range(rows):
        for col in range(columns):
            if nextTetronimo.shape[row][col] == 1:
                pygame.draw.rect(screen,nextTetronimo.colour, (nextX + col*blockSide,  nextY + row*blockSide, blockSide, blockSide))

    ##Draw the mesh
    for horizontalLine in range(nRows+1):
        pygame.draw.line(screen, (128,128,128), (nextX, nextY+ horizontalLine*blockSide), (nextX + nLength, nextY + horizontalLine * blockSide))
        for verticalLine in range(nColumns+1):
            pygame.draw.line(screen, (128,128,128), (nextX + verticalLine * blockSide, nextY), (nextX + verticalLine * blockSide, nextY + nHeight))



##Converting shapes into grid positions
def onGridPosition(currentTetronimo):
    gridCoordinates = []
    rows = len(currentTetronimo.shape)
    columns = len(currentTetronimo.shape[0])
    ## Go through the tetronimos shape to find all blocks that make it
    for row in range(rows):
        for col in range(columns):
            if currentTetronimo.shape[row][col] == 1:
                ## always y,x when working with this layout.
                gridCoordinates.append((currentTetronimo.y + row , currentTetronimo.x + col))
    return gridCoordinates



def openSpace(currentPos):
    global grid2D, columns, rows
    for pos in currentPos:
        y, x = pos
        if not((y>= 0 and y<rows) and (x>= 0 and x <columns)):
            return False
        elif grid2D[y][x]!= -1:
            return False
    return True


#Game controls
def rotateUp(currentTetronimo):
    currentTetronimo.rotate(currentTetronimo.shape)
    currentPos = onGridPosition(currentTetronimo)
    if not openSpace(currentPos):
        currentTetronimo.rotate(currentTetronimo.shape)
        currentTetronimo.rotate(currentTetronimo.shape)
        currentTetronimo.rotate(currentTetronimo.shape)



def moveLeft(currentTetronimo ):
    currentTetronimo.x -=1
    currentPos = onGridPosition(currentTetronimo)
    if not openSpace(currentPos):
        currentTetronimo.x += 1

def moveRight(currentTetronimo):
    currentTetronimo.x +=1
    currentPos = onGridPosition(currentTetronimo)
    if not openSpace(currentPos):
        currentTetronimo.x -= 1

def moveDown(currentTetronimo):
    currentTetronimo.y +=1
    currentPos = onGridPosition(currentTetronimo)
    if not openSpace(currentPos):
        currentTetronimo.y -= 1



##initializing scores, lines and speed
##--------------------------------------
score = 0
scoreText = pygame.font.Font('Uniforme (Font).ttf', 40)
addedScoreText = pygame.font.Font('Uniforme (Font).ttf', 25)

lines = 0
lineText = pygame.font.Font('Uniforme (Font).ttf', 30)

speed = 2  ##Change this speed to 1 for easy, 2 for medium, 3 for hard

def displayScore(x, y):
    showScore = scoreText.render("Score " + str(score), True, (	132, 92, 214))
    screen.blit(showScore, (x, y))
    showLine = lineText.render("Lines cleared " + str(lines), True, (	132, 92, 214))
    screen.blit(showLine, (x, y+ 2*blockSide))

def displayAddedScore(addedScore,x, y):
    addScore = addedScoreText.render("+ " + str(addedScore), True, (215, 111, 0))
    screen.blit(addScore, (x, y))
    pygame.display.update()



def changeSpeed():
    if lines < 100:
       return False
    ## Speed increases by one
    n = lines - 80
    speed = n%20 + 2


##Calculating Zones, changing score and adjusting blocks above
##--------------------------------------


def checkTetris():
    global lines, score
    counter = 0
    ## Check rows from bottom to top
    for i in range(rows):
        ## Check if the entire row does not contain a 0
        if all(x != -1 for x in grid2D[i]):
            counter += 1
            lastRow = i
            clearRow(i)

    lines += counter

    if counter == 4:
        tetrisSound.play()
        addedScore = 5000
        score += addedScore
        displayAddedScore(addedScore, gridOriginX - 3*blockSide, gridOriginY)
    elif counter > 0:
        zoneSound.play()
        for i in range(counter):
            addedScore = 1000+300*i
            displayAddedScore(addedScore, gridOriginX - 3*blockSide, gridOriginY + lastRow*blockSide - i*blockSide)
            score += addedScore
    else:
        return False


def clearRow(row):
    for i in range(row,0,-1):
        grid2D[i] = grid2D[i-1]
    grid2D[0]=[-1 for i in range(columns)]


def checkLoss(currentPositions):
    global lines, score, speed, grid2D

    #If a piece has stopped falling and is at the top than the game is over, might wanna change
    for pos in currentPositions:
        y, x = pos
        ##If Player has lost
        if y < 1:
                overFont =  pygame.font.Font('Uniforme (Font).ttf', 40)
                gameOver = overFont.render("Game Over, press space to play again", 1, (215,215,215))
                screen.blit(gameOver,((wLength - gameOver.get_width()) // 2, (wHeight - gameOver.get_height())//2))
                pygame.display.update()
                print("Final score: " + str(score))
                print("Lines made: "  + str(lines))
                print("Final speed: "+ str(speed))

                choice = False
                while not choice:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            choice = True

                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                score = 0
                                lines = 0
                                speed = 2

                                grid2D = [[-1 for x in range(columns)] for x in range(rows)]
                                print("Starting new game")
                                main()
                pygame.quit()
    return False


##Main Function, Let's play
##--------------------------------------
def main():


    playing = True

    # initializing clock and time
    clock = pygame.time.Clock()
    time = 1

    ## Picking first 2 pieces randomly
    currentTetronimo = getTetronimo()
    nextTetronimo = getTetronimo()
    falling = True


    while playing:

        ##Keys and moves
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                playing = False
            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_UP:
                    rotateUp(currentTetronimo)
                elif evt.key== pygame.K_LEFT:
                     moveLeft(currentTetronimo)
                elif evt.key== pygame.K_RIGHT:
                    moveRight(currentTetronimo)
                elif  evt.key== pygame.K_DOWN:
                    moveDown(currentTetronimo)

        ##Speed control
        time += clock.get_rawtime()
        clock.tick()

        if 1000/time <= speed:
                time = 1
                currentTetronimo.y += 1
                currentPos = onGridPosition(currentTetronimo)
                if (not (openSpace(currentPos)) and currentTetronimo.y > 0):
                    currentTetronimo.y -= 1
                    falling = False

        currentPos = onGridPosition(currentTetronimo)

        if not falling:
            updateGrid(currentPos, currentTetronimo.number)
            checkTetris()
            checkLoss(currentPos)
            changeSpeed()
            currentTetronimo = nextTetronimo
            nextTetronimo = getTetronimo()
            falling = True

        displayBackground()
        displayScore(wLength*3//4,wHeight//10)
        drawCurrentPiece(currentPos, currentTetronimo.colour)
        drawGrid(grid2D)
        showNextTetronimo(nextTetronimo)


        pygame.display.update()

    pygame.quit()

main()
