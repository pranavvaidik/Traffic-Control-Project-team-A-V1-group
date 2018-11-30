#!/usr/bin/python
# -*- coding: utf-8 -*-

##The traffic light class
import itertools
import numpy as np
import random
import math


class Traffic_Lights:

    #Q-value state-action pairs dictionary
    Q           = {}             #Dictionary to store the Q_s_a values
    state_list  = []            #State_list
    action_list = []            #Action_list
    gamma       = 0.05          #Discount factor
    alpha       = 0.20         #Learning Rate
    epsilon     = 0.1                # Epsilon for exploration/exploitation

    vehicle_queue = {}

    def __init__(self,location, adjacent_roads, signal_direction):
	self.Q = {}
	self.state_list = []
	self.action_list = []
	self.vehicle_queue = {}
	self.signal = []
        self.location             = location                    #This attribute gives the location of the traffic light
        self.adjacent_roads       = adjacent_roads              #Is a list of the lanes the signal is catering to 
        self.signal_direction     = signal_direction            #This attribute gives the existence of the signal (4 directions)
        
        for i in range(0,len(signal_direction)):    #Checking if signal is present in that direction
            if(signal_direction[i] == 1):             #If yes initializing it to Red
                if(i == 0): self.signal.insert(0,'R')
                if(i == 1): self.signal.insert(1,'R')
                if(i == 2): self.signal.insert(2,'R')
                if(i == 3): self.signal.insert(3,'R')
    
        
        #Function to create the new list 
        def lt_append(list_inp, index, new_list):
            for x in list_inp:
                y = list(x)
                y.insert(index, None)
                x = tuple(y)
                new_list.append(x)
            return new_list
        
        #Creating the S_A_pairs
        if (0 in signal_direction):
            state_list_temp  = list(itertools.product(['L','M','H'], repeat=3))   #states
            action_list_temp = [('R','R','R'),('G','R','R'),('R','G','R'),('R','R','G')] #Actions
            index            = signal_direction.index(0)
            self.state_list       = lt_append(state_list_temp,index,self.state_list)
            self.action_list      = lt_append(action_list_temp,index,self.action_list)
            s_a_list         = list(itertools.product(self.state_list,self.action_list)) #Q_s_a
        else:
            self.state_list       = list(itertools.product(['L','M','H'], repeat=4))   #states
            self.action_list      = [('R','R','R','R'),('G','R','R','R'),('R','G','R','R'),('R','R','G','R'),('R','R','R','G')] #Actions
            s_a_list         = list(itertools.product(self.state_list,self.action_list)) #Q_s_a
       

        #Creating the dictionary
        for i in range(0,len(s_a_list)):
            self.Q[s_a_list[i]] = 0;

        for i in range(0,len(signal_direction)):
            self.vehicle_queue[i] = []

    def update_queue(self):
        for i in range(0,len(self.signal_direction)):
           if(self.signal_direction[i]):
               if len(self.vehicle_queue[i]) == 0:                          #initially when the queue is empty
                  lane_vehicles = self.adjacent_roads[i*2]
                  for l in lane_vehicles:
                      counter = lane_vehicles.index(l)+ 1
                      info = [l,counter ]  # list of vehicle ID, counter
                      self.vehicle_queue[i].append(info)

               else:
                    for n in range(len(self.vehicle_queue[i])):
		      if self.adjacent_roads[i*2][n] != self.vehicle_queue[i][n][0]:
		         self.vehicle_queue[i][n][0] = self.adjacent_roads[i*2][n] 
                         self.vehicle_queue[i][n][1] = n
		      else:
                         self.vehicle_queue[i][n][1] = self.vehicle_queue[i][n][1] + 1 


    #Check the Red signal Violation
    def check_signal_violation(self):
        violation = [0,0,0,0]
        for i in range(0,len(self.signal_direction)):
            if(self.signal_direction[i]):
                if(i == 0) : 
                    violation[0] = self.monitor_vehicle(self.signal[0], self.adjacent_roads, i)
                if(i == 1) :
                    violation[1] = self.monitor_vehicle(self.signal[1], self.adjacent_roads, i)
                if(i == 2) :
                    violation[2] = self.monitor_vehicle(self.signal[2], self.adjacent_roads, i)
                if(i == 3) :
                    violation[3] = self.monitor_vehicle(self.signal[3], self.adjacent_roads, i)
        return violation
                 
    
    #Function to check the vehicle position at the red signal
    def monitor_vehicle(self,signal, adjacent_roads, i):
        my_lane    = adjacent_roads[i*2]
        current_id = my_lane[-1]  #vehicle_id of the car at the signal (intersection)
       
        if signal == 'R':
            if len(self.vehicle_queue[i]) > 0:
              if(current_id != self.vehicle_queue[i][-1][0]):
                return 1
              else:
                return 0
        else:
            return 0


    #Function to the check the vehicle's vanished
    def check_vehicle_vanished(self, vid, adjacent_roads):
         cnt = 0
         for i in range(0,len(adjacent_roads)):
                if(vid in adjacent_roads[i]):
                    cnt = cnt + 1
         if(cnt == 0):  #vehicle vanished
             return 1
         else :
             return 0
                    
    
    #Call this function when you move the car i.e when the signal is green
    #Check the collision at the signal
    def check_collision_at_signal(self):
        collision = 0
        for i in range(0,len(self.signal_direction)):
            if(self.signal_direction[i]):
                if(i == 0) : 
                    collision = collision + self.collision_check(self.signal[0], self.adjacent_roads, i)
                if(i == 1) :
                    collision = collision + self.collision_check(self.signal[1], self.adjacent_roads, i)
                if(i == 2) :
                    collision = collision + self.collision_check(self.signal[2], self.adjacent_roads, i)
                if(i == 3) :
                    collision = collision + self.collision_check(self.signal[3], self.adjacent_roads, i)
        return collision

    #Function to check if a collision has happened after the green signal
    def collision_check(self, signal, adjacent_roads, i):
        vid_vanish_check = 0
        if len(self.vehicle_queue[i]):
            if self.vehicle_queue[i][-1][0] != None:
               vid_vanish_check = self.check_vehicle_vanished(self.vehicle_queue[i][-1][0], adjacent_roads)
        return vid_vanish_check


