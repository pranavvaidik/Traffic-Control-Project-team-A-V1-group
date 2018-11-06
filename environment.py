# add relevant libraries here
import numpy as np
#from agent import LearningAgent, DummyAgent


class Environment():
	nodes = [(62,65), (-3,62), (0,62), (31,62), (62,62), (0,31), (31,31), (62,31), (0,0), (31,0), (2,2), (65,0), (0,-3)]
	
	exit_nodes = [(62,65),(-3,62),(0,-3),(65,0)]
	
	random_lights = True
	
	turn_map = dict()
	
	for key in ['NORTH','SOUTH','EAST','WEST']:
		turn_map[key] = dict()
		turn_map[key][key] = 'forward'
	
	turn_map['NORTH']['EAST'] = 'right'
	turn_map['NORTH']['WEST'] = 'left'
	
	turn_map['SOUTH']['WEST'] = 'right'
	turn_map['SOUTH']['EAST'] = 'left'
	
	turn_map['EAST']['NORTH'] = 'left'
	turn_map['EAST']['SOUTH'] = 'right'
	
	turn_map['WEST']['NORTH'] = 'right'
	turn_map['WEST']['SOUTH'] = 'left'
	
	
	
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
		
	
	def valid_actions(self, location):
		
		# takes in the location of a vehicle and gives all valid actions as a dictionary, including the next segments if the car is at the intersection.
		
		# if not at intersection
		if location[0] !=0:
			actions = ['forward', None]
			
		else:
			next_segments = self.next_segment(location[1])
			actions = next_segments.keys()
		
		return actions
	
	
	def next_segment(self, current_road_segment):
		# returns the set of possible road segments for each action as a dictionary {action : next segment} format
		current_heading = self.headings([current_road_segment])
		
		#find the roads that start with the same intersection, except for the one that is going in the reverse direction (no U-turns)
		next_road_segments = [item for item in self.road_segments.keys() if item[0] == current_road_segment[1] and item[1] != current_road_segment[0]]
		next_road_headings = self.headings(next_road_segments)
		
		
		next_actions = dict()
		
		for i,segment in enumerate(next_road_segments):
			next_actions[self.turn_map[current_heading][next_road_headings[i]]] = segment
		
		return next_actions
		
	def headings(self, road_segments_list):
		
		#calculates and returns the direction of the vehicles in a road segment
		
		directions = [tuple(np.linalg.subtract(segment[1],segment[0])) for segment in road_segment_list]
		headings = [None]*len(road_segment_list)
		
		for i, direction in enumerate(directions):
			
			if direction[0] == 0:
				if direction[1] >= 0:
					heading[i] = 'NORTH'
				else:
					heading[i] = 'SOUTH'	
			
			elif direction[1] == 0:
				if direction[0] >= 0:
					heading[i] = 'EAST'
				else:
					heading[i] = 'WEST'

		return headings
		
		
	
	
				
	def create_agent(self, is_learning = True, epsilon = 1, learning_rate = 1):
		
		#creates agents.
		
		if is_learning:
			agent = LearningAgent(epsilon, learning_rate)
		else:
			agent = DummyAgent()
		
        	#self.agent_states[agent] = {'location': random.choice(self.intersections.keys()), 'heading': (0, 1)}
        	return agent

	
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
	
	
	def update_traffic(self):
	
		return
	
	def send_traffic_info(self):
		#join the continuous road segments and send to i-group
		
		return
		

		
		
		
