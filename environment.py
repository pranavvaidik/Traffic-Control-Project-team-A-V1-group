# add relevant libraries here
import numpy as np
#from agent import LearningAgent, DummyAgent


class Environment():
	nodes = [(62,65), (-3,62), (0,62), (31,62), (62,62), (0,31), (31,31), (62,31), (0,0), (31,0), (62,0), (65,0), (0,-3)]
	
	exit_nodes = [(62,65),(-3,62),(0,-3),(65,0)]
	
	traffic_nodes=[(0,0), (31,0), (62,0),(0,31),(31,31),(62,31),(0,62),(31,62),(62,62)]
	
	random_lights = True
	
	traffic_lights = dict()
	
	turn_map = dict()
	
	#initializing the list of agents in the environment
	smart_agent_list_current = []
	
	dummy_agent_list_current = []
	
	dummy_agent_list_start = []
	
	smart_agent_list_reached = []
	
	smart_agent_list_start = []
	
	agent_list_current = smart_agent_list_current + dummy_agent_list_current
	
	agent_list_start = smart_agent_list_start + dummy_agent_list_start
	
	
	
	# counting number of violations and throughput
	collision_count = 0
	signal_violation_count = 0
	reached_count = 0
	wrong_destination_reached_count = 0
	throughput = 0
	
	#building a turn map
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
	
	
	
	
	congestion_map = dict()
	
	
	def __init__(self):
		
		# set time to zero
		self.time = 0
		
		
		# set initializations for UI
		self.block_size = 20
		self.n_blocks = (69,69)
		
		
		
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
			
			if len(actions) == 0:
				actions.append('forward')
		
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
		
		
		self.collision_count = 0
		self.signal_violation_count = 0
		self.reached_count = 0
		self.wrong_destination_reached_count = 0
		self.throughput = 0
		
		
		# clear all starting, current and end locations of agents
		for agent in self.smart_agent_list_current:
			print "NOT REACHED"
			agent.location = None
			agent.destination = None
			agent.start_point = None
			agent.state = None
			self.smart_agent_list_start.append(agent)
		
		for agent in self.dummy_agent_list_current:
			#print "NOT REACHED"
			agent.location = None
			#agent.destination = None
			agent.start_point = None
			#agent.state = None
			self.dummy_agent_list_start.append(agent)
		
		
		
		
		self.smart_agent_list_current = []
		self.dummy_agent_list_current = []
		self.agent_list_current = []
		
		for agent in self.smart_agent_list_reached:
			
			if agent.location == agent.destination:
				print agent.location
				print agent.destination
				print "SUCCESS"
			else:
				print agent.location
				print agent.destination
				
				print "FAILED"
			
			agent.location = None
			agent.destination = None
			agent.start_point = None
			agent.state = None
			self.smart_agent_list_start.append(agent)
		
		for agent in self.dummy_agent_list_start:
			agent.location = None
			agent.start_point = None
			#self.smart_agent_list_start.append(agent)
		
			
		self.smart_agent_list_reached = []
		
		
		self.agent_list_start = self.smart_agent_list_start + self.dummy_agent_list_start
		
		print "there are ", len(self.smart_agent_list_current), "smart agents"
		print "there are ", len(self.dummy_agent_list_current), "dummy agents"
		print "there are ", len(self.agent_list_current), "total agents"
		
		
	
	def update_traffic_lights(self):
		for loc in self.nodes:
			dirs = [None]
			if loc not in self.exit_nodes:                
                		#choose the signal randomly from legal directions
				self.traffic_lights[loc] = np.random.choice(self.directions_to_loc[loc])
       
   		return
	
	
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
		
		
		# for each agent in env, set the start, destination and current location points
	        	
		entry_roads = [item for item in self.road_segments.keys() if item[0] in self.exit_nodes]
			
		for current_road in entry_roads:
			
			if len(self.agent_list_start) > 0:
				# check if the entry slot is empty
				if not self.road_segments[current_road][-1]:
					send_flag = np.random.choice([True,False],p=[1,0]) # will change the distribution later
	               		else:
	               			send_flag = False
	                else:
	                	send_flag = False
	                
	                       		
	        	if send_flag:
	               		new_agent = self.agent_list_start.pop()
	                     	
	               		# check which of the entry slots are vacant, and then place the vehicle
	        		new_agent.start_point = current_road[0]
	                     	
	                     	if new_agent.is_smart:
	                     	
	                     		if new_agent.start_point == (62,65):
	            				 new_agent.destination = (0,-3)
	            			elif new_agent.start_point == (0,-3):
	            				 new_agent.destination = (62,65)
	            			elif new_agent.start_point == (-3,62):
	            				 new_agent.destination = (65,0)
	            			elif new_agent.start_point == (65,0):
	            				 new_agent.destination = (-3,62)
	                     	
	                        	self.smart_agent_list_current.append(new_agent)
	                        	self.smart_agent_list_start.remove(new_agent)
	                        else:
	                        	self.dummy_agent_list_current.append(new_agent)
	                        	self.dummy_agent_list_start.remove(new_agent)
	                        	#print "this happened"
	                        	#print new_agent.location	
	                        
	                     	
	                     	
	                        #current_road = [item for item in self.road_segments.keys() if item[0] == new_agent.start_point]

				# check if the slot is empty
				

				# place new agent on the new location
	                        location_on_road = len(self.road_segments[current_road])-1
	                        new_agent.location = (location_on_road, current_road)
	                        	
		
		# update traffic lights
		self.update_traffic_lights()
		
		
		# update all vehicles
		temp = []
		
		for agent in self.agent_list_current:
			agent.update()
		
			if agent.location in self.exit_nodes:
				#if not agent.is_smart:
				#	print "Dummy reached the destination"
				#else:
				#	print "smart agent reached destination"
					
				temp.append(agent)
				if agent.is_smart:
					self.smart_agent_list_reached.append(agent)
					self.smart_agent_list_current.remove(agent)
				else:
					self.dummy_agent_list_start.append(agent)
					self.dummy_agent_list_current.remove(agent)
				#	print "agent loc is: ", agent.location
			#if agent.location == None:
			
				
		
		self.agent_list_current = self.smart_agent_list_current + self.dummy_agent_list_current
		self.agent_list_start = self.smart_agent_list_start + self.dummy_agent_list_start			
		
		# also remove cars that crashed
		
		
		
		
		
		self.time = self.time + 2
		
		
		return
	
	
	def send_traffic_info(self):
		#join the continuous road segments and send to i-group
		
		return
		

		
		
		
