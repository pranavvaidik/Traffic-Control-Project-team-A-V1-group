import pygame
import os
import time
import random
import importlib
import csv
import numpy as np
import sys


class Simulator():
	
	# colors for identification
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
       	'white'   : (255, 255, 255),
       	'red'     : (255,   0,   0),
       	'green'   : (  0, 255,   0),
       	'blue'    : (  0,   0, 255),
       	'cyan'    : (  0, 200, 200),
       	'magenta' : (200,   0, 200),
       	'yellow'  : (255, 255,   0),
       	'orange'  : (255, 128,   0),
            }
            
	
	def __init__(self,env, update_delay=0.5, display=True):
		
		self.env = env
		
		self.unique_roads = []
		for road in self.env.road_segments.keys():
			if tuple(reversed(road)) not in self.unique_roads:
				self.unique_roads.append(road)

		
		
		
		
		self.update_delay = update_delay
		
		
		self.bg_color = self.colors['gray']
		self.boundary_color = self.colors['black']
		self.road_color = self.colors['black']
		self.road_width = 20
		self.bounds = (5,10,self.env.n_blocks[0],self.env.n_blocks[1])
		
		self.quit = False
        	self.start_time = None
        	self.current_time = 0.0
        	self.last_updated = 0.0
		
		
		# This is for simulation purposes, not to be touched yet
		self.display = display
		
		
		if self.display:
	            	#try:
        	    	self.pygame = importlib.import_module('pygame')
        		self.pygame.init()
        	        self.size = ((self.env.n_blocks[0] + 15 )* self.env.block_size, (self.env.n_blocks[1]+15)*self.env.block_size)
        	        self.screen = self.pygame.display.set_mode(self.size)
			
			self.block_size = self.env.block_size
			
			self.dir_img_size=(self.block_size,self.block_size)
				
			self.direction_images={
					'NORTH':self.pygame.transform.smoothscale(pygame.image.load('images/North.png'),self.dir_img_size),
					'SOUTH':self.pygame.transform.smoothscale(pygame.image.load('images/South.png'),self.dir_img_size),
					'EAST':self.pygame.transform.smoothscale(pygame.image.load('images/East.png'),self.dir_img_size),
					'WEST':self.pygame.transform.smoothscale(pygame.image.load('images/West.png'),self.dir_img_size)
					}
				
				
        	        #self._ew = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "east-west.png")), (self.road_width, self.road_width))
        	        #self._ns = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "north-south.png")), (self.road_width, self.road_width))
		
        	        self.frame_delay = max(1, int(self.update_delay * 1000))  # delay between GUI frames in ms (min: 1)
        	        self.agent_sprite_size = (self.block_size, self.block_size)
        	        #self.primary_agent_sprite_size = (42, 42)
        		        
        	        #self.agent_circle_radius = 20  # radius of circle, when using simple representation
        		        
			print "agent list is ", len(self.env.agent_list_start), " long"
        		        
        	        for agent in self.env.smart_agent_list_start:
        	        	agent.color = random.choice(self.env.car_colors.keys())
        	            	agent._sprite = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), self.agent_sprite_size)
        	            	agent._sprite_size = (agent._sprite.get_width(), agent._sprite.get_height())
        	            	print "this was run atleast once"
			
        	        for agent in self.env.dummy_agent_list_start:
        	        	agent.color = random.choice(self.env.car_colors.keys())
        	            	agent._sprite = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), self.agent_sprite_size)
        	            	agent._sprite_size = (agent._sprite.get_width(), agent._sprite.get_height())
        	            	print "this was run atleast once"
						
			
        	        self.font = self.pygame.font.Font(None, 20)
        	        self.paused = False
       		#	except ImportError as e:
        	#	        self.display = False
        	#	        print "Simulator.__init__(): Unable to import pygame; display disabled.\n{}: {}".format(e.__class__.__name__, e)
   		#	except Exception as e:
   		#	        self.display = False
        	#		print "Simulator.__init__(): Error initializing GUI objects; display disabled.\n{}: {}".format(e.__class__.__name__, e)

		
		
        	print( "The length of the list is ", len(self.env.smart_agent_list_start))
		
		return
	
	
	def set_traffic_lights(self,traffic_lights):
		
		
		
		for loc in traffic_lights.keys():
			
			if traffic_lights[loc] == None:
				center = self.coordinate_transform(loc)
		        	pygame.draw.circle(self.screen, self.colors['red'], center, self.block_size/2, 0)
			else:
				dir_sprite = self.direction_images[traffic_lights[loc]] 
				self.screen.blit(dir_sprite, self.coordinate_transform(  tuple(np.array(loc) - np.array([0.5,-0.5]))  )) ##need to transform traffic_nodes[i]        				
		
		
		"""i=-1 #index iterating over traffic nodes
		for l in traffic_lights:#yet to define variable traffic_lights, would be receiving from I team	
			for direction in l:
				i+=1
				if direction==None:
					#print('No green light')
					center = self.coordinate_transform(self.traffic_nodes[i])
			        	pygame.draw.circle(self.screen, self.colors['red'], center, self.block_size/2, 0)
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
					
				
				self.screen.blit(direction_image, self.coordinate_transform(  tuple(np.array(traffic_nodes[i]) - np.array([0.5,-0.5]))  )) ##need to transform traffic_nodes[i] """       
		return
	
	
	def coordinate_transform(self, point_tuple):
		# takes in coordinate in the road coordinates and converts them to pygame version
		transformed_x = (self.bounds[0] + point_tuple[0] + 3 + 0.5)*self.block_size
		transformed_y = (self.bounds[1] + self.bounds[3] -3 - point_tuple[1] - 0.5)*self.block_size
		return (int(transformed_x), int(transformed_y))


	def place_vehicle(self,agent):
		# takes in the location of the car and gives out the location on the UI
		
		road_segment = agent.location[1]
		slot = len(self.env.road_segments[road_segment]) - agent.location[0]
		
		
		# get the direction of movement of the vehicle
		direction = np.subtract(road_segment[1],road_segment[0])
		length = np.linalg.norm(direction)
	
		car_location = self.coordinate_transform(tuple(np.array(road_segment[0]) - np.array([0.5,-0.5]) + (slot ) * (direction/length)  + np.flip(direction/length) * (0.25 if direction[0] == 0 else -0.25) ))
	
		if hasattr(agent, '_sprite'):
			rotated_sprite = agent._sprite if tuple(direction/length) == (1,0) else pygame.transform.rotate(agent._sprite, 180 if tuple(direction/length) == (-1,0)  else tuple(direction/length)[1]*90 )
		
		return car_location, rotated_sprite
	
	
	
	def render(self):
	
		# Reset the screen.
	        self.screen.fill(self.bg_color)
        
        
        
        	# Draw elements
        	# * Static elements

	
        
        	# TODO: convert the rect boundaries to a math term dependent on parameters from env 
        	pygame.draw.rect(self.screen, self.boundary_color, ( self.bounds[0]*self.block_size, self.bounds[1]*self.block_size, self.bounds[2]*self.block_size, self.bounds[3]*self.block_size), 4)
        
        
        	# iteration over roads to draw the roads and separation lines
        	for road in self.unique_roads:
        
        		# transforming road points
        		road_start = self.coordinate_transform(road[0])
        		road_end = self.coordinate_transform(road[1])
        	
        		# drawing the roads 
        		pygame.draw.line(self.screen, self.road_color, road_start, road_end, self.road_width)
        		
        		# drawing the separation lines
        		pygame.draw.line(self.screen, self.colors['white'], road_start, road_end, 1)
        	
        	# Highlight the traffic nodes with yellow circles
        	
        	for node in self.env.traffic_nodes:
        		center = self.coordinate_transform(node)
        		pygame.draw.circle(self.screen, self.colors['yellow'], center, self.block_size/2, 0)
        	
        	# Highlight the exit nodes with green circles
        	for node in self.env.exit_nodes:
        		center = self.coordinate_transform(node)
        		pygame.draw.circle(self.screen, self.colors['green'], center, self.block_size/2, 0)
        		
        	# Add traffic light directions on the map
        	self.set_traffic_lights(self.env.traffic_lights)
        	
		# Add Dynamic elements from here on
		
		
		for agent in self.env.smart_agent_list_current:
			car_location, rotated_sprite = self.place_vehicle(agent)
			self.screen.blit(rotated_sprite, car_location)
		
		
		
		# everything in the loop should be in the render function, which is called in a while loop at every time instance
        	for event in pygame.event.get():
        	        if event.type == pygame.QUIT:
        	                done = True
		
		
		#pygame.time.delay(500)	
		
		#step()
		
		        
        	pygame.display.flip()
	
	
		return
	
		
		
	def run(self, tolerance=0.05, n_test=0):
	
		
		
		
		self.quit = False
		
		
	        total_trials = 1
	        testing = False
	        trial = 1

	        while True:
	
			self.env.reset()
	
	            # Flip testing switch
	            	if not testing:
	                	if total_trials > 20: # Must complete minimum 20 training trials
				        
	                    		a = self.env.smart_agent_list_start[0]
	                    		
	                    
	                    		if a.is_learning:
	                        		if a.epsilon < tolerance: # assumes epsilon decays to 0
	                            			testing = True
	                            			trial = 1
	                    		else:
	                        		testing = True
	                        		trial = 1
	                        if total_trials > 60:
	                        	testing = True
	                        	trial = 1
	            	# Break if we've reached the limit of testing trials
	            	else:
	                	if trial > n_test:
	                    		break
	
	
	            	
	            	
	            	# for each agent in env, set the start, destination and current location points
	            	
	            	for agent in self.env.smart_agent_list_start:
	            		
	            		choice = np.random.choice(len(self.env.exit_nodes))
	            		agent.start_point = self.env.exit_nodes[choice]
	            		
	            		
	            		if agent.start_point == (62,65):
	            			 agent.destination = (0,-3)
	            		elif agent.start_point == (0,-3):
	            			 agent.destination = (62,65)
	            		elif agent.start_point == (-3,62):
	            			 agent.destination = (65,0)
	            		elif agent.start_point == (65,0):
	            			 agent.destination = (-3,62)
	            		
	            		
	            	
	            	
	            	self.current_time = 0.0
	            	self.last_updated = 0.0
	            	self.start_time = time.time()
	            	
	            	while self.env.time < 3600:
	                	#try:
	                    	# Update current time
	                    	self.current_time = time.time() - self.start_time
	
	                    	# Handle GUI events
	                    
	                    	
	                    
	                    	# Update environment
	                    	if self.current_time - self.last_updated >= self.update_delay:
	                        	
	                        	if len(self.env.smart_agent_list_start) > 0:
	                        		send_flag = np.random.choice([True,False],p=[1,0]) # will change the distribution later
	                        		
	                        		if send_flag:
	                        			new_agent = self.env.smart_agent_list_start.pop()
	                        			current_road = [item for item in self.env.road_segments.keys() if item[0] == new_agent.start_point]
	                        			
	                        			location_on_road = len(self.env.road_segments[current_road[0]])-1
	                        			new_agent.location = (location_on_road, current_road[0])
	                        			self.env.smart_agent_list_current.append(new_agent)
	                        		
	                        		
	                        	
	                        	self.env.step()
	                        	
	                        	self.last_updated = self.current_time
	                    		
	                    		if len(self.env.smart_agent_list_start) == 0 and len(self.env.smart_agent_list_current) == 0:
	                    			# learning agent reached some destination or had an accident
	                    			break
	                    	
	                    	# Render text
	                    	#self.render_text(trial, testing)
	
	                    	# Render GUI and sleep
	                    	if self.display:
	                        	self.render()
	                        	self.pygame.time.wait(self.frame_delay)
	
		                #except KeyboardInterrupt:
	                    	#	self.quit = True
	                	#finally:
	                    	#	if self.quit or self.env.done:
	                        #		break
	
	            	#if self.quit:
	                #	break
	
	            	
	            	print("Trial number", trial)
			
			if testing:
				print "TESTING"
	            	# Trial finished
#	        	if self.env.success == True:
#	                	print "\nTrial Completed!"
#	                	print "Agent reached the destination."
#	            	else:
#	                	print "\nTrial Aborted!"
#	                	print "Agent did not reach the destination."
	
	            	# Increment
	            	total_trials = total_trials + 1
	            	trial = trial + 1
	
	
	        print "\nSimulation ended. . . "
	
	        # Report final metrics
	        #if self.display:
	        #    self.pygame.display.quit()  # shut down pygame
			
			
		
	
	
		return
