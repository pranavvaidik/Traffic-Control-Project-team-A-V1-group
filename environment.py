# add relevant libraries here
import numpy as np
#from agent import LearningAgent, DummyAgent


class Environment():
	nodes = [(62,65), (-3,62), (0,62), (31,62), (62,62), (0,31), (31,31), (62,31), (0,0), (31,0), (62,0), (65,0), (0,-3)]
	
	exit_nodes = [(62,65),(-3,62),(0,-3),(65,0)]
	
	random_lights = True
	
	traffic_lights = dict()
	
	turn_map = dict()
	
	smart_agent_list_current = []
	
	smart_agent_list_reached = []
	
	
	
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
	
	
	
	# directions of vehicles arriving at an intersection
	directions_to_loc = dict()
	
	
	
	
	
	
	congestion_map = dict()
	
	
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
		
		
		for loc in self.nodes:
			if loc not in self.exit_nodes:			
        			# get all the legal directions at the intersection
				roads_ending_at_loc = [item for item in self.road_segments.keys() if item[1] == loc]
				self.directions_to_loc[loc] = self.headings(roads_ending_at_loc)
				self.directions_to_loc[loc].append(None)
	
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
		current_heading = self.headings([current_road_segment])[0]
		
		#find the roads that start with the same intersection, except for the one that is going in the reverse direction (no U-turns)
		next_road_segments = [item for item in self.road_segments.keys() if item[0] == current_road_segment[1] and item[1] != current_road_segment[0]]
		next_road_headings = self.headings(next_road_segments)
		
		
		next_actions = dict()
		
		for i,segment in enumerate(next_road_segments):
			next_actions[self.turn_map[current_heading][next_road_headings[i]]] = segment
		
		return next_actions
		
	def headings(self, road_segments_list):
		
		#calculates and returns the direction of the vehicles in a road segment
		
		directions = [tuple(np.subtract(segment[1],segment[0])) for segment in road_segments_list]
		headings = [None]*len(road_segments_list)
		
		for i, direction in enumerate(directions):
			
			if direction[0] == 0:
				if direction[1] >= 0:
					headings[i] = 'NORTH'
				else:
					headings[i] = 'SOUTH'	
			
			elif direction[1] == 0:
				if direction[0] >= 0:
					headings[i] = 'EAST'
				else:
					headings[i] = 'WEST'

		return headings
		
	
	
	def reset(self):
		# clear all roads
		self.__init__()
		
		# clear all starting, current and end locations of agents
		for agent in self.smart_agent_list_current:
			agent.location = None
			agent.destination = None
			agent.start_point = None
		
		for agent in self.smart_agent_list_reached:
			agent.location = None
			agent.destination = None
			agent.start_point = None
		
	
	def update_traffic_lights(self):
		for loc in self.nodes:
			dirs = [None]
			if loc not in self.exit_nodes:                
                		#choose the signal randomly from legal directions
				self.traffic_lights[loc] = np.random.choice(self.directions_to_loc[loc])
       
   		return self.traffic_lights	
	
	
	def congestion_at_intersection(self, intersection):
		roads_to_intersection = [item for item in self.road_segments.keys() if item[1] == intersection[1]]
		
		congestion = 0
		for road in roads_to_intersection:
			#locate the first empty slot on the road segment to find the number of cars waiting at the intersection for that road segment
			congestion = congestion + self.road_segments[road].index(None)
		return congestion
		
	def congestion_calc(self):
		
		intersections = [item for item in self.nodes if item not in self.exit_nodes]
		for intersection in intersections:
			congestion_map[intersection] = self.congestion_at_intersection(intersection)
		
		return
	
	
	def step(self):
		
		
		
		
		# update traffic lights
		self.update_traffic_lights()
		
		
		# update all vehicles
		temp = []
		for agent in self.smart_agent_list_current:
			agent.update()
			
			# remove cars that reached exit nodes
			if agent.location[1][1] in self.exit_nodes:
				temp.append(agent)
				agent_list_reached.append(agent)
				
			# also remove cars that crashed
		
		
		for agent in temp:
			smart_agent_list_current.remove(agent)
			
		# during training, we are supposed to check for collisions
		
		
		
		self.time = self.time + 2
		
		
		return
	
	
	def send_traffic_info(self):
		#join the continuous road segments and send to i-group
		
		return
		

		
		
		
