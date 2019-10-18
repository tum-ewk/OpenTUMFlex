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



import ems as HEMS

import flexproduct as flexpd
import forecast as fcst
import heatpump as hp
import elecvehicle as ev
import optimization as opt
import combinedhheatpower as chp
import flexibilityoffers as flexoff
import flexibilityplatform as flexplat
import flexpackage.flexplot as flexplot

  
 

if __name__ == '__main__':
        
    
    
    #fill the data stucture 
    weatherdata = csv.read('path')
    fcst = fcst(weatherfcst = weatherdata, loadfcst = '' )
    
    
        
    #initialize the ems 
    ems = HEMS(ID = '01', forecast = fcst, flexproduct = flexpd, )
    
    # using the data
    ems.fcst['weatherdata']
    
    #add new device
    
    ems.devices.append('hp', quantity = 2, initialize = 'default')
    ems.devices.append('pv', quantity = 1, peakpower = 10, speficications = '')
    
    
    #calculate the optimal timetable
    
    ems.optplan = opt.calculation(time_invervall = 15)
    
    #calculate the flexibility and load results
    
    ems.flex(ID = '3351')['power'] = flexoff.calc_flex(options = 'all')['power']
    ems.flex(ID = '3351')['price'] = flexoff.calc_flex(options = 'all')['price']
    
    #visualize the results
    
    flexplot(ems);

    #
    #in this section the optimal schedual will be sent to each device
    #
    #
    
    ems.opt_send()
    
 
   
    
    

    

