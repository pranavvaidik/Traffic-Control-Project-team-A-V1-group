# import necessary libraries and environment.py
import numpy as np
from environment import Environment

#creating agent class
class LearningAgent():
	# This is the intelligent agent we are trying to train and test
	
	location = None  #will be a tuple; first entry will be its location on the segment, second entry will be a tuple that describes the segment
	
	time_taken = 0
	start_point = None
	destination_point = None
	
	test_mode = False
	
	state = None
	
	epsilon = 1
	learning_rate = 1
	
	
	
	
	def __init__(self, env, epsilon, learning_rate, is_learning = False):
		self.Q_intersection = dict()
		self.Q_road_segment = dict()
		self.epsilon = epsilon
		self.learning_rate = learning_rate
		self.is_at_intersection = False
		self.ID = None
		self.env = env
		
	
	def get_inputs(self):
		#gets information from the environment about the traffic
		#gets information from the i-groups about the lights
		
		lights = env.traffic_lights[self.location[1]]
		
		heading = env.headings([location[1]])[0]
		
		if lights == heading:
			inputs = {'light':'green', 'forward' : None, 'left' : None, 'right' : None}
		else:
			inputs = {'light':'red', 'forward' : None, 'left' : None, 'right' : None}
		
		next_actions = env.next_segment(location[1])
		
		for action in next_actions.keys():
			#will tell if slot is empty for each valid turn. True means slot is empty, false is when there is a vehicle present.
			inputs[action] = (next_actions[action][-1] == None)
		
		return inputs
		
	def next_waypoint(self):
		#only called when agent is at intersection
		
		current_road = self.location[1]
		current_intersection = current_road[1]
		
		diff = np.subtract(self.destination, current_intersection)
		
		# get the directions to destination from the next intersection
		directions_to_destination = []
		
		if diff[0] > 0:
			directions_to_destination.append('NORTH')
		elif diff[0] < 0:
			directions_to_destination.append('SOUTH')
		
		if diff[1] > 0:
			directions_to_destination.append('EAST')
		elif diff[1] < 0:
			directions_to_destination.append('WEST')
		
		#possible actions at next intersection
		valid_actions = env.next_segment(current_road)
		
		# get roads and actions that match the directions to the destination point
		
		next_road_headings = env.headings(valid_actions.values())
		
		best_action_dirs = list(set(directions_to_destination) & set(next_road_headings))
		
		if len(best_action_dirs) == 0:
			# all next roads are moving away from the destination. all actions would be equally bad
			best_actions = valid_actions.keys()
		else:
			# select list of actions that would point towards destination
			best_actions = []
			for i, action in enumerate(valid_actions.keys()):
				if next_road_headings[i] in best_action_dirs:
					best_actions.append(action)
		
		# choose best route randomly.
		return np.random.choice(best_actions)
	
	
	
	def build_state(self):
		
		if self.is_at_intersection:
			
			
			# The state should contain the following information : light, waypoint, forward_slot_empty, left_slot_empty, right_slot_empty, direction_with_least_congestion
			
			#get lights and traffic
			inputs = self.get_inputs()
			
			#get waypoint
			waypoint = self.next_waypoint()
			
			# may consider taking in the congestion, but ignore for now
			
			self.state = (waypoint, inputs['light'], inputs['forward'], inputs['left'], inputs['right'] )
			
		else:
			#check if next slot is empty; state will be of the form: {next_slot_empty: True/False}
			if self.env.road_segments[location[1]][location[0] - 1] == None:
				state = (True)  #{'next_slot_empty':True}
			else:
				state = (False) #{'next_slot_empty':False}
			
			#return dictonary or flag value
			
		return
		
	def choose_action(self, state):
		
		if self.is_at_intersection:
			# left, right, straight, or None
			valid_actions_list = self.env.valid_actions(self.location)
			valid_actions_list.append(None)
			
			if not is_learning:
				action = np.random.choice(valid_actions_list)
			else:
				is_random = np.random.choice([True,False], p = [self.epsilon, 1-self.epsilon])
				# using epsilon greedy method
				if is_random:
					action = np.random.choice(valid_actions_list)
				else:
					best_actions = [actions for actions, q_value in self.Q_intersection[state].items() if q_value == self.get_maxQ(state)]
					action = random.choice(best_actions)
			
		else:
			# move forward or None
			valid_actions_list = ['forward',None]
			
			if not is_learning:
				action = np.random.choice(valid_actions_list)
			else:
				is_random = np.random.choice([True,False], p = [self.epsilon, 1-self.epsilon])
				# using epsilon greedy method
				if is_random:
					action = np.random.choice(valid_actions_list)
				else:
					best_actions = [actions for actions, q_value in self.Q_road_segment[state].items() if q_value == self.get_maxQ(state)]
					action = random.choice(best_actions)
			
			
			
		return action
	
	def get_maxQ(self, state):
		
		if self.is_at_intersection:
			maxQ = max(self.Q_intersection[state].values())
		else:
			maxQ = max(self.Q_road_segment[state].values())
		return maxQ
	
	
	def learn(self):
	
		return
	
	def createQ(self):
		
		# if state is in the Q-function, add state in dictionary
		
		if self.is_at_intersection:
			if state not in self.Q_intersection.keys():
				valid_actions = self.env.valid_actions(self.location)
				
				self.Q_intersection[state] = dict()
				
				for action in valid_actions:
					self.Q_intersection[state][action] = 0.0
					
		else:
			if state not in self.Q_road_segment.keys():	
				self.Q_road_segment[state] = dict()
				self.Q_road_segment[state][None] = 0.0
				self.Q_road_segment[state]['forward'] = 0.0
		
		return
	
	def update(self):
		#called at the end of each time instance. when called, it builds the state, add the state to the Q-function, choose action, act and get reward, and learn and update its Q-function
		state = self.build_state()          # Get current state
        	self.createQ(state)                 # Create 'state' in Q-table
        	action = self.choose_action(state)  # Choose an action
        	reward = self.act(action) # Receive a reward
        	self.learn(state, action, reward)   # Q-learn
		
		#move, get reward, update Q-function
		
		return
		
	def act(self, action):
		# move/ don't move, get reward, update Q-function
		
		# find a way to add the violations to violations counter
		
		####################
		# reward key:
		# Moving closer to the destination -> +1 
		# Moving away from destination -> -1
		# Reaching destination -> +40
		# Red Light Violation -> -50
		# Collision -> -50
		# Reaching Wrong Destination -> -5
		# Waiting when green light -> -5
		# Waiting when next slot is empty -> -5
		# Do nothing -> 0
		################
		
		if not is_at_intersection:
			
			if action == None:
				if self.state == (True):
					# not moving when empty slot ahead
					reward = -5
				else:
					# next slot not empty
					reward = 0
			else:
				#action is to move forward
				if self.state == (True)
					# next slot empty and moving
					next_location = (self.location[0]-1, self.location[1])
					distance_moved = self.dist_to_destination(self.location) - self.dist_to_destination(next_location)
					
					if distance_moved > 0:
						reward = +1 # moving closer to destination
					else:
						reward = -1 # moving away from destination
				else:	
					#collision with next vehicle
					reward = -50
		else:
			# add what happens when close to destination (right and wrong)
			
			if self.location[1][1] in self.env.exit_nodes and self.location[0] == 0:
				if self.location[1][1] == self.destination:
					if action == 'forward':
					
						next_location = 'REACHED!'
						reward = 40
					else:
						reward = -5
				else:
					# wrong destination
					if action == 'forward':
						next_location = 'WRONG DESTINATION'
						reward = -5
					else:
						reward = -5
			
			
			if self.state[1] == 'red':
				if action == None:
					reward = 0
				else:
					# red light violation, also better to remove this car from the system to make it simpler
					reward = -50
			else:
				next_actions = self.env.next_segment(self.location[1])
				
				
				
				
				if action == None:
					# waiting when green light
					reward = -5
				elif action == 'forward':
					#collision with vehicle in front
					if self.state[2] == False:
						reward = -50
						
						#location of car should either not change or we have to remove the car from the traffic system
						
					else:
						next_road = next_actions[action]
						
						next_location = (len(self.env.road_segments[next_road])-1,next_road) 
						distance_moved = self.dist_to_destination(self.location) - self.dist_to_destination(next_location)
						
						if next_road[1] in self.env.exit_nodes:
							if next_road[1] != self.destination:
								reward = -30 # penalty for entering the segment leading to wrong destination
						
						else:					
							if distance_moved > 0:
								reward = 1 # moving closer to destination
							else:
								reward = -1 # moving away from destination
							
						
							
				
				elif action == 'left':
					#collision with vehicle at left
					if self.state[3] == False:
						reward = -50
						
						#location of car should either not change or we have to remove the car from the traffic system
						
					else:
						next_road = next_actions[action]
						next_location = (len(self.env.road_segments[next_road])-1,next_road) 
						distance_moved = self.dist_to_destination(self.location) - self.dist_to_destination(next_location)
						if distance_moved > 0:
							reward = +1 # moving closer to destination
						else:
							reward = -1 # moving away from destination
				
				elif action == 'right':
					#collision with vehicle at right
					if self.state[4] == False:
						reward = -50
						
						#location of car should either not change or we have to remove the car from the traffic system
						
					else:
						next_road = next_actions[action]
						next_location = (len(self.env.road_segments[next_road])-1,next_road) 
						distance_moved = self.dist_to_destination(self.location) - self.dist_to_destination(next_location)
						if distance_moved > 0:
							reward = +1 # moving closer to destination
						else:
							reward = -1 # moving away from destination
			
			
			
		
		
		
		
		return
		
	def dist_to_destination(self, location):
		#calculates the l1 distance to destination from current location
		if location != None and destination_point != None :
			location_on_road = location[0]
			next_intersection = location[0][1]
			
			# get total distance
			dist = location_on_road + 1 + np.linalg.norm(np.linalg.subtract(self.destination_point, next_intersection),1)
		return dist
	
	

