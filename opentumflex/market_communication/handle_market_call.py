"""
The "example_1.py" module demonstrates an example to calculate flexibility assuming 
the house to have all pv, battery, ev, hp, chp. 
"""
__author__ = "Babu Kumaran Nalini"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Babu Kumaran Nalini"
__email__ = "babu.kumaran-nalini@tum.de"
__status__ = "Development"

# import optimization module
from opentumflex.optimization.model import create_model, solve_model, extract_res


# import flex devices modules
from opentumflex.flexibility.flex_pv import calc_flex_pv
from opentumflex.flexibility.flex_bat import calc_flex_bat
from opentumflex.flexibility.flex_hp import calc_flex_hp
from opentumflex.flexibility.flex_ev import calc_flex_ev
from opentumflex.flexibility.flex_chp import calc_flex_chp


def run_reopt(my_ems, plot_fig=False):   
    """
    

    Parameters
    ----------
    my_ems : Dictionary
        Dictionary of the opentumflex model.
    plot_fig : Binary, optional
        Select if reoptimization plots are required or not.
        The default is False.

    Returns
    -------
    my_ems : Dictionary
        Updated dictionary of the opentumflex model.

    """
    
    # Select device under reoptimization
    device = my_ems['reoptim']['device']
    
    # Calculate device state changes before reoptimization
    if device == 'pv':
        my_ems = calc_flex_response_pv(my_ems)    
    elif device == 'bat':
        my_ems = calc_flex_response_bat(my_ems)
    elif device == 'ev':
        my_ems = calc_flex_response_ev(my_ems)
    elif device == 'hp':
        my_ems = calc_flex_response_hp(my_ems)
    
    # Check and start reoptimization if possible    
    if my_ems['reoptim']['status'] == 1:    
        if plot_fig: print('Reoptimization Possible')
        opt_res = opt(my_ems)  
        my_ems['reoptim']['optplan'] = run_opt(opt_res, my_ems, plot_fig=plot_fig, result_folder='data/')        
        
        # Calculate flexibility after reoptimization
        my_ems['reoptim']['flexopts'] = {}
        my_ems['reoptim']['flexopts']['pv'] = calc_flex_pv(my_ems, reopt=1)
        my_ems['reoptim']['flexopts']['bat'] = calc_flex_bat(my_ems, reopt=1)
        my_ems['reoptim']['flexopts']['hp'] = calc_flex_hp(my_ems, reopt=1)
        
    return my_ems


def calc_flex_response_pv(my_ems):
    """
    

    Parameters
    ----------
    my_ems : Dictionary
        Dictionary of the opentumflex model.

    Returns
    -------
    my_ems : Dictionary
        Updated dictionary of the opentumflex model.

    """
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    if f_type == 'Neg':
        # Flexibility information    
        f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
        f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
        if f_pow != 0:
            f_steps = int(round(f_ene*ntsteps/f_pow))
            my_ems['reoptim']['status'] = 1
        else:
            f_steps = 0
            print('No flexibility found')    
            my_ems['reoptim']['status'] = 0
            
        if my_ems['reoptim']['status'] == 1:            
            # Update initial steps for reoptimization
            my_ems['time_data']['isteps'] = rstep+f_steps+1
            
            # Battery SOC at flexibility time step
            s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
            e_bSOC = my_ems['optplan']['bat_SOC'][rstep+f_steps]    
            bat_max_e = my_ems['devices']['bat']['stocap']
        
            if s_bSOC >= e_bSOC:
                tot_dis = 0
                for i in range(rstep,rstep+f_steps):
                    tot_dis = tot_dis + my_ems['optplan']['bat_output_power'][i]
                tot_dis = tot_dis*f_steps/ntsteps
                if abs(f_ene) >= tot_dis:
                    e_bal = abs(f_ene) - tot_dis
                    e_bal_soc = e_bal*100/bat_max_e
                    if s_bSOC + e_bal_soc <= 100 :
                        my_ems['devices']['bat']['initSOC'] = s_bSOC + e_bal_soc
                    else:
                        my_ems['devices']['bat']['initSOC'] = 100
                else:
                    soc_red = tot_dis - abs(f_ene)
                    soc_red = soc_red*100/bat_max_e    #in %
                    my_ems['devices']['bat']['initSOC'] = s_bSOC - soc_red      
            else:
                SOC_added = abs(f_ene*100/bat_max_e)
                if e_bSOC + SOC_added > 100: # Include SOC limits
                    my_ems['devices']['bat']['initSOC'] = 100
                else: 
                    my_ems['devices']['bat']['initSOC'] = e_bSOC + SOC_added     
    
    elif f_type == 'Pos':
        my_ems['reoptim']['status'] = 0
        print('No positive flexibility for PV')   
    
    return my_ems


