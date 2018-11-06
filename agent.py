# import necessary libraries and environment.py
import numpy as np
from environment import Environment

#creating agent class
class LearningAgent():
	# This is the intelligent agent we are trying to train and test
	
	location = None #needs to be set #will be a tuple; first entry will be its location on the segment, second entry will be a tuple that describes the segment
	
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
		

		
		
		return
		
	def next_waypoint(self):
		#uses self.location and self.destination to plan the next waypoint
		return
		
	def build_state(self):
		
		if self.is_at_intersection:
			#collect waypoint information
			
			#see if any vehicle is curently there
			
			#see if the vehicle has green light
			
			# return dictionary
			
		else:
			#check if next slot is empty; state will be of the form: {next_slot_empty: True/False}
			
			
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
	
	def learn():
	
		return
	
	def createQ(self):
		
		# if state is in the Q-function, add state in dictionary
		
		if self.is_at_intersection:
			if state not in self.Q_intersection.keys():
				valid_actions = self.env.valid_actions(self.location)
				
				self.Q_intersection[state] = dict()
				self.Q_intersection[state][None] = 0.0
				self.Q_intersection[state]['forward'] = 0.0
				self.Q_intersection[state]['left'] = 0.0
				self.Q_intersection[state]['right'] = 0.0
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
	
	def __init__(self):
	
		return
		
	
	def get_inputs(self):
		# gets inputs from environment and i-group about lights and traffic respectively
		## NAZIA
		# if test_mode == False:
		#	call update_traffic_lights ??
		# else:
		#	call i-groups functions ???
		
		return
		
		
def run():
	
	#initializes the environment and the agents and runs the simulator
	
	env = Environment()
	
	# For training scneario
	
	agent = env.create_agent(is_learning=True)
	
	
	
	
	
	

if __name__ == '__main__':
	run()
