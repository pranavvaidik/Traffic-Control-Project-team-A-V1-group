#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:34:42 2018

@author: pasha_bhai
"""
import math
from Traffic_signal import Traffic_Lights,get_state,calc_reward,update_vehicles,epsilon_greedy,update_q_learning

class Traffic():
    
     get_traffic_signal = [None]*9
     
    
     def __init__(self):
        
        vehicle_id = self.get_map()
        
        #Creating Traffic objects
        self.get_traffic_signal[6] = Traffic_Lights([0,62], [vehicle_id.get((0,31),(0,62)),None,None,vehicle_id.get((0,62),(0,31)),vehicle_id.get((31,62),(0,62)),vehicle_id.get((0,62),(31,62)),vehicle_id.get((-3,62),(0,62)),vehicle_id.get((0,62),(-3,62))],[0,1,1,1])
        self.get_traffic_signal[7] = Traffic_Lights([31,62],[vehicle_id.get((31,31),(31,62)),None,None,vehicle_id.get((31,62),(31,31)),vehicle_id.get((62,62),(31,62)),vehicle_id.get((31,62),(62,62)),vehicle_id.get((0,62),(31,31)),vehicle_id.get((31,62),(0,62))],[0,1,1,1])
        self.get_traffic_signal[8] = Traffic_Lights([62,62],[vehicle_id.get((62,31),(62,62)),vehicle_id.get((62,62),(62,65)),vehicle_id.get((62,65),(62,62)),vehicle_id.get((62,62),(62,31)),None,None,vehicle_id.get((31,62),(62,62)),vehicle_id.get((62,62),(31,62))],[1,1,0,1])

        #Signals in the middle
        self.get_traffic_signal[3] = Traffic_Lights([0,31], [vehicle_id.get((0,0),(0,31)),vehicle_id.get((0,31),(0,62)),vehicle_id.get((0,62),(0,31)),vehicle_id.get((0,31),(0,0)),vehicle_id.get((31,31),(0,31)),vehicle_id.get((0,31),(31,31)),None,None],[1,1,1,0])
        self.get_traffic_signal[4] = Traffic_Lights([31,31],[vehicle_id.get((31,0),(31,31)),vehicle_id.get((31,31),(31,62)),vehicle_id.get((31,62),(31,31)),vehicle_id.get((31,31),(31,0)),vehicle_id.get((62,31),(31,31)),vehicle_id.get((31,31),(62,31)),vehicle_id.get((0,31),(31,31)),vehicle_id.get((31,31),(0,31))],[1,1,1,1])
        self.get_traffic_signal[5] = Traffic_Lights([62,31],[vehicle_id.get((62,0),(62,31)),vehicle_id.get((62,31),(62,62)),vehicle_id.get((62,62),(62,31)),vehicle_id.get((62,31),(62,0)),None,None,vehicle_id.get((31,31),(62,31)),vehicle_id.get((62,31),(31,31))],[1,1,0,1])

        #Bottom most signals
        self.get_traffic_signal[0] = Traffic_Lights([0,0], [vehicle_id.get((0,-3),(0,0)),vehicle_id.get((0,0),(0,31)),vehicle_id.get((0,31),(0,0)),vehicle_id.get((0,0),(0,-3)),vehicle_id.get((31,0),(0,0)),vehicle_id.get((0,0),(31,0)),None,None],[1,1,1,0])
        self.get_traffic_signal[1] = Traffic_Lights([31,0],[None,vehicle_id.get((31,0),(31,31)),vehicle_id.get((31,31),(31,0)),None,vehicle_id.get((62,0),(31,0)),vehicle_id.get((31,0),(62,0)),vehicle_id.get((0,0),(31,0)),vehicle_id.get((31,0),(0,0))],[1,0,1,1])
        self.get_traffic_signal[2] = Traffic_Lights([62,0],[None,vehicle_id.get((62,0),(62,31)),vehicle_id.get((62,31),(62,0)),None,vehicle_id.get((65,0),(62,0)),vehicle_id.get((62,0),(65,0)),vehicle_id.get((31,0),(62,0)),vehicle_id.get((62,0),(31,0))],[1,0,1,1])

         
     def update_traffic_lights(self, congestion_map):
         
         green_light        = [[],[],[]]
         check_green_action = [[],[],[]]
         
         current_state = {}
         action = {}
         vehicle_id = congestion_map
         red_signal_violation_count = 0
         collisions_count = 0
            
         # Execute this every timestep after vehicle movement
         for i in range(0,9):
          
           self.TL = self.get_traffic_signal[i]
           current_state[i] = get_state(self.TL)
           action[i] = epsilon_greedy(self.TL.Q,current_state[i],self.TL.action_list,self.TL.epsilon) 
           
           #Update adjacent roads variable from info received from V group
           update_vehicles(self.TL,vehicle_id)
           
           #check for red signal violation
           red_signal_violation = self.TL.check_signal_violation()

           for n in range(0,len(red_signal_violation)):
               if red_signal_violation[n] == 1:
                   red_signal_violation_count+=1
           
           #check for collisions
           no_collisions = self.TL.check_collision_at_signal()
           collisions_count+=1
          
           #Update vehicle queue and counter associated with it to calculate waiting time
           self.TL.update_queue()
          
           next_state = get_state(self.TL)

           #Calculate reward
           reward = calc_reward(self.TL, no_collisions)    
        
           #update Q values based on reward, s, a
           s_a = (current_state[i],action[i])
           self.TL.Q[s_a] = update_q_learning(self.TL.alpha,self.TL.gamma,self.TL.Q, current_state[i], action[i], reward, next_state) 
     
           #TODO : throughput calculation
           
         for i in range(0,9):
      
            self.TL = self.get_traffic_signal[i]
      
            current_state[i] = get_state(self.TL)
      
            action[i] = epsilon_greedy(self.TL.Q,current_state[i],self.TL.action_list,self.TL.epsilon) 
        
            self.TL.signal = action[i]
      
            #Update traffic lights 
            if 'G' in action[i]:
                if action[i][0] == 'G' : direction = 'NORTH'
                if action[i][1] == 'G' : direction = 'SOUTH'
                if action[i][2] == 'G' : direction = 'EAST'
                if action[i][3] == 'G' : direction = 'WEST'
            else:
                direction = None
            
            
            
            k = i/3
            green_light[k].append(direction)
            check_green_action[k].append(action[i])
            #print green_light
            #print check_green_action
            
            self.epsilon = self.TL.epsilon
            
         return green_light
         
     
     #Function to reset epsilon
     def reset(self, testing=True):

         if testing:
		 	 self.epsilon = 0
			 self.learning_rate = 0
         else:
			 a = 0.05
			 c = -5
			 if self.epsilon == 1:
			    	t = 0
			 else:
				    t = (math.log(1/self.epsilon-1) - c)/a
			 t=t+1
			 self.epsilon = 1/(math.exp(a*t+c)+1)
         for i in range(9):
	         self.get_traffic_signal[i].epsilon = self.epsilon
         
         return


     def get_map(self):
        
        vehicle_id = dict()
		
        #initializing the entry/exit road segments
        vehicle_id[((-3,62),(0,62))] = [None]*2
        vehicle_id[((0,62),(-3,62))] = [None]*2 

        vehicle_id[((62,65),(62,62))] = [None]*2
        vehicle_id[((62,62),(62,65))] = [None]*2
		
        vehicle_id[((62,0),(65,0))] = [None]*2
        vehicle_id[((65,0),(62,0))] = [None]*2

        vehicle_id[((0,0),(0,-3))] = [None]*2
        vehicle_id[((0,-3),(0,0))] = [None]*2
		
        #initializing the rest of the road segments
        vehicle_id[((0,62),(31,62))] = [None]*30	
        vehicle_id[((31,62),(0,62))] = [None]*30
		
        vehicle_id[((62,62),(31,62))] = [None]*30	
        vehicle_id[((31,62),(62,62))] = [None]*30

        vehicle_id[((0,62),(0,31))] = [None]*30	
        vehicle_id[((0,31),(0,62))] = [None]*30
		
        vehicle_id[((31,31),(31,62))] = [None]*30	
        vehicle_id[((31,62),(31,31))] = [None]*30
		
        vehicle_id[((62,62),(62,31))] = [None]*30	
        vehicle_id[((62,31),(62,62))] = [None]*30
		
        vehicle_id[((0,31),(31,31))] = [None]*30	
        vehicle_id[((31,31),(0,31))] = [None]*30
		
        vehicle_id[((31,31),(62,31))] = [None]*30	
        vehicle_id[((62,31),(31,31))] = [None]*30
		
        vehicle_id[((0,31),(0,0))] = [None]*30	
        vehicle_id[((0,0),(0,31))] = [None]*30
		
        vehicle_id[((31,31),(31,0))] = [None]*30	
        vehicle_id[((31,0),(31,31))] = [None]*30
		
        vehicle_id[((62,0),(62,31))] = [None]*30	
        vehicle_id[((62,31),(62,0))] = [None]*30
		
        vehicle_id[((31,0),(0,0))] = [None]*30	
        vehicle_id[((0,0),(31,0))] = [None]*30
		
        vehicle_id[((31,0),(62,0))] = [None]*30	
        vehicle_id[((62,0),(31,0))] = [None]*30
        
        return vehicle_id
