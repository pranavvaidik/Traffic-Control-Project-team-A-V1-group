#!/usr/bin/python

import pygame
import os
import time
import random
import importlib
import csv
import numpy as np
import sys

from Traffic_signal   import Traffic_signal,get_state,calc_reward,update_vehicles,epsilon_greedy,update_q_learning,car_tracing

# Code by Hameed Start
def set_traffic_lights(traffic_lights):

	i=-1 #index iterating over traffic nodes
	for l in traffic_lights:#yet to define variable traffic_lights, would be receiving from I team	
		for direction in l:
			i+=1
			if direction==None:
				#print('No green light')
				center = coordinate_transform(traffic_nodes[i])
		        	pygame.draw.circle(screen, colors['red'], center, block_size/2, 0)
				continue
			elif direction[:1].upper()=='N': #if North
				direction_image=direction_images['North']				
			elif direction[:1].upper()=='E': #if East
				direction_image=direction_images['East']
			elif direction[:1].upper()=='W': #if West
				direction_image=direction_images['West']
			elif direction[:1].upper()=='S': #if South
				direction_image=direction_images['South']
			else:
				raise Exception('Invalid direction')
				
			
			screen.blit(direction_image, coordinate_transform(  tuple(np.array(traffic_nodes[i]) - np.array([0.5,-0.5]))  )) ##need to transform traffic_nodes[i]        
	return


block_size = int(sys.argv[1])

dir_img_size=(block_size,block_size)

direction_images={
		'North':pygame.transform.smoothscale(pygame.image.load('images/North.png'),dir_img_size),
		'South':pygame.transform.smoothscale(pygame.image.load('images/South.png'),dir_img_size),
		'East':pygame.transform.smoothscale(pygame.image.load('images/East.png'),dir_img_size),
		'West':pygame.transform.smoothscale(pygame.image.load('images/West.png'),dir_img_size)
		}
		
#########      End          ########



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
    
car_colors = {
        #'black'   : (  0,   0,   0),
        'white'   : (255, 255, 255),
        'red'     : (255,   0,   0),
        'green'   : (  0, 255,   0),
        #'dgreen'  : (  0, 228,   0),
        'blue'    : (  0,   0, 255),
        'cyan'    : (  0, 200, 200),
        'magenta' : (200,   0, 200),
        'yellow'  : (255, 255,   0),
        #'mustard' : (200, 200,   0),
        'orange'  : (255, 128,   0),
        #'maroon'  : (200,   0,   0),
        #'crimson' : (128,   0,   0),
        #'gray'    : (155, 155, 155)
    }


pygame.init()



n_blocks = (69,69)

#size = (900,900)
size = ((n_blocks[0] + 15 )* block_size, (n_blocks[1]+15)*block_size)
screen = pygame.display.set_mode(size,pygame.RESIZABLE)
done = False

bg_color = colors['gray']
boundary_color = colors['black']
road_color = colors['black']
road_width = 20





bounds = (5,10,69,69)

def coordinate_transform(point_tuple):
	# takes in coordinate in the road coordinates and converts them to pygame version
	
	
	transformed_x = (bounds[0] + point_tuple[0] + 3 + 0.5)*block_size
	
	
	transformed_y = (bounds[1] + bounds[3] -3 - point_tuple[1] - 0.5)*block_size
	
	return (int(transformed_x), int(transformed_y))


def place_vehicle(agent):
	
	# takes in the location of the car and gives out the location on the UI
	
	slot = agent.location[0]
	road_segment = agent.location[1]
	
	# get the direction of movement of the vehicle
	direction = np.subtract(road_segment[1],road_segment[0])
	length = np.linalg.norm(direction)
	
	car_location = coordinate_transform(tuple(np.array(road_segment[0]) - np.array([0.5,-0.5]) + (slot + 1) * (direction/length)  + np.flip(direction/length) * (0.25 if direction[0] == 0 else -0.25) ))
	
	if hasattr(agent, '_sprite'):
		rotated_sprite = agent._sprite if tuple(direction/length) == (1,0) else pygame.transform.rotate(agent._sprite, 180 if tuple(direction/length) == (-1,0)  else tuple(direction/length)[1]*90 )
	
	
	return car_location, rotated_sprite
	

# nodes and road segments
nodes = [(62,65), (-3,62), (0,62), (31,62), (62,62), (0,31), (31,31), (62,31), (0,0), (31,0), (62,0), (65,0), (0,-3)]
exit_nodes = [(62,65),(-3,62),(0,-3),(65,0)]
#traffic_nodes=[x for x in nodes if x not in exit_nodes]
traffic_nodes=[(0,0), (31,0), (62,0),(0,31),(31,31),(62,31),(0,62),(31,62),(62,62)]



