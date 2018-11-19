import pygame
import os
import time
import random
import importlib
import csv


colors = {
        'black'   : (  0,   0,   0),
        'white'   : (255, 255, 255),
        'red'     : (255,   0,   0),
        'green'   : (  0, 255,   0),
        'dgreen'  : (  0, 228,   0),
        'blue'    : (  0,   0, 255),
        'cyan'    : (  0, 200, 200),
        'magenta' : (200,   0, 200),
        'yellow'  : (255, 255,   0),
        'mustard' : (200, 200,   0),
        'orange'  : (255, 128,   0),
        'maroon'  : (200,   0,   0),
        'crimson' : (128,   0,   0),
        'gray'    : (155, 155, 155)
    }

pygame.init()


block_size = 20

n_blocks = (69,69)

#size = (900,900)
size = ((n_blocks[0] + 15 )* block_size, (n_blocks[1]+15)*block_size)
screen = pygame.display.set_mode(size)
done = False

bg_color = colors['gray']
boundary_color = colors['black']
road_color = colors['black']
road_width = 20



bounds = (5,10,69,69)



while not done:
	
	# Reset the screen.
        screen.fill(bg_color)
        
        
        
        # Draw elements
        # * Static elements

	# rect = ((self.env.bounds[0] - self.env.hang)*self.env.block_size, (self.env.bounds[1]-self.env.hang)*self.env.block_size, (self.env.bounds[2] + self.env.hang/3)*self.env.block_size, (self.env.bounds[3] - 1 + self.env.hang/3)*self.env.block_size)
        # Boundary
        
        # TODO: convert the rect boundaries to a math term dependent on parameters from env 
        pygame.draw.rect(screen, boundary_color, ( bounds[0]*block_size, bounds[1]*block_size, bounds[2]*block_size, bounds[3]*block_size), 4)
        
        #pygame.draw.line(screen, road_color, ( bounds[1]*block_size, (bounds[0]+2)*block_size), ((bounds[1] + bounds[3] - 2)*block_size, (bounds[0]+2)*block_size), block_size) # replace 4th argument with road_width
        
        
        pygame.draw.line(screen, road_color,  ( bounds[0]*block_size, (bounds[1]+4)*block_size ) , ( (bounds[0] + bounds[2] - 3)*block_size , (bounds[1] + 4)*block_size ), road_width )
        pygame.draw.line(screen, colors['white'], ( bounds[0]*block_size, (bounds[1]+4)*block_size ) , ( (bounds[0] + bounds[2] - 3)*block_size , (bounds[1] + 4)*block_size ), 1)
        
        pygame.draw.line(screen, road_color,  ( (bounds[0] + bounds[3] - 3)*block_size , bounds[1]*block_size ) , ( (bounds[0] + bounds[3] - 3)*block_size , (bounds[1] + bounds[3] - 3 )*block_size ), road_width )
        pygame.draw.line(screen, colors['white'], ( (bounds[0] + bounds[3] - 3)*block_size , bounds[1]*block_size ) , ( (bounds[0] + bounds[3] - 3)*block_size , (bounds[1] + bounds[3] - 3 )*block_size ), 1)
        
        
        
        
        #pygame.draw.rect(screen, boundary_color, ( bounds[0]*block_size, bounds[1]*block_size, block_size, block_size), 4)
        
        
        
        
        
        pygame.draw.line(screen, colors['white'], (50, 100), (50, 100), 1) # points are given as (column, row), with (0,0) at the top left
        
        
        
        

	# everything in the loop should be in the render function, which is called in a while loop at every time instance
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        pygame.display.flip()



