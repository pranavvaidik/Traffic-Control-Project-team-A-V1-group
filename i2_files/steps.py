#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:26:12 2018

@author: pasha_bhai
"""

from I2_Light import Traffic as TL_i2
traffic = TL_i2()	
m = traffic.get_map()
m[((0,-3),(0,0))] = [23,25]

for i in range(10):
    traffic.update_traffic_lights(m)