# add relevant libraries here


class environment():
	nodes = [(-1,2), (0,-1), (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (2,3), (3,0)]
	
	exit_nodes = [(-1,2),(0,-1),(3,0),(2,3)]
	
	def __init__(self):
		self.road_segments = dict()
		
		#initializing the entry/exit road segments
		self.road_segments[((0,-1),(0,0))] = [None]*2
		self.road_segments[((0,0),(0,-1))] = [None]*2
		
		self.road_segments[((-1,2),(0,2))] = [None]*2
		self.road_segments[((0,2),(-1,2))] = [None]*2
		
		self.road_segments[((2,2),(2,3))] = [None]*2
		self.road_segments[((2,3),(2,2))] = [None]*2
		
		self.road_segments[((2,0),(3,0))] = [None]*2
		self.road_segments[((3,0),(2,0))] = [None]*2
		
		#initializing the rest of the road segments
		self.road_segments[((0,0),(0,1))] = [None]*30	
		self.road_segments[((0,1),(0,0))] = [None]*30
		
		self.road_segments[((0,2),(0,1))] = [None]*30	
		self.road_segments[((0,1),(0,2))] = [None]*30
		
		self.road_segments[((0,0),(1,0))] = [None]*30	
		self.road_segments[((1,0),(0,0))] = [None]*30
		
		self.road_segments[((1,1),(0,1))] = [None]*30	
		self.road_segments[((0,1),(1,1))] = [None]*30
		
		self.road_segments[((0,2),(1,2))] = [None]*30	
		self.road_segments[((1,2),(0,2))] = [None]*30
		
		self.road_segments[((1,0),(1,1))] = [None]*30	
		self.road_segments[((1,1),(1,0))] = [None]*30
		
		self.road_segments[((1,1),(1,2))] = [None]*30	
		self.road_segments[((1,2),(1,1))] = [None]*30
		
		self.road_segments[((1,0),(2,0))] = [None]*30	
		self.road_segments[((2,0),(1,0))] = [None]*30
		
		self.road_segments[((1,1),(2,1))] = [None]*30	
		self.road_segments[((2,1),(1,1))] = [None]*30
		
		self.road_segments[((2,2),(1,2))] = [None]*30	
		self.road_segments[((1,2),(2,2))] = [None]*30
		
		self.road_segments[((2,1),(2,0))] = [None]*30	
		self.road_segments[((2,0),(2,1))] = [None]*30
		
		self.road_segments[((2,1),(2,2))] = [None]*30	
		self.road_segments[((2,2),(2,1))] = [None]*30
		
		
		
	def update_traffic_lights(self):
		
	
		
	
	def send_traffic_info(self, road_segments):
		#join the continuous road segments and send to i-group
		
		
		
		
		
		
		
		
		
