"""
The "gen_offers.py" saves flexibility offers in .xlsx/.csv format
"""

__author__ = "Babu Kumaran Nalini"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Babu Kumaran Nalini"
__email__ = "babu.kumaran-nalini@tum.de"
__status__ = "Development"

import os


def save_offers(my_ems,  device,  filetype='xlsx'):
    """
    

    Parameters
    ----------
    my_ems : Dictionary 
        Dictionary file of the ems model with flex offer dataframe.
    device : String,  e.g. 'ev'/'pv'
        Device whose offers need to be saved as XLSX/CSV file.
    filetype : String, optional
        The default is 'xlsx'. Input can be 'xlsx'/'csv'

    Returns
    -------
    None.

    """
    # Find path and check for a result folder
    cwd = os.getcwd()
    mdir = "results" 
    path = os.path.join(cwd, mdir)
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = device+'_flex_offers'
    new_cwd = os.path.join(path, file_name)
    
    # Save flex offers in the requested format
    if filetype == '.xlsx':
        my_ems['flexopts'][device].to_excel(new_cwd+'.xlsx')
        print("Excel file generated! Available on " + path)
    elif filetype == 'csv':
        my_ems['flexopts'][device].to_csv(new_cwd+'.csv', sep=';', decimal='.', index=False)
        print("CSV file generated! Available on " + path)
    else:
        print('Unknown file format - .xlsx/.csv supported')
