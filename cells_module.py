import pygame
from math import cos, sin, radians, atan, pi, e, pow, sqrt
from random import randint
from time import sleep


# Creating cell Class
class Cell:
    list_of_cells = []
    listOf_cell_IDs = []
    current_cell_ID = 0

    def __init__(self):

        # temp vars
        self.removed = 0
        self.degree = 0
        self.midpoint = []
        self.pre_bend_start = []
        self.pre_bend_end = []
        self.bend_radius = 0
        self.lst_removed = []
        self.horizon_lst_removed = []

        self.x_pos = 0
        self.y_pos = 0

        self.rightMost_xCoord = []
        self.leftMost_xCoord = []
        self.topMost_yCoord = []
        self.lowMost_yCoord = []

        self.vertices = []

        # For circle specific cells
        self.radius = 0

        # For elliptical specific cells
        self.major_axis = 0
        self.minor_axis = 0

        self.overlap = False

        # For physics engine
        self.mass = 0
        self.x_acceleration = 0
        self.y_acceleration = 0
        self.x_velocity = 0
        self.y_velocity = 0

        self.red = randint(0,255)
        self.green = randint(0,255)
        self.blue = randint(0,255)
        # self.red = 80 + randint(1,30)
        # self.green = self.red
        # self.blue = self.red

        self.cell_ID = 0
        self.screen = 0

    def circular_cell(self,monitor,radius,x_pos,y_pos,creation_type="manual"):
        # Generates a circular base cell    

        # Saves data
        self.radius = radius
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = monitor

        self.cell_ID = Cell.current_cell_ID
        Cell.listOf_cell_IDs.append(self.cell_ID)
        Cell.current_cell_ID += 1

        #  It's at 360 and not 361, since 0 and 360 are the same so the number 360 does not need to be included 
        for i in range(360):
            # adds the x and y coordinate of the center of the circle to the x and y coordinates of the circle defined by the user's input
            x = x_pos + cos(radians(i)) * radius
            y = y_pos - sin(radians(i)) * radius

            # defines the vertices and appends them to the in-built list of the cell
            vertex = [x,y]
            self.vertices.append(vertex) 

        if creation_type != "auto":
            self.rightMost_xCoord = [self.vertices[0][0],self.vertices[0][1], 0]
            self.topMost_yCoord = [self.vertices[90][0],self.vertices[90][1], 90]
            self.leftMost_xCoord = [self.vertices[180][0], self.vertices[180][1], 180]
            self.lowMost_yCoord = [self.vertices[270][0], self.vertices[270][1], 270]
            self.overlap_checker()
            if self.overlap:
                return
            # Appends cell to total cell list
            Cell.list_of_cells.append(self)
        
        # Saves data to the cell object, to be used later in other functions

# When Back, make sure this makes a smooth bacillus shape
    def bacteria_cell(self,monitor,major_radius,minor_radius,x_pos,y_pos,left_smother_factor,right_smother_factor,creation_type="manual"):
        # Makes a bacillus shaped cell by making 2 lines and curves the edges with the final circle in the sequence

        # Saving important data : WIll 
        self.major_axis = major_radius*2
        self.minor_axis = minor_radius*2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = monitor

        self.cell_ID = Cell.current_cell_ID
        Cell.listOf_cell_IDs.append(self.cell_ID)
        Cell.current_cell_ID += 1

        # Setting the origins of the circles that will be used to round off the edges of the bacteria
        rightSide_circleOrigin = [x_pos + major_radius, y_pos]
        leftSide_circleOrigin = [x_pos - major_radius, y_pos]

        # Sets up the bacteria similar to a unit circle.  Starting from the far right and going counterclockwise until it reachs back at the same spot
        # Makes top right part of the round part of the bacillus shape
        for i in range(1,91):
            x = rightSide_circleOrigin[0] + cos(radians(i)) * minor_radius * right_smother_factor
            y = rightSide_circleOrigin[1] - sin(radians(i)) * minor_radius
            vertex = [x,y]
            self.vertices.append(vertex)

        # Makes the top straight line part of the bacillus shape
        for i in range(2*major_radius):
            x = x - 1
            vertex = [x,y]
            self.vertices.append(vertex)

        # Makes the entire left side of the round bacillus shape
        for i in range(90,270):
            x = leftSide_circleOrigin[0] + cos(radians(i)) * minor_radius * left_smother_factor
            y = leftSide_circleOrigin[1] - sin(radians(i)) * minor_radius
            vertex = [x,round(y,6)]
            self.vertices.append(vertex)

        # Makes the bottom straight line part of the bacillus shape
        for i in range(2*major_radius):
            x = x + 1
            vertex = [x,y]
            self.vertices.append(vertex)
        # Makes the bottom right part of the round part of the bacillus shape
        for i in range(271,360):
            x = rightSide_circleOrigin[0] + cos(radians(i)) * minor_radius * right_smother_factor
            y = rightSide_circleOrigin[1] - sin(radians(i)) * minor_radius
            vertex = [x,round(y,6)]
            self.vertices.append(vertex)

        if creation_type != 'auto':
            # Index of this is 0
            self.rightMost_xCoord = [self.vertices[0][0],self.vertices[0][1], 0]
            # Index of this is 180 + major_radius*2  
            self.leftMost_xCoord = [self.vertices[180 + major_radius*2][0], self.vertices[180 + major_radius*2][1], (180 + major_radius*2)]
            # Index of this is 90 + major_radius
            self.topMost_yCoord = [self.vertices[90 + major_radius][0], self.vertices[90 + major_radius][1], (90 + major_radius)]
            # Index of this is  270 + (3*major_radius)
            self.lowMost_yCoord = [self.vertices[270 + (3*major_radius)][0], self.vertices[270 + (3*major_radius)][1], (270 + (3*major_radius))]

            self.overlap_checker()
            if self.overlap:
                return
            # Appends cell to total cell list
            Cell.list_of_cells.append(self)

