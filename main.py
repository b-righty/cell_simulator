import pygame
from time import sleep
from math import cos, sin, radians, atan, pi
from random import randint
from cells_module import Cell


pygame.init()

screen = pygame.display.set_mode((900,700))
running = True
# Background
screen.fill((30,30,30))

# progenitor = Cell()

# bacillus cells
# for i in range(1):
#     progenitor = Cell()
#     progenitor.bacteria_cell(100,50,randint(400,400),randint(300,300))
    # progenitor.random_cell(randint(50,800),randint(40,600), major_axis=10, minor_axis=5, height_variation= 1, depth_variation=1, hill_frequency=0, allow_valleys=True, valley_frequency=40, smallest_width=1,biggest_width=2,cell_type='bacillus' )
    # progenitor.rotate_cell(randint(10,179))
    # progenitor.draw_polygon()


# circular cells
# for i in range(20):
#     progenitor = Cell()
#     progenitor.random_cell(randint(40,800),randint(40,600),radius=30,height_variation=6,depth_variation=6, hill_frequency=3,allow_valleys=True,valley_frequency=3,smallest_width=5,biggest_width=20,cell_type="circular")
#     progenitor.draw_polygon(True)

# Making a sort of sperm cell,  or cell with a tail and head.
sperm = Cell()
# sperm.circular_cell(screen,30,400,300)
sperm.bacteria_cell(screen,60,20,400,300,1,1)

# for i in range(50):
#     sperm.bend_cell(150,i)
#     sperm.draw_polygon()


# for i in range(2):
    
#     angle_A = -20*i

#     dot1 = [60,40]
#     dot2 = [60,80]
#     midpoint = [60,60]
#     dot1x = 0*cos(radians(angle_A)) - 20*sin(radians(angle_A))
#     dot1y = 0*sin(radians(angle_A)) + 20*cos(radians(angle_A))

#     dot1 = [midpoint[0] + dot1x, midpoint[1] - dot1y]

#     dot2x = 0*cos(radians(angle_A)) - (-20)*sin(radians(angle_A))
#     dot2y = 0*sin(radians(angle_A)) + (-20)*cos(radians(angle_A))

#     dot2 = [midpoint[0] + dot2x, midpoint[1] - dot2y]

#     pygame.draw.line(screen,(255,0,0),dot1,dot2,1)
#     pygame.draw.circle(screen,(0,255,0),dot1,1)
#     pygame.draw.circle(screen,(0,255,0),dot2,1)




# sperm.rotate_cell(180,((sperm.major_axis*2 + 360) - 181), 10)
# sperm.make_hill(30,60,20,right_sharpness=0.3,left_sharpness=0.5)
# 100, 260
# Higher sharpness number makes the curve tighter    Left and Right refer to parabola's left/right
# sperm.make_hill(30,150,30)
# sperm.make_hill(60,120,30)
# sperm.make_hill(75,105,15)
# sperm.random_cell(randint())
# sperm.draw_polygon(True)

# good_cell = Cell()
# good_cell.random_cell(randint(20,60),randint(40,800),randint(40,600),randint(10,15),randint(5,20),True)

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


# cell_list = []

#  Creates a certain amount of random cells
# for i in range(20):
#     temp_cell = Cell()
#      CHANGE arguments in random_cell
#     temp_cell.random_cell(randint(10,40),randint(40,800),randint(40,600),randint(5,15),randint(5,20),True)
#     temp_cell.draw_polygon(True,True)
#     cell_list.append(temp_cell)

# sperm.bend_cell(150,45)
# sperm.draw_polygon(True,start=150,end=len(sperm.vertices) - 150)

play = True
i = 1
while running:

    # Allows for user to click x on top right of gui and close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play
    
    # for i in range(len(cell_list)):
    #     cell_list[i].rotate_cell(1)
    #     cell_list[i].draw_polygon(True,True)
    #  Makes all the cells move randomly
    # Makes a cool looking effect if you don't reset the screen
    # for i in range(len(Cell.list_of_circular_cells)):
    #     change_x = randint(-3,3)
    #     change_y = randint(-3,3)

    #     for vertice in Cell.list_of_circular_cells[i].vertices:
    #         vertice[0] += change_x
    #         vertice[1] += change_y
        
    #     Cell.list_of_circular_cells[i].draw_polygon(True,True)


    # Rotates the cell
    # sperm.rotate_cell(2)
    # sperm.draw_polygon(True,True)

        #Make a consume_cell function in the class where it makes one cell disappear and gives half the radius of the consumed cell to the consumer cell, this may require making radius an instataneaous value if I want to make it in the most efficient way but I don't have to.

    sperm.bend_cell(150,i)
    sperm.draw_polygon(True,start=150,end=len(sperm.vertices) - 150)

    # for j in range(151):
    #     pygame.draw.circle(screen,(0,0,255,), sperm.vertices[j],3)


    pygame.display.update()

    ######################  This Part resets the scene and puts time between each scene,  usually sleep(0.08) works smoothly
    sleep(0.5)
    screen.fill((30,30,30))
    ######################