#Update adjacent lanes variable of traffic light class based on input from V group
def update_vehicles(traffic_intersection,vehicle_id):
    x = traffic_intersection.location[0]
    y = traffic_intersection.location[1]
    for i in range(0,len(traffic_intersection.signal_direction)):
            if(traffic_intersection.signal_direction[i]):
                if (i == 0):
                    x1 = x
                    if x == 62 and y == 62:
                      y1 = y + 3
                    else:
                      y1 = y + 31
                    #'k = '[' + str(x1) + ',' + str(y1) +'],[' + str(x) + ','+ str(y)+ ']'
                    k = [(x1,y1),(x,y)]
                if (i == 1):
                    x1 = x
                    if x == 0 and y == 0:
                      y1 = y - 3
                    else:
                      y1 = y - 31
                    #'k = '[' + str(x1) + ',' + str(y1) +'],[' + str(x) + ','+ str(y)+ ']'
                    k = [(x1,y1),(x,y)]
                if (i == 2):
                    if x == 62 and y == 0:
                      x1 = x + 3
                    else:
                      x1 = x + 31
                    y1 = y 
                    #'k = '[' + str(x1) + ',' + str(y1) +'],[' + str(x) + ','+ str(y)+ ']'
                    k = [(x1,y1),(x,y)]
                if (i == 3):
                    if x == 0 and y == 62:
                      x1 = x - 3
                    else:
                      x1 = x - 31
                    y1 = y
                #'k1 = '[' + str(x1) + ',' + str(y1) +'],[' + str(x) + ','+ str(y)+ ']'
                k1 = [(x1,y1),(x,y)]
                #'k2 = '[' + str(x) + ',' + str(y) +'],[' + str(x1) + ','+ str(y1)+ ']'
                k2 = [(x,y),(x1,y1)]
                traffic_intersection.adjacent_roads.insert(i*2,vehicle_id[k1])
                traffic_intersection.adjacent_roads.insert(i*2+1,vehicle_id[k2])
            else:
                traffic_intersection.adjacent_roads.insert(i*2,None)
                traffic_intersection.adjacent_roads.insert(i*2+1,None)

             
# Update waiting time for each vehicle based on vehicle movement
def update_waiting_time(traffic_intersection):
    waiting_time = 0
    for i in range(0,4):
        v_l = traffic_intersection.vehicle_queue[i]
        if v_l:                              #if vehicle queue is not empty
            for v in v_l:
                if v[0] is not None:                     #if vehicle ID is not zero
		    slot_number = [int(i) for i in range(0,len(v_l)) if v_l[i][0] == v[0]]
                    waiting_time = waiting_time + v[1] - slot_number[0] - 1   #(waiting_time = (counter - slot number))
    return waiting_time