class DummyAgent():
	#takes actions randomly. Always follows rules rigorously
	
	location = None   # Needs to be assigned a correct value.
	start_point = None # np.random.choice(Environment.exit_nodes)
	
	def __init__(self, env):
		self.Q_intersection = dict()
		self.Q_road_segment = dict()
		self.is_at_intersection = False
		self.ID = None
		self.env = env
		
		return
	
	
	def get_inputs(self):
		#gets information from the environment about the traffic
		#gets information from the i-groups about the lights
		
		lights = env.traffic_lights[self.location[1]]
		
		heading = env.headings([location[1]])[0]
		
		if lights == heading:
			inputs = {'light':'green'}
		else:
			inputs = {'light':'red'}
		
		next_actions = env.next_segment(location[1])
		
		for action in next_actions.keys():
			#will tell if slot is empty for each valid turn. True means slot is empty, false is when there is a vehicle present.
			inputs[action] = (next_actions[action][-1] == None)
		
		return inputs
		
	
	def choose_action(self):
		
		if self.is_at_intersection:
			# left, right, straight, or None
			inputs = self.get_inputs()
			if inputs['light'] == 'red' :
				only_action = None
			else :
				acts = []
				for acs in ['forward', 'right', 'left'] :
					if inputs[acs] == True
						acts.append(acs)
						
				only_action = np.random.choice(acts)		
		else:
			# move forward or None
			current_road = env.road_segments[location[1]]
			if current_road[location[0] + 1] == None :
				only_action = 'forward'
			else :
				only_action = None
		
		return only_action
		
	
	def act(self):
		# move/ don't move, get reward, update Q-function
		
		return
		
	
		
		
def run():
	
	#initializes the environment and the agents and runs the simulator
	
	env = Environment()
	
	# For training scneario
	
	agent = env.create_agent(is_learning=True)
	
	
	
	
	
	

if __name__ == '__main__':
	run()