# This func will allow cells to bend/fold
    def bend_cell(self,start,degrees):

        end = len(self.vertices) - (start)
        
        if self.degree == 0:
            self.midpoint = [(self.vertices[start][0] + self.vertices[end][0])/2, (self.vertices[start][1] + self.vertices[end][1])/2 ]
            print(self.vertices[start],self.vertices[end])
            self.pre_bend_start = self.vertices[start]
            self.pre_bend_end = self.vertices[end]
            self.bend_radius = self.midpoint[1] - self.pre_bend_start[1]

        angle_A = degrees
        self.degree += degrees
        lst_removed = []

        glue_spot = start
        tear_spot = end + 1
        y_var = 1
        please = self.vertices[tear_spot][1] - self.midpoint[1]
        if degrees < 0:
            y_var = -1
            glue_spot = end - 1
            tear_spot = start - 1
            please = self.midpoint[1] - self.vertices[tear_spot][1]
        # start,end

        for i in range(start,end+1):

            graphvers = [self.vertices[i][0] - self.midpoint[0], self.midpoint[1] - self.vertices[i][1]]
            newX = graphvers[0] * cos(radians(angle_A)) - graphvers[1]*sin(radians(angle_A))
            newY = graphvers[0] * sin(radians(angle_A)) + graphvers[1]*cos(radians(angle_A))

            new_coord = [self.midpoint[0] + newX, self.midpoint[1] - newY]

            # Fix this so it can adjust for either bend, upward and downward in whatever orientation the cell is in.
            # if (new_coord[0] > self.vertices[tear_spot][0]) and (new_coord[1] < self.vertices[tear_spot][1]):
            #     if i not in lst_removed:
            #         lst_removed.append(i)
            # else:
            #     self.vertices[i] = new_coord
            if (newX > 0) and (abs(newY) < abs(please)):
                if i not in lst_removed:
                    lst_removed.append(i)
            else:
                self.vertices[i] = new_coord

        for num,i in enumerate(lst_removed,0):

            self.vertices.pop(i)

            graphvers = [self.pre_bend_start[0] - self.midpoint[0], self.midpoint[1] - self.pre_bend_start[1]]

            newX = graphvers[0] * cos(radians((-1)*(3.0*num))) - graphvers[1]*sin(radians((-1)*(3.0*num)))

            newY = graphvers[0] * sin(radians((-1)*(3.0*num))) + graphvers[1]*cos(radians((-1)*(3.0*num)))

            # change the self.midpoint[1] - newY to self.midpoint[1] + newY
            # I found the issue:  The start point does go forward in the normal bend but it is constantly pushed back, while in the negative bend, the start point(technically endpoint for the negative bend) only goes forward, without going back.
            new_vertice = [self.midpoint[0] - newX, self.midpoint[1] - y_var*newY]

            pygame.draw.circle(self.screen,(0,255,0),new_vertice,6)
            pygame.draw.circle(self.screen,(255,0,0),self.vertices[glue_spot],6)

            print(glue_spot)
            self.vertices.insert(glue_spot, new_vertice)
        #     added_list.append(new_vertice)

        # for i in range(len(lst_removed)):
        #     self.vertices.insert(start,added_list[i])

