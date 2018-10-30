# add relevant libraries here
import numpy as np

class environment():
	nodes = [(62,65), (-3,62), (0,62), (31,62), (62,62), (0,31), (31,31), (62,31), (0,0), (31,0), (2,2), (65,0), (0,-3)]
	
	exit_nodes = [(62,65),(-3,62),(0,-3),(65,0)]
	
	random_lights = True
	
	
	
	def __init__(self):
		
		# set time to zero
		self.time = 0
		
		self.road_segments = dict()
		
		#initializing the entry/exit road segments
		self.road_segments[((-3,62),(0,62))] = [None]*2
		self.road_segments[((0,62),(-3,62))] = [None]*2
		
		self.road_segments[((62,65),(62,62))] = [None]*2
		self.road_segments[((62,62),(62,65))] = [None]*2
		
		self.road_segments[((62,0),(65,0))] = [None]*2
		self.road_segments[((65,0),(62,0))] = [None]*2
		
		self.road_segments[((0,0),(0,-3))] = [None]*2
		self.road_segments[((0,-3),(0,0))] = [None]*2
		
		#initializing the rest of the road segments
		self.road_segments[((0,62),(31,62))] = [None]*30	
		self.road_segments[((31,62),(0,62))] = [None]*30
		
		self.road_segments[((62,62),(31,62))] = [None]*30	
		self.road_segments[((31,62),(62,62))] = [None]*30
		
		self.road_segments[((0,62),(0,31))] = [None]*30	
		self.road_segments[((0,31),(0,62))] = [None]*30
		
		self.road_segments[((31,31),(31,62))] = [None]*30	
		self.road_segments[((31,62),(31,31))] = [None]*30
		
		self.road_segments[((62,62),(62,31))] = [None]*30	
		self.road_segments[((62,31),(62,62))] = [None]*30
		
		self.road_segments[((0,31),(31,31))] = [None]*30	
		self.road_segments[((31,31),(0,31))] = [None]*30
		
		self.road_segments[((31,31),(62,31))] = [None]*30	
		self.road_segments[((62,31),(31,31))] = [None]*30
		
		self.road_segments[((0,31),(0,0))] = [None]*30	
		self.road_segments[((0,0),(0,31))] = [None]*30
		
		self.road_segments[((31,31),(31,0))] = [None]*30	
		self.road_segments[((31,0),(31,31))] = [None]*30
		
		self.road_segments[((62,0),(62,31))] = [None]*30	
		self.road_segments[((62,31),(62,0))] = [None]*30
		
		self.road_segments[((31,0),(0,0))] = [None]*30	
		self.road_segments[((0,0),(31,0))] = [None]*30
		
		self.road_segments[((31,0),(62,0))] = [None]*30	
		self.road_segments[((62,0),(31,0))] = [None]*30
		
		
		
	def update_traffic_lights(self):
		# TODO: Update traffic lights randomly
		
		# if random lights is true
		
		
		#add comments
		
		#else, call their function
   		traffic_lights = []
   		if random_lights == True:
        		for loc in nodes:
       				dirs = [None]
            			if loc not in exit_nodes:
                			x = loc[0]
               				y = loc[1]
                			if x < 62 and x > 0:
                    				dirs.extend(['EAST','WEST'])
                			elif x == 0:
			               		dirs.append('EAST')
            				else:
                    				dirs.append('WEST')
                    
                			if y < 62 and y > 0:
                    				dirs.extend(['NORTH','SOUTH'])
                			elif y == 0:
                    				dirs.append('NORTH')
                			else:
                    				dirs.append('SOUTH')
                
                green = np.random.choice(dirs)
                traffic_lights.append('GLDT ' + green + ' for ' + str(loc))
       
   	return traffic_lights	
	
		
	
	def send_traffic_info(self, road_segments):
		#join the continuous road segments and send to i-group
		
		
		
		
		
		
		
		
		
