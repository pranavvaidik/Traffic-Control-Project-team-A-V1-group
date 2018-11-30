#!/usr/bin/python
# -*- coding: utf-8 -*-
            
class violation:
    
    def __init__(self,signal_direction,adjacent_roads,signal):
        self.signal_direction = signal_direction
        self.adjacent_roads   = adjacent_roads
        self.signal           = signal
    
    
    #Function to get the position of the vehicle
    def get_vehicle_position(self,vehicle_id,adjacent_roads):
        for i in range(0,len(adjacent_roads)):
                if(vehicle_id in adjacent_roads[i]):
                    vehicle_position = adjacent_roads[i].index(vehicle_id)
        return vehicle_position
        
    
    #Check the Red signal Violation
    def check_signal_violation(self,signal_direction,signal,adjacent_roads):
        violation = 0
        for i in range(0,len(signal_direction)):
            if(signal_direction[i]):
                if(i == 0) : 
                    violation = self.monitor_vehicle(signal[0], adjacent_roads, i)
                if(i == 1) :
                    violation = self.monitor_vehicle(signal[1], adjacent_roads, i)
                if(i == 2) :
                    violation = self.monitor_vehicle(signal[2], adjacent_roads, i)
                if(i == 3) :
                    violation = self.monitor_vehicle(signal[3], adjacent_roads, i)
        return violation
                 
    
    #Function to check the vehicle positin at the red signal
    def monitor_vehicle(self,signal, adjacent_roads, i):
        my_lane    = adjacent_roads[i]
        vehicle_id = my_lane[-1]  #vehicle_id of the car at the signal (intersection)
        current_position = self.get_vehicle_position(vehicle_id,adjacent_roads) #storing the current position of the vehicle
       
        while(signal == 'RED'):
            position_check = self.get_vehicle_position(vehicle_id,adjacent_roads) 
            if(position_check != current_position):
                return 1
            else:
                continue;
