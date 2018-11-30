#!/usr/bin/python

from Traffic_signal       import Traffic_signal,get_state,calc_reward,update_vehicles,epsilon_greedy,update_q_learning
from Red_Signal_Violation import violation
from Collision_detection  import collision_detection

get_traffic_signal = {}

global vehicle_id

#Sample dictionary received from V group
vehicle_id = {'[0,0],[0,31]':['V_1',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
	              '[0,31],[0,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,0],[31,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'V_15',0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,0],[0,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,0],[0,-3]':[0,0],\
		      '[0,-3],[0,0]':[0,0],\
		      '[31,0],[62,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[31,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,0],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,31],[31,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'V_6',0,0,0,0,0,0,0,0,0,0],\
		      '[0,31],[0,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,62],[0,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,31],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,31],[0,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[65,0]':[0,0],\
		      '[65,0],[62,0]':[0,0],\
		      '[31,31],[31,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,62],[31,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,62],[0,31]':[0,0,0,0,0,0,0,'V_9',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,0],[0,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[0,31],[0,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[62,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,31],[62,0]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,0],[62,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[31,62],[62,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,62],[31,62]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,31],[62,62]':[0,0,0,0,0,0,0,0,0,0,0,'V_3',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,62],[62,31]':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
		      '[62,62],[62,65]':[0,0],\
		      '[62,65],[62,62]':[0,0],\
		      '[0,62],[-3,62]':[0,0],\
		      '[-3,62],[0,62]':[0,0],\
		    }


# Top most signals (location, adjacent roads, signal_direction(N,S,E,W))
get_traffic_signal[7] = Traffic_signal([0,62], [vehicle_id.get('[-3,62],[0,62]'),vehicle_id.get('[0,62],31,62]'),vehicle_id.get('[0,62],[0,31]')],[0,1,1,1])
get_traffic_signal[8] = Traffic_signal([31,62],[vehicle_id.get('[0,62],31,62]'),vehicle_id.get('[31,62],[62,62]'),vehicle_id.get('[31,62],[31,31]')],[0,1,1,1])
get_traffic_signal[9] = Traffic_signal([62,62],[vehicle_id.get('[31,62],[62,62]'),vehicle_id.get('[-62,62],[62,65]'),vehicle_id.get('[62,62],[62,31]')],[1,1,0,1])

#Signals in the middle
get_traffic_signal[4] = Traffic_signal([0,31], [vehicle_id.get('[0,62],[0,31]'),vehicle_id.get('[0,31],[31,31]'),vehicle_id.get('[0,31],[0,0]')],[1,1,1,0])
get_traffic_signal[5] = Traffic_signal([31,31],[vehicle_id.get('[0,31],[31,31]'),vehicle_id.get('[31,31],[62,31]'),vehicle_id.get('[31,31],[31,0]'),vehicle_id.get('[31,31],[31,62]')],[1,1,1,1])
get_traffic_signal[6] = Traffic_signal([62,31],[vehicle_id.get('[31,31],[62,31]'),vehicle_id.get('[62,31],[62,0]'),vehicle_id.get('[62,31],[62,62]')],[1,1,0,1])

#Bottom most signals
get_traffic_signal[1] = Traffic_signal([0,0], [vehicle_id.get('[0,31],[0,0]'),vehicle_id.get('[0,0],[31,0]'),vehicle_id.get('[0,0],[0,-3]')],[1,1,1,0])
get_traffic_signal[2] = Traffic_signal([31,0],[vehicle_id.get('[0,0],[31,0]'),vehicle_id.get('[31,0],[62,0]'),vehicle_id.get('[31,0],[31,31]')],[1,0,1,1])
get_traffic_signal[3] = Traffic_signal([62,0],[vehicle_id.get('[31,0],[62,0]'),vehicle_id.get('[62,0],[62,31]'),vehicle_id.get('[62,0],[65,0]')],[1,0,1,1])

#At each timestep(3600/2) execute this at each intersection
for t in range(1,1801):
    
    current_state = {}
    action = {}
    green_light = []
    
    for i in range(1,10):

      TL = get_traffic_signal[i]

      current_state[i] = get_state(TL)

      action[i] = epsilon_greedy(TL.Q,current_state[i],TL.action_list,TL.epsilon)       # epsilon-greedy action selection

      #Update traffic lights and send this info to V group
      if 'G' in action[i]:
          if action[i][0] == 'G' : direction = 'North'
          if action[i][1] == 'G' : direction = 'South'
          if action[i][2] == 'G' : direction = 'East'
          if action[i][3] == 'G' : direction = 'West'
      else:
          direction = 'None'

      green_light.append('GLDT' + direction + 'for' + str(TL.location))
    
        
    for i in range(1,10):
      
      TL = get_traffic_signal[i]
       
      update_vehicles(TL)

      TL.update_queue()

      next_state = get_state(TL)
      
      # Detect Collisions --> Need to code this
     
      # take action A, observe R
      reward = calc_reward(TL, no_collisions)      
      
      TL.Q[current_state[i]][action] = update_q_learning(TL.alpha,TL.gamma,TL.Q, current_state[i], action[i], reward, next_state)        
      
      #Need to add code to detect red signal violation and throughput calculation




