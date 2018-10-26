# import necessary libraries and environment.py



#creating agent class
class Agent():
	# This is the intelligent agent we are trying to train and test
	
	location = None #needs to be set
	
	time_taken = 0
	start_point = None
	destination_point = None
	
	#x.c = Q_intersection = dict()
	#Q_road_segment = dict()
	
	epsilon = 1
	
	def __init__(self):
		self.Q_intersection = dict()
		self.Q_road_segment = dict()
		self.epsilon = 1
		self.learning_rate = 1
		self.is_at_intersection = False
		
		
	
	def get_inputs(self)
		#gets information from the environment about the traffic
		#gets information from the i-groups about the lights
	
	
	def next_waypoint(self):
		#uses self.location and self.destination to plan the next waypoint
		
	def move_to_next_location():
		
		

class Dummy_agent():
	#takes actions randomly. Always follows rules rigorously
	
	def __init__(self):
	
	
	def get_inputs(self):
		# gets inputs from environment and i-group about lights and traffic respectively
		
