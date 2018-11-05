# import necessary libraries and environment.py
import numpy as np
import environment


#creating agent class
class LearningAgent(env):
	# This is the intelligent agent we are trying to train and test
	
	location = None #needs to be set #will be a tuple; first entry will be its location on the segment, second entry will be a tuple that describes the segment
	
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
		self.ID = None
		
		
	
	def get_inputs(self):
		#gets information from the environment about the traffic
		#gets information from the i-groups about the lights
	
	
	def next_waypoint(self):
		#uses self.location and self.destination to plan the next waypoint
		
		
	def build_state():
		
		if self.is_at_intersection:
			#collect waypoint information
			
			#see if any vehicle is curently there
			
			#see if the vehicle has green light
			
			# return dictionary
			
		else:
			#check if next slot is empty
			
			#return dictonary or flag value
	
		
	def choose_action():
		
		if self.is_at_intersection:
			# left, right, straight, or None
			
		else:
			# move forward or None
			
		
	
	def learn():
	
	def update():
	
	
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
		
	
	def get_inputs(self):
		# gets inputs from environment and i-group about lights and traffic respectively
		## NAZIA
		# if test_mode == False:
		#	call update_traffic_lights ??
		# else:
		#	call i-groups functions ???
		