def calc_flex_response_bat(my_ems):
    """
    

    Parameters
    ----------
    my_ems : Dictionary
        Dictionary of the opentumflex model.

    Returns
    -------
    my_ems : Dictionary
        Updated dictionary of the opentumflex model.

    """
    
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    # Flexibility information    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
        my_ems['reoptim']['status'] = 1
    else:
        f_steps = 0
        print('No flexibility found \n')    
        my_ems['reoptim']['status'] = 0
    
    # Update initial steps for reoptimization        
    if my_ems['reoptim']['status'] == 1:               
        my_ems['time_data']['isteps'] = rstep+f_steps
        
        # Battery SOC at flexibility time step
        e_bSOC = my_ems['optplan']['bat_SOC'][rstep+f_steps-1]    
        bat_max_e = my_ems['devices']['bat']['stocap']
        
        if f_type == 'Neg':
           SOC_added = abs(f_ene*100/bat_max_e)
           if e_bSOC + SOC_added > 100:
               my_ems['devices']['bat']['initSOC'] = 100
           else:
               my_ems['devices']['bat']['initSOC'] = e_bSOC + SOC_added
           
        elif f_type == 'Pos':
            SOC_rem = abs(f_ene*100/bat_max_e)
            if e_bSOC - SOC_rem < 0:
                my_ems['devices']['bat']['initSOC'] = 0
            else: 
                my_ems['devices']['bat']['initSOC'] = e_bSOC - SOC_rem
       
    return my_ems  


def calc_flex_response_ev(my_ems):
    """
    

    Parameters
    ----------
    my_ems : Dictionary
        Dictionary of the opentumflex model.

    Returns
    -------
    my_ems : Dictionary
        Updated dictionary of the opentumflex model.

    """
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    # Flexibility information    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
        my_ems['reoptim']['status'] = 1
    else:
        f_steps = 0
        print('No flexibility found \n')    
        my_ems['reoptim']['status'] = 0
            
    if my_ems['reoptim']['status'] == 1:         
        # Update initial steps for reoptimization
        my_ems['time_data']['isteps'] = rstep+f_steps+1
        
        # Battery SOC at flexibility time step
        # s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
        e_bSOC = my_ems['optplan']['EV_SOC'][rstep+f_steps]    
        bat_max_e = my_ems['devices']['ev']['stocap']
        
        if f_type == 'Neg':
           SOC_added = abs(f_ene*100/bat_max_e)
           if e_bSOC + SOC_added > 100:
               my_ems['devices']['bat']['initSOC'] = 100
           else:
               my_ems['devices']['bat']['initSOC'] = e_bSOC + SOC_added
           
        elif f_type == 'Pos':
            SOC_rem = abs(f_ene*100/bat_max_e)
            if e_bSOC - SOC_rem < 0:
                my_ems['devices']['bat']['initSOC'] = 0
            else: 
                my_ems['devices']['bat']['initSOC'] = e_bSOC - SOC_rem     
                
    return my_ems  


def calc_flex_response_hp(my_ems):
    """
    

    Parameters
    ----------
    my_ems : Dictionary
        Dictionary of the opentumflex model.

    Returns
    -------
    my_ems : Dictionary
        Updated dictionary of the opentumflex model.

    """
    
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    # Flexibility information    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
        my_ems['reoptim']['status'] = 1
    else:
        f_steps = 0
        print('No flexibility found \n')    
        my_ems['reoptim']['status'] = 0
        
    if my_ems['reoptim']['status'] == 1:         
        # Update initial steps for reoptimization
        my_ems['time_data']['isteps'] = rstep+f_steps+1
        
        # Battery SOC at flexibility time step
        # s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
        e_hSOC = my_ems['optplan']['SOC_heat'][rstep]    
        sto_max_e = my_ems['devices']['sto']['stocap']
        COP_avg = sum(my_ems['optplan']['HP_COP'][rstep:rstep+f_steps])/f_steps
        
        if f_type == 'Neg':
           SOC_added = abs(COP_avg*f_ene*100/sto_max_e)
           if e_hSOC + SOC_added > 100:
               my_ems['devices']['sto']['initSOC'] = 100
           else:
               my_ems['devices']['sto']['initSOC'] = e_hSOC + SOC_added
           
        elif f_type == 'Pos':
            SOC_rem = abs(COP_avg*f_ene*100/sto_max_e)
            print(SOC_rem)
            if e_hSOC - SOC_rem < 0:
                my_ems['devices']['sto']['initSOC'] = 0
            else: 
                my_ems['devices']['sto']['initSOC'] = e_hSOC - SOC_rem 
                
    return my_ems      