#traffic lights - call them here if necessary
traffic_lights = [['NORTH','NORTH','EAST'],['NORTH',None,'SOUTH'],['SOUTH','EAST','WEST']]

road_segments = dict()
		
#initializing the entry/exit road segments
road_segments[((-3,62),(0,62))] = [None]*2
road_segments[((0,62),(-3,62))] = [None]*2

road_segments[((62,65),(62,62))] = [None]*2
road_segments[((62,62),(62,65))] = [None]*2
		
road_segments[((62,0),(65,0))] = [None]*2
road_segments[((65,0),(62,0))] = [None]*2

road_segments[((0,0),(0,-3))] = [None]*2
road_segments[((0,-3),(0,0))] = [None]*2
		
#initializing the rest of the road segments
road_segments[((0,62),(31,62))] = [None]*30	
road_segments[((31,62),(0,62))] = [None]*30
		
road_segments[((62,62),(31,62))] = [None]*30	
road_segments[((31,62),(62,62))] = [None]*30

road_segments[((0,62),(0,31))] = [None]*30	
road_segments[((0,31),(0,62))] = [None]*30
		
road_segments[((31,31),(31,62))] = [None]*30	
road_segments[((31,62),(31,31))] = [None]*30
		
road_segments[((62,62),(62,31))] = [None]*30	
road_segments[((62,31),(62,62))] = [None]*30
		
road_segments[((0,31),(31,31))] = [None]*30	
road_segments[((31,31),(0,31))] = [None]*30
		
road_segments[((31,31),(62,31))] = [None]*30	
road_segments[((62,31),(31,31))] = [None]*30
		
road_segments[((0,31),(0,0))] = [None]*30	
road_segments[((0,0),(0,31))] = [None]*30
		
road_segments[((31,31),(31,0))] = [None]*30	
road_segments[((31,0),(31,31))] = [None]*30
		
road_segments[((62,0),(62,31))] = [None]*30	
road_segments[((62,31),(62,0))] = [None]*30
		
road_segments[((31,0),(0,0))] = [None]*30	
road_segments[((0,0),(31,0))] = [None]*30
		
road_segments[((31,0),(62,0))] = [None]*30	
road_segments[((62,0),(31,0))] = [None]*30




#print road_segments.keys()

unique_roads = []


for road in road_segments.keys():
	if tuple(reversed(road)) not in unique_roads:
		unique_roads.append(road)






#creating some dummy agent class for testing purposes
class Agent():
	location = None
	color = None
	ID = None


agent_list = []
i = 400
for road in road_segments.keys():
	agent = Agent()
	agent.color = random.choice(car_colors.keys()) #'white'
	agent.location = (0, road)
	agent.ID = i
	agent._sprite = pygame.transform.smoothscale(pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), (block_size,block_size))
	road_segments[agent.location[1]][agent.location[0]] = agent.ID
	agent_list.append(agent)
	i = i+1
	

#I group code
get_traffic_signal = {}

