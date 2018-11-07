import sys, pygame
import time
import numpy as np

class Simulator():
	
	
	def __init__(self,env, update_delay=0.05, display=True):
		
		self.env = env
		self.update_delay = update_delay
		
		
		self.quit = False
        	self.start_time = None
        	self.current_time = 0.0
        	self.last_updated = 0.0
		
		
		# This is for simulation purposes, not to be touched yet
		self.display = display
		
		return
		
		
	def run(self, tolerance=0.05, n_test=0):
	
		
		
		
		self.quit = False
		
		
	        total_trials = 1
	        testing = False
	        trial = 1

	        while True:
	
			
	
	            # Flip testing switch
	            	if not testing:
	            
	            	
	                	if total_trials > 20: # Must complete minimum 20 training trials
				                    
	                    
	                    
	                    
	                    		if a.learning:
	                        		if a.epsilon < tolerance: # assumes epsilon decays to 0
	                            			testing = True
	                            			trial = 1
	                    		else:
	                        		testing = True
	                        		trial = 1
	                        
	            	# Break if we've reached the limit of testing trials
	            	else:
	                	if trial > n_test:
	                    		break
	
	
	            	self.env.reset()
	            	
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
	                        		send_flag = np.random.choice([True,False]) # will change the distribution later
	                        		
	                        		if send_flag:
	                        			new_agent = self.env.smart_agent_list_start.pop()
	                        			current_road = [item for item in self.env.road_segments.keys() if item[0] == new_agent.start_point]
	                        			
	                        			location_on_road = len(self.env.road_segments[current_road[0]])-1
	                        			new_agent.location = (location_on_road, current_road[0])
	                        			self.env.smart_agent_list_current.append(new_agent)
	                        		
	                        		
	                        	
	                        	self.env.step()
	                        	self.last_updated = self.current_time
	                    		
	                    		if len(self.env.smart_agent_list_current) == 0:
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
