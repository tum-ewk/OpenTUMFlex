# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:52:10 2019

@author: ge57vam
"""

#
# this part is to import the component module
# like: import heatpump as hp
#       import weatherdata as wdata
#
#
#
#

import flexproduct as flexpd
import prognosis as pns
import heatpump as hp
import elecvehicle as ev
import combinedhheatpower as chp
import flexibilityoffers as flexoff
import flexibilityplatform as flexplat


def ems(p1,p2,p3):    
    
    ID
    flexdevice
    flexprod
    optopt
    userpref
    
    #
    # In this function the chosen flexibility time will be realized and the reoptimization will proceed automatically
    #
    #
    
    flexreopt
    
    #
    #in this function the optimal schedual will be generated for each device
    #
    #
    
    optopt 
    
    #
    #in this section the optimal schedual will be sent to each device
    #
    #
    
    optsend
    
    #
    #in this section the flexibility for each device will be generated
    #
    #
    
    flexcalc
    
    #
    #in this section the EMS get the parameter from the FlexProduct and give the output format of the flexibility
    #
    #
    flexout
    
    
if __name__ == "__main__":  
# 3th argument for input file, and 4th argument for the result folder (dont have to be the same)    
    ems(p1,p2,p3)
    