#Sample dictionary received from V group --> Remove this after integration with V group code
vehicle_id =         {'[0,0],[0,31]':['V_0',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,0],[0,-3]':[0,0],\
		      '[0,0],[31,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,-3],[0,0]':['V_9',0],\
		      '[31,0],[0,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,0],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,0],[62,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[31,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[62,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[65,0]':[0,0],\
		      '[65,0],[62,0]':[0,0],\
		      '[62,31],[62,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,31],[62,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,31],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,62],[31,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,62],[62,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'V_10',0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,62],[62,65]':[0,0],\
		      '[62,65],[62,62]':[0,'V_8'],\
		      '[31,62],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,62],[62,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,62],[0,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,62],[0,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,62],[-3,62]':[0,0],\
		      '[0,62],[31,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[-3,62],[0,62]':[0,0],\
	              '[0,31],[0,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,31],[0,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,31],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,31],[31,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,31],[0,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,31],[31,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,31],[62,31]':[0,'V_2',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		    }


# Top most signals (location, adjacent roads, signal_direction(N,S,E,W))
get_traffic_signal[7] = Traffic_signal([0,62], [] ,[0,1,1,1])
get_traffic_signal[8] = Traffic_signal([31,62], [],[0,1,1,1])
get_traffic_signal[9] = Traffic_signal([62,62], [],[1,1,0,1])
#
##Signals in the middle
get_traffic_signal[4] = Traffic_signal([0,31], [],[1,1,1,0])
get_traffic_signal[5] = Traffic_signal([31,31],[],[1,1,1,1])
get_traffic_signal[6] = Traffic_signal([62,31],[],[1,1,0,1])
#
##Bottom most signals
get_traffic_signal[1] = Traffic_signal([0,0], [],[1,1,1,0])
get_traffic_signal[2] = Traffic_signal([31,0],[],[1,0,1,1])
get_traffic_signal[3] = Traffic_signal([62,0],[],[1,0,1,1])

red_signal_violation_count = 0
collisions_count = 0
current_state = {}
action = {}
green_light  = ['NORTH','NORTH','EAST','NORTH',None,'SOUTH','SOUTH','EAST','WEST']
t = 1

def step(t):

        global red_signal_violation_count,collisions_count,green_light
	
        #emulating a time step

        # Change Traffic light every 2s
        if t % 2 == 0:
          green_light = []
          
          for i in range(1,10):
      
            TL = get_traffic_signal[i]
      
            current_state[i] = get_state(TL)
      
            action[i] = epsilon_greedy(TL.Q,current_state[i],TL.action_list,TL.epsilon) 
        
            TL.signal = action[i]
      
            #Update traffic lights 
            if 'G' in action[i]:
                if action[i][0] == 'G' : direction = 'NORTH'
                if action[i][1] == 'G' : direction = 'SOUTH'
                if action[i][2] == 'G' : direction = 'EAST'
                if action[i][3] == 'G' : direction = 'WEST'
            else:
                direction = None
      
            green_light.append(direction)
      
        #Vehicle movement
	for agent in agent_list:
	
		if agent.location[0] + 1 < len(road_segments[agent.location[1]]):
			agent.location = (agent.location[0]+1, agent.location[1])
		else:
			agent.location = (0, agent.location[1])

        # Execute this every timestep after vehicle movement
        for i in range(1,10):
          
           TL = get_traffic_signal[i]
         
           #Update adjacent roads variable from info received from V group
           update_vehicles(TL,vehicle_id)
           
           #check for red signal violation
           red_signal_violation = TL.check_signal_violation()

           for n in range(0,len(red_signal_violation)):
               if red_signal_violation[n] == 1:
                   red_signal_violation_count+=1
           
           #check for collisions
           no_collisions = TL.check_collision_at_signal()
           collisions_count+=1
          
           #Update vehicle queue and counter associated with it to calculate waiting time
           TL.update_queue()
          
           next_state = get_state(TL)

           #Calculate reward
           reward = calc_reward(TL, no_collisions)    
        
           #update Q values based on reward, s, a
           s_a = (current_state[i],action[i])
           TL.Q[s_a] = update_q_learning(TL.alpha,TL.gamma,TL.Q, current_state[i], action[i], reward, next_state) 
     
           #TODO : throughput calculation


while not done:

        #increment timestep
        t += 1

	# Reset the screen.
        screen.fill(bg_color)
        
        
        
        # Draw elements
        # * Static elements

	
        
        # TODO: convert the rect boundaries to a math term dependent on parameters from env 
        pygame.draw.rect(screen, boundary_color, ( bounds[0]*block_size, bounds[1]*block_size, bounds[2]*block_size, bounds[3]*block_size), 4)
        
        
        # iteration over roads to draw the roads and separation lines
        for road in unique_roads:
        
        	# transforming road points
        	road_start = coordinate_transform(road[0])
        	road_end = coordinate_transform(road[1])
        	
        	# drawing the roads 
        	pygame.draw.line(screen, road_color, road_start, road_end, road_width)
        	
        	# drawing the separation lines
        	pygame.draw.line(screen, colors['white'], road_start, road_end, 1)
        
        # Highlight the traffic nodes with yellow circles
        
        for node in traffic_nodes:
        	center = coordinate_transform(node)
        	pygame.draw.circle(screen, colors['yellow'], center, block_size/2, 0)
        
        # Highlight the exit nodes with green circles
        for node in exit_nodes:
        	center = coordinate_transform(node)
        	pygame.draw.circle(screen, colors['green'], center, block_size/2, 0)
        	
        # Add traffic light directions on the map
        traffic_lights = [[green_light[0],green_light[1],green_light[2]],[green_light[3],green_light[4],green_light[5]],[green_light[6],green_light[7],green_light[8]]]
        set_traffic_lights(traffic_lights)
	
        # Add Dynamic elements from here on
	
	
	for agent in agent_list:
		car_location, rotated_sprite = place_vehicle(agent)
		screen.blit(rotated_sprite, car_location)
	
	
	
	# everything in the loop should be in the render function, which is called in a while loop at every time instance
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
	
	
	pygame.time.delay(500)	
	
        step(t)
	        
        pygame.display.flip()



	


