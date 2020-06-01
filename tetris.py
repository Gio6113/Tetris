#Tetris coded by Giorgio Sawaya

import math
import pygame
from pygame import mixer
import random


##Starting window and main layout
##--------------------------------------

#Setting background
pygame.init()
screen = pygame.display.set_mode((1000,790))
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
        screen.blit(title, (400, 10))

# initializing clock
clock = pygame.time.Clock()


##initializing scores
##--------------------------------------
score = 0
scoreText = pygame.font.Font('Uniforme (Font).ttf', 40)

def displayScore(x, y):
    '''(x,y) --> None'''
    showScore = scoreText.render("Score " + str(score), True, (	132, 92, 214))
    screen.blit(showScore, (x, y))


addedScore = 0
addedScoreText = pygame.font.Font('Uniforme (Font).ttf', 20)

def displayAddedScore(x, y):
    '''(x,y) --> None'''
    addScore = addedScoreText.render("+ " + str(addedScore), True, (230, 111, 0))
    screen.blit(addScore, (x, y))

    # timer = 0
    # elapsed = clock.tick(1)
    # timer = timer + elapsed/1000
    #
    # if timer > 1:
    #     return

##Calculating and displaying Scores zones and Tetris

## creating a grid of 16 by 12 blocks so 16 rows of 12
class grid(object):

    rows = 16
    columns = 12
    height = 16*15
    length = 12*15

    #constructor
    def __init__(self,start,dirnx=1,dirny=0,color=(37, 63, 63)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        """moving the cubes"""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w//self.rows
        #drawing the rectangle that is smaller than the size of the square to be able to see the borders
        pygame.draw.rect(surface, self.color, (self.pos[0]*distance+1, self.pos[1]*distance+1, distance-2, distance-2))
        if eyes:
            centre = distance//2
            radius = 3
            circleMiddleLeft = (self.pos[0]*distance+centre-radius,self.pos[1]*distance+7)
            circleMiddleRight = (self.pos[0]*distance + distance - radius*2, self.pos[1]*distance+7)
            pygame.draw.circle(surface, (25, 85, 181), circleMiddleLeft, radius)
            pygame.draw.circle(surface, (25, 85, 181), circleMiddleRight, radius)



##block

##List of all tetronimos
# tetronimos = [tripleSquare, doubleSquare, singleSquare, tripleL, quadrupleL, tripleStraight, \
# quadrupleStraight, chippedBrick, blockT, brokenPlank]

## Initializing randomly currentTetronimo and nextTetronimo
currentTetronimo = 0
nextTetronimo =0

playing = True
def main():
    while playing:


        displayBackground()

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                playing = False


            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_SPACE:
                    tetrisSound.play()
                    score += 100
                    displayAddedScore(100, 400)
                if evt.key== pygame.K_LEFT:
                    zoneSound.play()

        displayScore(750,100)
        pygame.display.update()
        pygame.time.delay(100)
main()
