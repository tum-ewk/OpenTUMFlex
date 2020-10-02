"""
The "gen_offers_alf.py" saves flexibility offers in FFE GmbH - alfmarkt .csv format
"""

__author__ = "Babu Kumaran Nalini"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Babu Kumaran Nalini"
__email__ = "babu.kumaran-nalini@tum.de"
__status__ = "Development"


import pandas as pd
from datetime import datetime 
import os


def save_offers_alf(my_ems, device):
    """
    

    Parameters
    ----------
    my_ems : Dictionary  
        Dictionary file of the ems model with flex offer dataframe.
    device : String,  e.g. 'ev'/'pv'
        Device whose offers need to be saved as CSV file.

    Returns
    -------
    None.

    """
    
    # Create empty dataframe in ALF format (German)
    df = pd.DataFrame(columns=['Uhrzeit', 'Leistung_Plan', 'Leistung-', 'Leistung+', 'Energie-',
                               'Energie+', 'Preis-', 'Preis+',  'Teilabruf',
                               'max_Anzahl_Abrufe_pro_Tag',  'max_Dauer_pro_Tag_in_h',
                               'Dauer_zwischen_zwei_Abrufen_in_h',  'max_Dauer_eines_Abrufs',
                               'min_Dauer_eines_Abrufs'], index=range(my_ems['time_data']['nsteps']))
     
    # Insert respective parameter from dictionary to the new dataframe                  
    df['Leistung_Plan'] = round(my_ems['flexopts'][device]['Sch_P'], 5)
    df['Leistung-'] = round(my_ems['flexopts'][device]['Neg_P'], 5)
    df['Leistung+'] = round(my_ems['flexopts'][device]['Pos_P'], 5)
    df['Energie-'] = round(my_ems['flexopts'][device]['Neg_E'], 5)
    df['Energie+'] = round(my_ems['flexopts'][device]['Pos_E'], 5)
    df['Preis-'] = round(my_ems['flexopts'][device]['Neg_Pr']*100, 2)
    df['Preis+'] = round(my_ems['flexopts'][device]['Pos_Pr']*100, 2)
    
    # Add UTC string to Uhrzeit(time)
    utc = " +0100"
    df['Uhrzeit'] = my_ems['time_data']['time_slots'] + utc
     
    # Add additional parameters           
    df.loc[0, 'Teilabruf'] = "Ja"
    df.loc[0, 'max_Anzahl_Abrufe_pro_Tag'] = 2.0
    df.loc[0, 'max_Dauer_pro_Tag_in_h'] = 2.25
    df.loc[0, 'Dauer_zwischen_zwei_Abrufen_in_h'] = 1.5
    df.loc[0, 'max_Dauer_eines_Abrufs'] = 1.5
    df.loc[0, 'min_Dauer_eines_Abrufs'] = 0.25
       
    # Find path and check for a result folder
    cwd = os.getcwd()
    # back_cwd = os.path.dirname(cwd)
    mdir = "flexoffers" 
    path = os.path.join(cwd, mdir)
    if not os.path.exists(path):
        os.mkdir(path)
    
    # Append CSV file name based on the date of the offers
    datetime_object = datetime.strptime(my_ems['time_data']['time_slots'][0], "%Y-%m-%d %H:%M")
    file_name = datetime_object.strftime("%Y-%m-%d") + '_' + device + 'Flex-Angebot.csv'
    new_cwd = os.path.join(path, file_name)
    
    # Save CSV file 
    df.to_csv(new_cwd, sep=';', index=False)
    print("CSV file generated - flex offers for alf markt! Available on " + new_cwd)
    # return df
