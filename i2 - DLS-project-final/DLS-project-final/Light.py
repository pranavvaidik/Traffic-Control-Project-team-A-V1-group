#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:34:42 2018

@author: pasha_bhai
"""

from Traffic_signal import Traffic_Lights,get_state,calc_reward,update_vehicles,epsilon_greedy,update_q_learning

class Traffic():
    
    
     def __init__(self):
        
        vehicle_id = self.get_map()

        #Creating Traffic objects
        self.get_traffic_signal[7] = Traffic_Lights([0,62], [vehicle_id.get([(-3,62),(0,62)]),vehicle_id.get([(0,62),(31,62)]),vehicle_id.get([(0,62),(0,31)])],[0,1,1,1])
        self.get_traffic_signal[8] = Traffic_Lights([31,62],[vehicle_id.get([(0,62),(31,62)]),vehicle_id.get([(31,62),(62,62)]),vehicle_id.get([(31,62),(31,31)])],[0,1,1,1])
        self.get_traffic_signal[9] = Traffic_Lights([62,62],[vehicle_id.get([(31,62),(62,62)]),vehicle_id.get([(-62,62),(62,65)]),vehicle_id.get([(62,62),(62,31)])],[1,1,0,1])

        #Signals in the middle
        self.get_traffic_signal[4] = Traffic_Lights([0,31], [vehicle_id.get([(0,62),(0,31)]),vehicle_id.get([(0,31),(31,31)]),vehicle_id.get([(0,31),(0,0)])],[1,1,1,0])
        self.get_traffic_signal[5] = Traffic_Lights([31,31],[vehicle_id.get([(0,31),(31,31)]),vehicle_id.get([(31,31),(62,31)]),vehicle_id.get([(31,31),(31,0)]),vehicle_id.get([(31,31),(31,62)])],[1,1,1,1])
        self.get_traffic_signal[6] = Traffic_Lights([62,31],[vehicle_id.get([(31,31),(62,31)]),vehicle_id.get([(62,31),(62,0)]),vehicle_id.get([(62,31),(62,62)])],[1,1,0,1])

        #Bottom most signals
        self.get_traffic_signal[1] = Traffic_Lights([0,0], [vehicle_id.get([(0,31),(0,0)]),vehicle_id.get([(0,0),(31,0)]),vehicle_id.get([(0,0),(0,-3)])],[1,1,1,0])
        self.get_traffic_signal[2] = Traffic_Lights([31,0],[vehicle_id.get([(0,0),(31,0)]),vehicle_id.get([(31,0),(62,0)]),vehicle_id.get([(31,0),(31,31)])],[1,0,1,1])
        self.get_traffic_signal[3] = Traffic_Lights([62,0],[vehicle_id.get([(31,0),(62,0)]),vehicle_id.get([(62,0),(62,31)]),vehicle_id.get([(62,0),(65,0)])],[1,0,1,1])

         
     def update_traffic_lights(self, congestion_map):
         
         green_light = []
         current_state = {}
         action = {}
          
         for i in range(1,10):
      
            TL = self.get_traffic_signal[i]
      
            current_state[i] = get_state(TL)
      
            action[i] = epsilon_greedy(TL.Q,current_state[i],TL.action_list,TL.epsilon) 
        
            TL.signal = action[i]
      
            #Update traffic lights 
            if 'G' in action[i]:
                if action[i][0] == 'G' : direction = 'NORTH'
                if action[i][1] == 'G' : direction = 'SOUTH'
                if action[i][2] == 'G' : direction = 'EAST'
                if action[i][3] == 'G' : direction = 'WEST'
            else:
                direction = None
      
            green_light.append(direction)
            
         return green_light


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