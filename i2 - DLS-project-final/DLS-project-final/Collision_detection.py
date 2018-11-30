#!/usr/bin/python
# -*- coding: utf-8 -*-
# I gave a green signal and there is a car there --> collision
#Penality for the same

class collision_detection:
    
    def __init__(self, signal_direction, location, adjacent_roads):
        self.signal_direction = signal_direction
        self.location         = location
        self.adjacent_roads   = adjacent_roads
    
    
    #Function to get the position of the vehicle
    def get_vehicle_position(self, vehicle_id, adjacent_roads):
        vehicle_position = 0
        for i in range(0,len(adjacent_roads)):
                if(vehicle_id in adjacent_roads[i]):
                    vehicle_position[0] = adjacent_roads[i].index(vehicle_id)
                    vehicle_position[1] = i;
        return vehicle_position
        
    
    #Function to the check the vehicle's vanished
    def check_vehicle_vanished(self, vehicle_id, adjacent_roads):
         cnt = 0
         for i in range(0,len(adjacent_roads)):
                if(vehicle_id in adjacent_roads[i]):
                    cnt = cnt + 1
         if(cnt == 0):  #vehicle vanished
             return 1
         else :
             return 0
                    
    
    #Call this function when you move the car i.e when the signal is green
    #Check the collision at the signal
    def check_collision_at_signal(self, signal_direction, signal, adjacent_roads, other_vid):
        collision = 0
        for i in range(0,len(signal_direction)):
            if(signal_direction[i]):
                if(i == 0) : 
                    collision = self.collision_check(signal[0], adjacent_roads, i, other_vid)
                if(i == 1) :
                    collision = self.collision_check(signal[1], adjacent_roads, i, other_vid)
                if(i == 2) :
                    collision = self.collision_check(signal[2], adjacent_roads, i, other_vid)
                if(i == 3) :
                    collision = self.collision_check(signal[3], adjacent_roads, i, other_vid)
        return collision
                 
    #Call this at the Reg signal before you give green
    def check_other_vid_at_signal(self, signal_direction, adjacent_roads):
        other_vid = []
        for i in range(0,len(signal_direction)):
            if(signal_direction[i]):
                if(i == 0) : 
                    other_vid = self.other_vid_check(adjacent_roads, i)
                if(i == 1) :
                    other_vid = self.other_vid_check(adjacent_roads, i)
                if(i == 2) :
                    other_vid = self.other_vid_check(adjacent_roads, i)
                if(i == 3) :
                    other_vid = self.other_vid_check(adjacent_roads, i)
        return other_vid
    
    
    #Function to check the vehicle positin at the red signal
    def other_vid_check(self, adjacent_roads, i):
        other_vid = 0
        my_lane    = adjacent_roads[i]
        vehicle_id = my_lane[-1]                        #vehicle_id of the car at the signal (intersection)
        current_position = self.get_vehicle_position(vehicle_id,adjacent_roads) #storing the current position of the vehicle
        for i in range(0,len(adjacent_roads)):          #get_other_vehilce_id
            if (i == current_position[1]): 
                other_vid[i] = 0
            else:
                other_vid[i] = adjacent_roads[i][0]     #The vehicle id of the car at the first index of other lane
        return other_vid
       
        
    #Function to chek if a collision has happened after the green signal
    def collision_check(self, signal, adjacent_roads, i, other_vid):
        vid_vanish_check = 0
        while(signal == 'G'):           #Wait till Green Signal is present #But the vehicle moves 2 steps ??  wait_for_2_time_steps
            continue
        #need to check if the other vehicles exist in the lanes --> if no collision
        for i in range(0,len(other_vid)):
            vid_vanish_check[i] = self.check_vehicle_vanished(other_vid[i], adjacent_roads)
        if 1 in vid_vanish_check:   #Collision check
            return 1
        else :
            return 0
      
