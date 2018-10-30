# import necessary libraries and environment.py
import numpy as np
import environment


#creating agent class
class Agent():
	# This is the intelligent agent we are trying to train and test
	
	location = None #needs to be set
	
	time_taken = 0
	start_point = None
	destination_point = None
	
	test_mode = False
	
	epsilon = 1
	learning_rate = 1
	
	
	def __init__(self, epsilon, learning_rate, is_learning = False):
		self.Q_intersection = dict()
		self.Q_road_segment = dict()
		self.epsilon = epsilon
		self.learning_rate = learning_rate
		self.is_at_intersection = False
		
		
	
	def get_inputs(self)
		#gets information from the environment about the traffic
		#gets information from the i-groups about the lights
	
	
	def next_waypoint(self):
		#uses self.location and self.destination to plan the next waypoint
		
		
	def build_state():
		
	def choose_action():
	
	
	def learn():
	
	def update():
	
	
	def dist_to_destination():
		#calculates the minimum distance to destination from current location
	
	
	
	

class Dummy_agent():
	#takes actions randomly. Always follows rules rigorously
	
	def __init__(self):
		
	
	def get_inputs(self):
		# gets inputs from environment and i-group about lights and traffic respectively
		## NAZIA
		# if test_mode == False:
		#	call update_traffic_lights ??
		# else:
		#	call i-groups functions ???
		