# Reward Calculation
def calc_reward(traffic_intersection,collision_detected):
    w_t = update_waiting_time(traffic_intersection)
    reward = -w_t
    if collision_detected:                     # if there is a collision, 10% penalty
        reward = reward - 0.1 * reward
    return reward

def get_length(vehicle_list):
   count = 0
   for v in vehicle_list:
	   if v[0] is not None:                    # Vehicle ID is not zero
		   count = count + 1
   return count

# Get Current State based on queue length in all directions
def get_state(traffic_intersection):
    queue_length = []
    for i in range(0,len(traffic_intersection.signal_direction)):
        if(traffic_intersection.signal_direction[i]):
           v_l = traffic_intersection.vehicle_queue[i]
           length = get_length(v_l)
           if length < 3:
        	queue_length.insert(i,'L')
           elif length >=3 and length < 5:
        	queue_length.insert(i,'M')
           else:
        	queue_length.insert(i,'H')
        else:
              queue_length.insert(i,None)
    state = (queue_length[0],queue_length[1],queue_length[2],queue_length[3])
    return state


# epsilon-greedy action selection
def epsilon_greedy(Q, state,action_list,eps):
    """Selects epsilon-greedy action for supplied state"""
    if np.random.random() > eps:            # select greedy action with probability epsilon
        Q_state = []
        sa_pair = []
        s_a_list = Q.keys() #Q_s_a
        for i in s_a_list:
            if i[0] == state:
              sa_pair.append(i)
              Q_state.append(Q[i])
        Q_max = max(Q_state)
        s_a = sa_pair[Q_state.index(Q_max)]
	return s_a[1]
    else:                                   # otherwise, select an action randomly
	nA = len(action_list)
	index = random.choice(np.arange(nA))
        return action_list[index]

def update_q_learning(alpha, gamma, Q, state, action, reward, next_state):
    """Returns updated Q-value for the most recent experience."""
    s_a = (state,action)
    Q_state = []
    s_a_list = Q.keys()
    for i in s_a_list:
        if i[0] == state:
          Q_state.append(Q[i])
    Q_max = max(Q_state)
    new_value = Q[s_a] + (alpha * (reward + gamma * Q_max - Q[s_a])) # get updated value
    return new_value


#Car tracing for one car from 0,0 to 62,65
def car_tracing(timestep,vehicle_id):

	lane = 0
	i = i +1
	if timestep > 0 and timestep < 3:
	   lane = 1
	elif timestep > 2 and timestep < 33:
	   lane = 2
        elif timestep >=33 and timestep < 63:
	   lane = 3
	elif timestep >= 63 and timestep < 93:
	   lane = 4
        elif timestep >= 93 and timestep < 123:
	   lane = 5
	elif timestep >= 123 and timestep < 125:
	   lane = 6

	if lane == 1:
  	   if i != 0:
  	      vehicle_id['[0,-3],[0,0]'][i-1] = 0
  	   vehicle_id['[0,-3],[0,0]'][i] = 'V_1'
  
        if lane == 2:
            if i != 0:
  		 vehicle_id['[0,0],[0,31]'][i-1] = 0
  	    else:
  		 vehicle_id['[0,-3],[0,0]'][1] = 0
  	    vehicle_id['[0,0],[0,31]'][i] = 'V_1'
             
        if lane == 3:
  	   if i != 0:
  	      vehicle_id['[0,31],[0,62]'][i-1] = 0
  	   else:
  		vehicle_id['[0,0],[0,31]'][29] = 0
  	   vehicle_id['[0,31],[0,62]'][i] = 'V_1'
  
        if lane == 4:
  	  if i != 0:
  	     vehicle_id['[0,62],[31,62]'][i-1] = 0
  	  else:
  	     vehicle_id['[0,31],[0,62]'][29] = 0
  	  vehicle_id['[0,62],[31,62]'][i] = 'V_1'
  
        if lane == 5:
  	  if i != 0:
  	    vehicle_id['[31,62],[62,62]'][i-1] = 0
  	  else:
  	    vehicle_id['[0,62],[31,62]'][29] = 0
  	  vehicle_id['[31,62],[62,62]'][i] = 'V_1'
  
        if lane == 6:
           if i != 0:
  	     vehicle_id['[62,62],[62,65]'][i-1] = 0
  	   else:
  	     vehicle_id['[31,62],[62,62]'][29] = 0
       	   vehicle_id['[62,62],[62,65]'][i] = 'V_1'







