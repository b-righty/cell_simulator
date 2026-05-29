import pygame
from time import sleep
from math import cos, sin, radians, atan, pi
from random import randint,uniform
from cells_module import Cell

# something to consider, using quaternions to make this 3D

pygame.init()

# Creating Window & Sets game/simulator to run
WIDTH = 900
HEIGHT = 680
screen = pygame.display.set_mode((WIDTH,HEIGHT))
running = True
# Frame Rate
clock = pygame.time.Clock()
fps = 10
# Background
screen.fill((30,30,30))

# List of Tests
testing_circularCell = False
circleCell = Cell()

testing_bacillusCell = False
bacillusCell = Cell()

testing_bend = False
testing_directionShift = False
testing_startingshift = False
btCell = Cell()
i = 0
degrees_turned = 0
start_bend = 150

testing_movement = False
mtCell = Cell()
mtCell2 = Cell()

demonstration_test = False
cells = 20

testing_rotation = False
degrees_rotated = 0
rotate = 1
rCell = Cell()

# next goal: make sure that when a cell is set to be created, that it is created.  Make it a setting so I can turn it on if I want the set amount of cedlls no matter what, and if off then that means I don't really care that much and if it can't thent he program won't try to create it again.


def circularCell_test():
    testing_circularCell = True
    for i in range(20):
        Cell().circular_cell(screen, randint(10,60), randint(60, WIDTH-60),randint(60,HEIGHT-60))
    return testing_circularCell
# testing_circularCell = circularCell_test()

def bacillusCell_test():
    testing_bacillusCell = True
    majora = randint(40,60)
    minora = majora//4
    bacillusCell.bacteria_cell(screen, majora, minora, randint(60,WIDTH-60), randint(40,HEIGHT-40),uniform(0,2),uniform(0,2))
    return testing_bacillusCell
# testing_bacillusCell = bacillusCell_test()

def bend_test(degrees):
    btCell.bacteria_cell(screen,60,20,WIDTH-500,HEIGHT-400,1,1)
    testing_bend = True
    return btCell, testing_bend, degrees
# btCell, testing_bend, i = bend_test(1)

def demonstration(cells):
    demonstration_test = True
    for i in range(cells):
        Cell().random_cell(screen,randint(60,WIDTH-60), randint(60,HEIGHT-60), randint(20,60))
    return demonstration_test
demonstration_test = demonstration(cells)

def movement_test():
    # 60, 460,250) 60, 400, 400
    # mtCell.random_cell(screen,WIDTH-440, HEIGHT-450, 60)
    mtCell.circular_cell(screen, 10, WIDTH-440, HEIGHT-450)
    mtCell.x_velocity = 0
    mtCell.y_velocity = 1
    mtCell.x_acceleration = 0
    mtCell.y_acceleration = 0
    # mtCell2.random_cell(screen,WIDTH-500, HEIGHT-500, 60)
    mtCell2.circular_cell(screen, 100, WIDTH-500, HEIGHT-300)
    mtCell2.x_velocity = 0
    mtCell2.y_velocity = -1
    mtCell2.x_acceleration = 0
    mtCell2.y_acceleration = 0
    testing_movement = True
    return mtCell, mtCell2, testing_movement
# mtCell, mtCell2, testing_movement = movement_test()

def rotate_test():
    rCell.random_cell(screen, WIDTH-500, HEIGHT-500, 10)
    return True
# testing_rotation = rotate_test()


# Make a collision detection system  *DONE*  (JUST NEED TO CLEAN IT UP)


#       To make a collision detection system I will need to make sure no cells overlap. *DONE*
#       Make cells rotate                    *DONE*
# Make a mitosis system
# Make a bacteria, virus, and human blood cell (with the nucleus in the middle)   * IN PROGRESS
#       Make an elliptical bacteria cell                      *DONE*
#       Make swiggly line bacteria cells (Learn how to turn ellipse bacteria cell)
#       Make simple animal cells with a nucleus
#       Make a plant cell with a nucleus
#       Make tail and sort of head cell
# Make a motion/drag system, where it looks like the cell's being dragged through some viscous material.
#               For the drag system, to make it look realistic make the screen act like winds.  Where each altitude interval or interval of y coordinates has a different speed which speeds whatever vertices of a cell are in the interval in by that speed, but not the whole cell.
#     Would require an acceleration and decellaration system                *IN PROGRESS*
#     Adding some hairs/tails to the cells that move and wiggle would look cool too.   *IN PROGRESS*
#     Make Cells rotate        *DONE*
# Make a consume_cell function in the class where it makes one cell disappear and gives half the radius of the consumed cell to the consumer cell, this may require making radius an instataneaous value if I want to make it in the most efficient way but I don't have to.



# Set Text
paused = False
temp = False

try:
    font = pygame.font.SysFont('Arial', 48)
except:
    font = pygame.font.SysFont(None, 48)

textPaused = font.render("PAUSED", True, (255,255,255))
rectPaused = textPaused.get_rect()
rectPaused.x = 0
rectPaused.y = 0

textFPS = font.render("FPS: "+str(fps), True , (0,255,0))
rectFPS = textFPS.get_rect()
rectFPS.x = 0
rectFPS.y = 48

while running:

    # Allows for user to click x on top right of gui and close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                temp = not temp
                screen.blit(textPaused, rectPaused)

    screen.blit(textFPS, rectFPS)
    
    # Make basic bacillus cell
    if (not paused) and testing_bacillusCell:
        bacillusCell.draw_polygon(True)

    # Make basic circular cell
    if (not paused) and testing_circularCell:
        for cell in Cell.list_of_cells:
            cell.draw_polygon(True)

    # Make cell bend
    if (not paused) and testing_bend:

        if testing_directionShift:
            if degrees_turned == 45:
                i = -1
        if testing_startingshift:
            start_bend += 1
        btCell.bend_cell(start_bend,i)
        degrees_turned += 1
        btCell.draw_polygon(True,start=start_bend,end=(len(btCell.vertices) - start_bend) + 1)

    # Checks collision and movement
    if (not paused) and testing_movement:
        mtCell2.translate_cell(True)
        mtCell.translate_cell(True)
        mtCell2.draw_polygon(True,True)
        mtCell.draw_polygon(True,True)

    # Checks rotation
    if (not paused) and testing_rotation:
        rCell.rotate_cell(0,len(rCell.vertices),rotate)
        degrees_rotated += rotate
        rCell.draw_polygon(True,True)

    # Does a small demonstration of current progress
    if (not paused) and demonstration_test:
        # print('here')
        ids = [[cell.cell_ID, cell.overlap, cell.topMost_yCoord, cell.rightMost_xCoord, cell.lowMost_yCoord, cell.leftMost_xCoord] for cell in Cell.list_of_cells]
        for cell in Cell.list_of_cells:
            cell.draw_polygon(True,False,True)
    # for j in range(151):
    #     pygame.draw.circle(screen,(0,0,255,), sperm.vertices[j],3)



    ######################  This Part resets the scene and puts time between each scene,  usually sleep(0.08) works smoothly
    # sleep(0.05)
    if not paused:
        pygame.display.update()
        screen.fill((30,30,30))
    if temp:
        paused = not paused
        temp = not temp

    clock.tick(fps)
    ######################
