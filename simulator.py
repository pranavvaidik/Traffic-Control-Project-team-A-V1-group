import sys, pygame
import time
import numpy as np

class Simulator():
	
	# car colors for identification
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
	
	
	def __init__(self,env, update_delay=0.0001, display=True):
		
		self.env = env
		self.update_delay = update_delay
		
		
		self.quit = False
        	self.start_time = None
        	self.current_time = 0.0
        	self.last_updated = 0.0
		
		
		# This is for simulation purposes, not to be touched yet
		self.display = display
		
		
		if self.display:
            	try:
            		self.pygame = importlib.import_module('pygame')
        	        self.pygame.init()
        	        self.screen = self.pygame.display.set_mode(self.size)
        	        #self._logo = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "logo.png")), (self.road_width, self.road_width))
	
        	        self._ew = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "east-west.png")), (self.road_width, self.road_width))
        	        self._ns = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "north-south.png")), (self.road_width, self.road_width))
	
        	        self.frame_delay = max(1, int(self.update_delay * 1000))  # delay between GUI frames in ms (min: 1)
        	        self.agent_sprite_size = (32, 32)
        	        self.primary_agent_sprite_size = (42, 42)
        	        self.agent_circle_radius = 20  # radius of circle, when using simple representation
        	        """for agent in self.env.agent_states:
        	            if agent.color == 'white':
        	                agent._sprite = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), self.primary_agent_sprite_size)
        	            else:
        	                agent._sprite = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), self.agent_sprite_size)
        	            agent._sprite_size = (agent._sprite.get_width(), agent._sprite.get_height())"""
	
        	        self.font = self.pygame.font.Font(None, 20)
        	        self.paused = False
       		except ImportError as e:
        	        self.display = False
        	        print "Simulator.__init__(): Unable to import pygame; display disabled.\n{}: {}".format(e.__class__.__name__, e)
   		except Exception as e:
   		        self.display = False
        		print "Simulator.__init__(): Error initializing GUI objects; display disabled.\n{}: {}".format(e.__class__.__name__, e)

		
		
		
		
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
	                    	#if self.display:
	                        #	self.render(trial, testing)
	                        #	self.pygame.time.wait(self.frame_delay)
	
		                #except KeyboardInterrupt:
	                    	#self.quit = True
	                	#finally:
	                    	#if self.quit or self.env.done:
	                        #	break
	
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
