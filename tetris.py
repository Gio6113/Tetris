#Tetris coded by Giorgio Sawaya
import pygame
from pygame import mixer
import random


##Global variables and default sizes
##--------------------------------------

##Window
w_lenght =  1000
w_height = 750

##Grid

##change the following 3 for your personalized board
columns = 12
rows = 20
block_side = 29  #recommanded range 25-35

border = 8
length = columns*block_side
height = rows*block_side
grid_origin_X = (w_lenght - length) // 2
grid_origin_y = w_height - height - block_side

grid_2d = [[-1 for x in range(columns)] for x in range(rows)]


## Grid showing next tetronimo
next_rows = 3
next_columns = 4
next_border = 6
next_x = w_lenght//10
next_y = w_height//2
next_length = next_columns*block_side
next_height = next_rows*block_side


##Starting window and main layout
##--------------------------------------

#Setting background
pygame.init()
screen = pygame.display.set_mode((w_lenght, w_height))
background = pygame.image.load('Background.png')

#Fixing top bar of window
pygame.display.set_caption('Tetris')
block = pygame.image.load('block.png')
pygame.display.set_icon(block)

#initializing sounds
zone_sound = mixer.Sound("Zone.wav")
tetris_sound = mixer.Sound("Tetris!.wav")

#Displaying Tetris game title
title = pygame.image.load('Title.png')

