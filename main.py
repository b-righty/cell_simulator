import pygame
from time import sleep
from math import cos, sin, radians, atan, pi
from random import randint,uniform
from cells_module import Cell

# something to consider, using quaternions to make this 3D

pygame.init()

# Creating Window & Sets game/simulator to run
screen = pygame.display.set_mode((900,700))
running = True
# Frame Rate
clock = pygame.time.Clock()
fps = 10
# Background
screen.fill((30,30,30))

# List of Tests
testing_bend = False
btCell = 0
i = 0
testing_movement = False
mtCell = 0


def bend_test(degrees):
    btCell = Cell()
    btCell.bacteria_cell(screen,60,20,400,300,1,1)
    testing_bend = True
    return btCell, testing_bend, degrees
#btCell, testing_bend, i = bend_test(1,3)

def movement_test():
    mtCell = Cell()
    mtCell.circular_cell(screen,60,320,400)
    mtCell.x_velocity = 0
    mtCell.y_velocity = -1
    mtCell.x_acceleration = 0
    mtCell.y_acceleration = 0
    mtCell2 = Cell()
    mtCell2.circular_cell(screen,60, 400, 200)
    mtCell2.x_velocity = 0
    mtCell2.y_velocity = 1
    mtCell2.x_acceleration = 0
    mtCell2.y_acceleration = 0
    testing_movement = True
    return mtCell, mtCell2, testing_movement,
mtCell, mtCell2, testing_movement = movement_test()



# Make a collision detection system
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
    
    # Rotates all cells in list_of_cells
    # for i in range(len(Cell.list_of_cells)):
    #     if i % 2 == 1:
    #         Cell.list_of_cells[i].rotate_cell(0,len(Cell.list_of_cells[i].vertices),1+(i/100))
    #     else:
    #         Cell.list_of_cells[i].rotate_cell(0,len(Cell.list_of_cells[i].vertices),-1+(i/100))
    #     Cell.list_of_cells[i].draw_polygon(True,True)
        
    #  Makes all the cells move randomly
    # Makes a cool looking effect if you don't reset the screen
    # for i in range(len(Cell.list_of_cells)):
    #     change_x = randint(-3,3)
    #     change_y = randint(-3,3)

    #     for vertice in Cell.list_of_cells[i].vertices:
    #         vertice[0] += change_x
    #         vertice[1] += change_y
        
    #     Cell.list_of_cells[i].draw_polygon(True,True)


    # Make cell bend
    if not paused and testing_bend:
        btCell.bend_cell(150,i)
        # sperm.draw_polygon(True)
        btCell.draw_polygon(True,start=150,end=(len(btCell.vertices) - 150) + 1)
        
    if not paused and testing_movement:
        mtCell2.translate_cell(True)
        mtCell.translate_cell(True)
        mtCell2.draw_polygon(True,True)
        mtCell.draw_polygon(True,True)


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
