import sys, pygame
import time


class Simulator():
	
	
	def __init__(self,env, update_delay=2.0, display=True):
		
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
	
	            

	            	# Trial finished
	        	if self.env.success == True:
	                	print "\nTrial Completed!"
	                	print "Agent reached the destination."
	            	else:
	                	print "\nTrial Aborted!"
	                	print "Agent did not reach the destination."
	
	            	# Increment
	            	total_trials = total_trials + 1
	            	trial = trial + 1
	
	
	        print "\nSimulation ended. . . "
	
	        # Report final metrics
	        #if self.display:
	        #    self.pygame.display.quit()  # shut down pygame
			
			
		
	
	
		return