def display_background():
        screen.blit(background, (0, 0))
        screen.blit(title, ((w_lenght - title.get_width()) // 2, w_height // 75))



##Tetronimos (game pieces)
##--------------------------------------

## Creating tetronimo shapes. You can easily make a new shape by creating a 2D array and using "1" to indicate a filled block in the
## layout (check examples below). ***Don't forget to update the list of tetronimos if you added or/and removed some***.

single_square  =   [[1]]

double_square  =  [[1,1],
                   [1,1]]

triple_square  =  [[1,1,1],
                   [1,1,1],
                   [1,1,1]]

triple_l   =      [[0,0,1],
                   [1,1,1]]

skinny_l   =      [[0,0,0,1],
                   [1,1,1,1]]

quadruple_l =     [[0,0,1,1],
                   [1,1,1,1]]

triple_j =        [[1,0,0],
                   [1,1,1]]

skinny_j =        [[1,0,0,0],
                   [1,1,1,1]]

quadruple_j =      [[1,1,0,0],
                   [1,1,1,1]]

triple_straight =   [[1,1,1]]

quadruple_straight = [[1,1,1,1]]

broken_straight =    [[1,1,0,1]]

block_t =           [[0,1,0],
                     [1,1,1]]

block_plus =        [[0,1,0],
                     [1,1,1],
                     [0,1,0]]

block_gun =          [[1,1],
                      [1,0]]

chipped_brick =       [[0,1,1],
                       [1,1,1]]

spinner_block =        [[1,0,0],
                        [1,0,0],
                        [1,0,1]]

two_by_four =          [[1,1,1,1],
                        [1,1,1,1]]

two_by_one =            [[1,1]]

super_s    =           [[0,0,1,1],
                        [1,1,1,0]]

super_z      =         [[1,1,0,0],
                        [0,1,1,1]]

bridge_block =         [[1,0,1],
                        [1,0,1],
                        [1,1,1]]

mini_bridge =          [[1,0,1],
                        [1,1,1]]




##List of all tetronimos (shapes)
tetronimos = [single_square, double_square, triple_square, triple_l, skinny_l, quadruple_l, triple_j, skinny_j, quadruple_j, \
bridge_block, triple_straight, quadruple_straight, broken_straight, block_t, block_plus, block_gun, chipped_brick, spinner_block, two_by_four, \
two_by_one, mini_bridge,super_z, super_s ]

##List of all colours
tetronimo_colours = [(235, 64, 52), (255, 153, 0), (37, 215, 220), (255, 238, 0),(59, 189, 30),(217, 11, 169)]


class Tetronimo(object):

    def __init__(self, posX, posY, shape):
        self.x = posX
        self.y = posY
        self.shape = shape
        ##Identification tag and colour
        self.number = tetronimos.index(shape)
        self.colour = tetronimo_colours[self.number%len(tetronimo_colours)]

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
def drawGrid(grid_2d):

    #Drawing border
    pygame.draw.rect(screen, (163, 15, 15), (grid_origin_X-border//2, grid_origin_y-border//2, length+border, height+border), border)

    ##Drawing the taken squares
    for row in range(len(grid_2d)):
        for col in range(len(grid_2d[row])):
            if grid_2d[row][col]!=-1:
                pygame.draw.rect(screen,tetronimo_colours[grid_2d[row][col]%len(tetronimo_colours)], (grid_origin_X + col*block_side,  grid_origin_y + row*block_side, block_side, block_side))

    ##Drawing the mesh
    for horizontal_line in range(rows+1):
        pygame.draw.line(screen, (215,215,215), (grid_origin_X, grid_origin_y+ horizontal_line*block_side), (grid_origin_X + length, grid_origin_y + horizontal_line * block_side))
        for vertical_line in range(columns+1):
            pygame.draw.line(screen, (215,215,215), (grid_origin_X + vertical_line * block_side, grid_origin_y), (grid_origin_X + vertical_line * block_side, grid_origin_y + height))

#Drawing the moving piece.
def draw_current_piece(current_pos, colour):
    for pos in current_pos:
        y, x = pos
        if (y>= 0 and y<rows) and (x>= 0 and x < columns):
            pygame.draw.rect(screen, colour, (grid_origin_X + x*block_side,  grid_origin_y + y*block_side, block_side, block_side))


#Updating main grid after piece stops FALLING
def update_grid(current_pos, number):
    global grid_2d, columns, rows
    for pos in current_pos:
        y, x = pos
        if (y>= 0 and y<rows) and (x>= 0 and x <columns):
            grid_2d[y][x] = number


##Updating and displaying next grid in same fashion as the main grid
def show_next_tetronimo(next_tetronimo):

    ## Label
    next_font =  pygame.font.Font('Uniforme (Font).ttf', 25)
    next_text = next_font.render('Next Shape', 1, (132, 92, 214))
    screen.blit(next_text, (w_lenght//10 , w_height//2 - block_side - 5))

    pygame.draw.rect(screen, (163, 15, 15), (next_x-next_border//2, next_y-next_border//2, next_length+next_border, next_height+next_border), next_border)

    #Drawing the taken squares
    rows = len(next_tetronimo.shape)
    columns = len(next_tetronimo.shape[0])
    ## Go through the tetronimos shape to find all blocks that make it
    for row in range(rows):
        for col in range(columns):
            if next_tetronimo.shape[row][col] == 1:
                pygame.draw.rect(screen,next_tetronimo.colour, (next_x + col*block_side,  next_y + row*block_side, block_side, block_side))

    ##Draw the mesh
    for horizontal_line in range(next_rows+1):
        pygame.draw.line(screen, (128,128,128), (next_x, next_y+ horizontal_line*block_side), (next_x + next_length, next_y + horizontal_line * block_side))
        for vertical_line in range(next_columns+1):
            pygame.draw.line(screen, (128,128,128), (next_x + vertical_line * block_side, next_y), (next_x + vertical_line * block_side, next_y + next_height))



##Converting shapes into grid positions
def on_grid_position(current_tetronimo):
    grid_coordinates = []
    rows = len(current_tetronimo.shape)
    columns = len(current_tetronimo.shape[0])
    ## Go through the tetronimos shape to find all blocks that make it
    for row in range(rows):
        for col in range(columns):
            if current_tetronimo.shape[row][col] == 1:
                ## always y,x when working with this layout.
                grid_coordinates.append((current_tetronimo.y + row , current_tetronimo.x + col))
    return grid_coordinates



def open_space(current_pos):
    global grid_2d, columns, rows
    for pos in current_pos:
        y, x = pos
        if not((y>= 0 and y<rows) and (x>= 0 and x <columns)):
            return False
        elif grid_2d[y][x]!= -1:
            return False
    return True


#Game controls
def rotate_up(current_tetronimo):
    current_tetronimo.rotate(current_tetronimo.shape)
    current_pos = on_grid_position(current_tetronimo)
    if not open_space(current_pos):
        current_tetronimo.rotate(current_tetronimo.shape)
        current_tetronimo.rotate(current_tetronimo.shape)
        current_tetronimo.rotate(current_tetronimo.shape)



def move_left(current_tetronimo ):
    current_tetronimo.x -=1
    current_pos = on_grid_position(current_tetronimo)
    if not open_space(current_pos):
        current_tetronimo.x += 1

def move_Right(current_tetronimo):
    current_tetronimo.x +=1
    current_pos = on_grid_position(current_tetronimo)
    if not open_space(current_pos):
        current_tetronimo.x -= 1

def move_Down(current_tetronimo):
    current_tetronimo.y +=1
    current_pos = on_grid_position(current_tetronimo)
    if not open_space(current_pos):
        current_tetronimo.y -= 1



##initializing scores, lines and speed
##--------------------------------------
score = 0
score_text = pygame.font.Font('Uniforme (Font).ttf', 40)
added_score_text = pygame.font.Font('Uniforme (Font).ttf', 25)

lines = 0
line_text = pygame.font.Font('Uniforme (Font).ttf', 30)

speed = 2  ##Change this speed to 1 for easy, 2 for medium, 3 for hard

def display_score(x, y):
    show_score = score_text.render("Score " + str(score), True, (	132, 92, 214))
    screen.blit(show_score, (x, y))
    show_line = line_text.render("Lines cleared " + str(lines), True, (	132, 92, 214))
    screen.blit(show_line, (x, y+ 2*block_side))

def display_added_score(added_score,x, y):
    addScore = added_score_text.render("+ " + str(added_score), True, (215, 111, 0))
    screen.blit(addScore, (x, y))
    pygame.display.update()



def change_speed():
    if lines < 50:
       return False
    ## Speed increases by one every 20 lines cleared starting from 50 lines
    n = lines - 30
    speed = n%20 + 2


##Calculating Zones, changing score and adjusting blocks above
##--------------------------------------


def check_tetris():
    global lines, score
    counter = 0
    ## Check rows from bottom to top
    for row in range(rows):
        ## Check if the entire row does not contain a 0
        if all(x != -1 for x in grid_2d[row]):
            counter += 1
            last_row = row
            clear_row(row)

    lines += counter

    if counter == 4:
        tetris_sound.play()
        added_score = 5000
        score += added_score
        display_added_score(added_score, grid_origin_X - 3*block_side, grid_origin_y)

    elif counter > 0:
        zone_sound.play()
        for i in range(counter):
            added_score = 1000+300*i
            display_added_score(added_score, grid_origin_X - 3*block_side, grid_origin_y + last_row*block_side - i*block_side)
            score += added_score
    else:
        return False


def clear_row(row):
    for i in range(row,0,-1):
        grid_2d[i] = grid_2d[i-1]
    grid_2d[0]=[-1 for i in range(columns)]


def checkLoss(current_positions):
    global lines, score, speed, grid_2d

    #If a piece has stopped falling and is at the top than the game is over, might wanna change
    for pos in current_positions:
        y, x = pos
        ##If Player has lost
        if y < 1:
                over_font =  pygame.font.Font('Uniforme (Font).ttf', 40)
                game_over = over_font.render("Game Over, press space to play again", 1, (215,215,215))
                screen.blit(game_over,((w_lenght - game_over.get_width()) // 2, (w_height - game_over.get_height())//2))
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

                                grid_2d = [[-1 for x in range(columns)] for x in range(rows)]
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
    current_tetronimo = getTetronimo()
    next_tetronimo = getTetronimo()
    falling = True


    while playing:

        ##Keys and moves
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                playing = False
            elif evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_UP:
                    rotate_up(current_tetronimo)
                elif evt.key== pygame.K_LEFT:
                     move_left(current_tetronimo)
                elif evt.key== pygame.K_RIGHT:
                    move_Right(current_tetronimo)
                elif  evt.key== pygame.K_DOWN:
                    move_Down(current_tetronimo)

        ##Speed control
        time += clock.get_rawtime()
        clock.tick()

        if 1000/time <= speed:
                time = 1
                current_tetronimo.y += 1
                current_pos = on_grid_position(current_tetronimo)
                if (not (open_space(current_pos)) and current_tetronimo.y > 0):
                    current_tetronimo.y -= 1
                    falling = False

        current_pos = on_grid_position(current_tetronimo)

        if not falling:
            update_grid(current_pos, current_tetronimo.number)
            check_tetris()
            checkLoss(current_pos)
            change_speed()
            current_tetronimo = next_tetronimo
            next_tetronimo = getTetronimo()
            falling = True

        display_background()
        display_score(w_lenght*3//4,w_height//10)
        draw_current_piece(current_pos, current_tetronimo.colour)
        drawGrid(grid_2d)
        show_next_tetronimo(next_tetronimo)


        pygame.display.update()

    pygame.quit()

main()
