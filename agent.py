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
			inputs = {'light':'green'}
		else:
			inputs = {'light':'red'}
		
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
			
			#get lights
			inputs = get_inputs()
			
			
			waypoint = self.next_waypoint()
			
			
			#collect waypoint information
			
			#see if any vehicle is curently there
			
			#see if the vehicle has green light
			
			# return dictionary
			
		else:
			#check if next slot is empty; state will be of the form: {next_slot_empty: True/False}
			if self.env.road_segments[location[1]][location[0] - 1] == None:
				state = {'next_slot_empty':True}
			else:
				state = {'next_slot_empty':False}
			
			#return dictonary or flag value
			
		return
		
	def choose_action(self):
		
		if self.is_at_intersection:
			# left, right, straight, or None
			x=1
		else:
			# move forward or None
			x=1
		return
	
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
        	reward = self.act(self, action) # Receive a reward
        	self.learn(state, action, reward)   # Q-learn
		
		
		#move, get reward, update Q-function
		
		
		return
		
	def act(self):
		# move/ don't move, get reward, update Q-function
		
		
		return
		
	def dist_to_destination(self):
		#calculates the l1 distance to destination from current location
		if self.location != None and self.destination_point != None :
			location_on_road = self.location[0]
			next_intersection = self.location[0][1]
			
			# get total distance
			dist = location_on_road + 1 + np.linalg.norm(np.linalg.subtract(self.destination_point, next_intersection),1)
		return dist
	
	

class DummyAgent():
	#takes actions randomly. Always follows rules rigorously
	
	location = None   # Needs to be assigned a correct value.
	start_point = np.random.choice(Environment.exit_nodes)
	
	def __init__(self, env):
		self.Q_intersection = dict()
		self.Q_road_segment = dict()
		self.is_at_intersection = False
		self.ID = None
		self.env = env
		
		return
			
	
	def get_inputs(self):
		# gets inputs from environment and i-group about lights and traffic respectively
		
		
		
		
		
		return
		
	def choose_action(self):
		
		if self.is_at_intersection:
			# left, right, straight, or None
			x=1
		else:
			# move forward or None
			x=1
		return
		
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