# NOT DONE:  I reckon I need to add a self.overlap_checker() here
# REALLY NOT DONE: Instead of using self.check_extremePoints(), I'm pretty sure I could just check the points nearest to the previous extreme points and see if they surpass it, making them the new extreme points.    NOOOO NEVERMIND, THIS WONT WORK
    def rotate_cell(self,start,end,degrees):

        origin = (self.x_pos, self.y_pos)
        print(self.vertices[start])
        # print(self.vertices[end])

        for index, vertex in enumerate(self.vertices[start:end]):
            graphVers_x = vertex[0] - origin[0]
            graphVers_y = -1*(vertex[1] - origin[1])

            new_x = graphVers_x*cos(radians(degrees)) - graphVers_y*sin(radians(degrees))
            new_y = graphVers_x*sin(radians(degrees)) + graphVers_y*cos(radians(degrees))

            new_vertex = [origin[0] + new_x, origin[1] - new_y]

            self.vertices[index] = new_vertex
        
        self.check_extremePoints()
        
    # When Back, try increasing the power of the parabola that makes the hill from 2 to 4, or to 6 , etc, to see if it makes the hill sharper.
    def make_hill(self, start, end, height, direction = "up",right_sharpness=0,left_sharpness=0):
        
        # The mathematical Principle I'm using here is rotation of graphs.  This function, mathematically, is simply rotating a slanted plane until the x-axis is horizontal, then creating a parabola, and then rotating the parabola from the horizontal x-axis back into the slanted(original) version.

        # Defines the x and y distance between the first and last point given
        x_dist = self.vertices[end][0] - self.vertices[start][0]
        # The computer flips the y-plane, so going down returns a higher y coordinate than going up, which is why I multiplied by -1
        y_dist = -1*(self.vertices[end][1] - self.vertices[start][1])

        # Defines the midpoint between the first and last point
        midpoint = [(self.vertices[start][0] + self.vertices[end][0])/2, (self.vertices[start][1] + self.vertices[end][1])/2 ]

        # Defines the distance of the start point from the midpoint, keep in mind this distance is equal to the distance of the end point from the midpoint as well
        graphVersionStart = [self.vertices[start][0] - midpoint[0],self.vertices[start][1] - midpoint[1]]

        # Defines the angle needed to rotate the graph by, which is angle_B
        try:
            angle_A =  atan(abs(y_dist/x_dist))
        except ZeroDivisionError:
            angle_A = pi/2
        angle_B = 2*pi - angle_A

        # Chooses the correct angle and positive/negative orientation of the parabola by using convex/concave lens geometry/logic
        # Here correct orientation for the parabola would be it sticking out of the cell and not inward.
        if x_dist < 0:
            orientation = -1
            if y_dist < 0:
                chosen_angle = angle_A
            else:
                chosen_angle = angle_B
        else:
            orientation = 1
            if y_dist < 0:
                chosen_angle = angle_B
            else:
                chosen_angle = angle_A
        
        # Changes the orientation of the parabola by the user's desire.  Up isn't included here since the parabola is already up by default
        if direction.lower() == "down":
            orientation = orientation * -1

        # Defines the start point given in the start but in the new rotated plane, where the x-axis is horizontal.
        normXStartpoint = graphVersionStart[0] * cos(chosen_angle)  -  graphVersionStart[1] * sin(chosen_angle)

        # Will make sure the right_sharpness and left_sharpness don't make a gap in the cell membrane
        # The 1, in the while loop, can be swapped to a lesser number to change the tightness of the cell membrane I want for the first and last points
        if right_sharpness:
            right_check = (2*height)/(1 + pow(e,right_sharpness*abs(normXStartpoint)))
            while right_check > 1:
                right_sharpness += 0.01
                right_check = (2*height)/(1 + pow(e,right_sharpness*abs(normXStartpoint)))

        if left_sharpness:
            left_check = (2*height)/(1 + pow(e,left_sharpness*abs(normXStartpoint)))
            while left_check > 1:
                left_sharpness += 0.01
                left_check = (2*height)/(1 + pow(e,left_sharpness*abs(normXStartpoint)))

        for i in range(1,end - start):
            
            # Already explained
            graphVers = [self.vertices[start + i][0] - midpoint[0], self.vertices[start + i][1] - midpoint[1]]
            normX = graphVers[0] * cos(chosen_angle)  -  graphVers[1] * sin(chosen_angle)


            # Creates the y coordinate in the rotated plan using a parabola equation
            parabolaY = orientation*(height/(normXStartpoint*normXStartpoint))*((normX)*(normX) - normXStartpoint*normXStartpoint)

            # Uses Sigmoid Function to create sharper hills and valleys
            if (normX <= 0) and right_sharpness:
                parabolaY = (-1*orientation*(2*height))/(1 + pow(e,(-1)*right_sharpness*normX))

            elif (normX > 0) and left_sharpness:
                parabolaY = -1*orientation*(2*height)/(1 + pow(e,left_sharpness*normX))
            
            # Rotates the coordinates in the horizontal x-axis plan into the slanted (original) plane
            newX = normX * cos(chosen_angle) - parabolaY * sin(chosen_angle)
            normParabolaY = normX * sin(chosen_angle) + parabolaY * cos(chosen_angle)



            # Puts the x and y coordinates together and switches them with their corresponding spot in the list of vertices for the cell
            sup_coord = [midpoint[0] + newX, midpoint[1] - normParabolaY]

            # Changes the declared extreme points of the cell if this function creates new ones, so that I can make an accurate proximity box later
            # IMPORTANT: DO NOT REPLACE THIS WITH self.checkExtremePoints, because it will waste a lot of time by checking the entire cell when all this is doing is checking the hill.

            # Changes all the assignments of the extremem points to include the third index number
            if sup_coord[0] > self.rightMost_xCoord[0]:
                self.rightMost_xCoord = [sup_coord[0],sup_coord[1],start + i]
            elif sup_coord[0] < self.leftMost_xCoord[0]:
                self.leftMost_xCoord = [sup_coord[0],sup_coord[1],start + i]
            
            if sup_coord[1] < self.topMost_yCoord[1]:
                self.topMost_yCoord = [sup_coord[0],sup_coord[1],start + i]
            elif sup_coord[1] > self.lowMost_yCoord[1]:
                self.lowMost_yCoord = [sup_coord[0],sup_coord[1],start + i]


            self.vertices[start+i] = sup_coord

    def random_cell(self,monitor, x_pos, y_pos, radius=0,ellipse=[0,0],height_depth_variation=[10,4],hill_valley_frequency=[5,5], width_range=[20,70],cell_type="circular"):

        #Creates a cell and skip_counter:  Skip_counter will be used to make sure this func doesn't create a hill on top another hill
        match cell_type:
            case "circular":
                self.circular_cell(monitor,radius,x_pos, y_pos)
            case "bacillus":
                self.bacteria_cell(monitor,ellipse[0],ellipse[1],x_pos,y_pos,1,1,creation_type="auto")
            case _:
                pass
        skip_counter = 0
        valley_chance = 0

        # Ends the function if the base cell already overlaps another cell
        # if self.overlap:
        #     return

        for i in range(len(self.vertices)):
            # does the skip_counter thing mentioned above
            if skip_counter > 0:
                skip_counter -= 1
                continue

            # generates the probabilty of one generating one hill
            make_hill_chance = randint(0,hill_valley_frequency[0])
            valley_chance = randint(0,hill_valley_frequency[1])

            # Makes sure that once its set to generate a hill, that the endpoint of the new hill doesn't exceed the list length of the cell vertices
            if make_hill_chance == 1:
                skip_counter = randint(width_range[0],width_range[1])

                if ((i + skip_counter) > 359) and (skip_counter < width_range[0]):
                    break
                elif ((i + skip_counter) > 359) and (skip_counter >= width_range[0]):
                    skip_counter = width_range[0]
                    if (i + skip_counter) > 359:
                        break

                endPoint = i + skip_counter
                hill_height = randint(1,height_depth_variation[0])

                self.make_hill(i,endPoint,hill_height)
            elif valley_chance == 1:

                skip_counter = randint(width_range[0],width_range[1])

                if ((i + skip_counter) > 359) and (skip_counter < width_range[0]):
                    break
                elif ((i + skip_counter) > 359) and (skip_counter >= width_range[0]):
                    skip_counter = width_range[0]
                    if (i + skip_counter) > 359:
                        break

                endPoint = i + skip_counter
                valley_depth = randint(1,height_depth_variation[1])

                self.make_hill(i,endPoint,valley_depth,"down")

        # Appends the newly made cell to the total list of cells in the Class if it doesn't overlap with another
        # SUPER IMPORTANT:                                       I reckon the check_extremePoints() function here is pointless since I already have it in the make_hills function but I have to test it.  If this is true then when I'm in the hill function I can just
        self.check_extremePoints()
        self.overlap_checker()
        if not self.overlap:
            Cell.list_of_cells.append(self)

    def translate_cell(self,active_acceleration):
        # Make it so that the velocites are only added to the extreme points first, check if they overlap with any cell, and go from there.
        self.leftMost_xCoord[0] += self.x_velocity
        self.rightMost_xCoord[0] += self.x_velocity
        self.topMost_yCoord[0] += self.x_velocity
        self.lowMost_yCoord[0] += self.x_velocity
        self.leftMost_xCoord[1] += self.y_velocity
        self.rightMost_xCoord[1] += self.y_velocity
        self.topMost_yCoord[1] += self.y_velocity
        self.lowMost_yCoord[1] += self.y_velocity

        self.overlap_checker()
        if self.overlap:
            self.leftMost_xCoord[0] -= self.x_velocity
            self.rightMost_xCoord[0] -= self.x_velocity
            self.topMost_yCoord[0] -= self.x_velocity
            self.lowMost_yCoord[0] -= self.x_velocity
            self.leftMost_xCoord[1] -= self.y_velocity
            self.rightMost_xCoord[1] -= self.y_velocity
            self.topMost_yCoord[1] -= self.y_velocity
            self.lowMost_yCoord[1] -= self.y_velocity
            self.x_velocity = 0
            self.y_velocity = 0

            # self.overlap = False
        else:
            # self.leftMost_xCoord[0] -= self.x_velocity
            # self.rightMost_xCoord[0] -= self.x_velocity
            # self.topMost_yCoord[0] -= self.x_velocity
            # self.lowMost_yCoord[0] -= self.x_velocity
            # self.leftMost_xCoord[1] -= self.y_velocity
            # self.rightMost_xCoord[1] -= self.y_velocity
            # self.topMost_yCoord[1] -= self.y_velocity
            # self.lowMost_yCoord[1] -= self.y_velocity
            for vertice in self.vertices:
                vertice[0] += self.x_velocity
                vertice[1] += self.y_velocity
        # if active_acceleration:
        #     self.x_velocity += self.x_acceleration
        #     self.y_velocity += self.y_acceleration
        
        # self.overlap_checker()
        # if self.overlap:
        #     self.x_velocity = (-1) * self.x_velocity
        #     self.y_velocity = (-1) * self.y_velocity
        

    def overlap_checker(self):

        # Checker to make sure no cells who overlap are made
        # Works by essentially creating proxmity boxes and checks if each cell is within that proximity box
        # HOLY HELL I FORGOT: THIS ISN'T DONE:  Once a cell is detected to be in the proximit box of another, I now need to manually check each of the vertices in that cell to see if the two cells actually touch.  The only reason I used proximity boxes was to save a lot of computational power and time.

        for cell in Cell.list_of_cells:
            
            if cell == self:
                continue
            
            if (cell.leftMost_xCoord[0] <= self.rightMost_xCoord[0] <= cell.rightMost_xCoord[0]):

                if (cell.topMost_yCoord[1] <= self.topMost_yCoord[1] <= cell.lowMost_yCoord[1]):
                    self.overlap = True
                    break
                
                elif (cell.topMost_yCoord[1] <= self.lowMost_yCoord[1] <= cell.lowMost_yCoord[1]):
                    self.overlap = True
                    break

            elif (cell.leftMost_xCoord[0] <= self.leftMost_xCoord[0] <= cell.rightMost_xCoord[0]):

                if (cell.topMost_yCoord[1] <= self.topMost_yCoord[1] <= cell.lowMost_yCoord[1]):
                    self.overlap = True
                    break
                
                elif (cell.topMost_yCoord[1] <= self.lowMost_yCoord[1] <= cell.lowMost_yCoord[1]):
                    self.overlap = True
                    break

        # for cell in Cell.list_of_cells:
            
        #     if cell == self:
        #         continue
            
        #     if (cell.leftMost_xCoord[0] <= self.rightMost_xCoord[0] <= cell.rightMost_xCoord[0]) or (cell.leftMost_xCoord[0] <= self.leftMost_xCoord[0] <= cell.rightMost_xCoord[0]):

                # if (self.topMost_yCoord[1] <= cell.topMost_yCoord[1] <= self.lowMost_yCoord[1]) or (self.topMost_yCoord[1] <= cell.lowMost_yCoord[1] <= self.lowMost_yCoord[1]):
                #     self.overlap = True
                #     break
                # elif (cell.topMost_yCoord[1] <= self.topMost_yCoord[1] <= cell.lowMost_yCoord[1]) or (cell.topMost_yCoord[1] <= self.lowMost_yCoord[1] <= cell.lowMost_yCoord[1]):
                #     self.overlap = True
                #     break

            # if (self.leftMost_xCoord[0] <= cell.rightMost_xCoord[0] <= self.rightMost_xCoord[0]) or (self.leftMost_xCoord[0] <= cell.leftMost_xCoord[0] <= self.rightMost_xCoord[0]):

            #     if (self.topMost_yCoord[1] <= cell.topMost_yCoord[1] <= self.lowMost_yCoord[1]) or (self.topMost_yCoord[1] <= cell.lowMost_yCoord[1] <= self.lowMost_yCoord[1]):
            #         self.overlap = True
            #         break
            #     elif (cell.topMost_yCoord[1] <= self.topMost_yCoord[1] <= cell.lowMost_yCoord[1]) or (cell.topMost_yCoord[1] <= self.lowMost_yCoord[1] <= cell.lowMost_yCoord[1]):
            #         self.overlap = True
            #         break

    def check_extremePoints(self,start=0,end=0):
        # Changes the declared extreme points of the cell if the function creates new ones, so that I can make an accurate proximity box later
        # Use this typically to check the entire cell at once, it is possible to check small sections of the cell but this can be glitchy and prone to error, so be cautious if used for small sections of the cell instead of the whole thing at once.
        if not end:
            end = len(self.vertices) 

        self.rightMost_xCoord = [self.x_pos,self.y_pos]
        self.leftMost_xCoord = [self.x_pos,self.y_pos]
        self.topMost_yCoord = [self.x_pos,self.y_pos]
        self.lowMost_yCoord = [self.x_pos,self.y_pos]

        # Changing self.vertices[start:end] to self.vertices

        for i,vertex in enumerate(self.vertices):
            if vertex[0] > self.rightMost_xCoord[0]:
                self.rightMost_xCoord = [vertex[0],vertex[1],i]
            elif vertex[0] < self.leftMost_xCoord[0]:
                self.leftMost_xCoord = [vertex[0],vertex[1],i]
            
            if vertex[1] < self.topMost_yCoord[1]:
                self.topMost_yCoord = [vertex[0],vertex[1],i]
            elif vertex[1] > self.lowMost_yCoord[1]:
                self.lowMost_yCoord = [vertex[0],vertex[1],i]

    def draw_polygon(self,show_vertices=False,show_proximityBox=False,start=0,end=0,thickness=1):

        # Doesn't draw the cell if it overlaps with another cell
        # if self.overlap:
        #     return
        # Actually puts the cell on the screen
        pygame.draw.polygon(self.screen,(self.red,self.green,self.blue),self.vertices)
        
        # Makes small bubbles on each vertice of the cell, which makes it look as if the cell has a membrane of sorts.
        # I'm swapping the red, green, and blue order in the tuple, so that the perimeter of the cell isn't the same color as the inside of the cell
        if show_vertices:
            for i in range(len(self.vertices)):
                # pygame.draw.circle(screen,(255 - self.red, 255 - self.green, 255 - self.blue),(self.vertices[i][0],self.vertices[i][1]),thickness)
                pygame.draw.circle(self.screen,(250,250,250),(self.vertices[i][0],self.vertices[i][1]),thickness)
        
        # Makes a little box surrounding the cell, which represents the cell's proximity box
        if show_proximityBox:
            topLeftCorner = [self.leftMost_xCoord[0],self.topMost_yCoord[1]]
            topRightCorner = [self.rightMost_xCoord[0],self.topMost_yCoord[1]]
            bottomRightCorner = [self.rightMost_xCoord[0],self.lowMost_yCoord[1]]
            bottomLeftCorner = [self.leftMost_xCoord[0],self.lowMost_yCoord[1]]
            proximity_box = [topLeftCorner,topRightCorner,bottomRightCorner,bottomLeftCorner]

            pygame.draw.polygon(self.screen,(255,255,255),proximity_box,thickness)

        # Makes a secant in the cell connecting any two points of the cell.
        if start and end:
            pygame.draw.line(self.screen,(255 - self.red,255 - self.green,255 - self.blue),self.vertices[start],self.vertices[end],thickness)

