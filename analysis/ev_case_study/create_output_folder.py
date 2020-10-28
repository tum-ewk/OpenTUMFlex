from pathlib import Path
import os
import shutil


def create_output_folder(output_path='output/',
                         power_levels=[3.7, 11, 22],
                         pricing_strategies=['ToU', 'Constant', 'ToU_mi', 'Con_mi', 'RTP']):
    # Delete existing output folder
    if os.path.exists(output_path):
        shutil.rmtree(path=output_path, ignore_errors=True)
    # Create output folder
    Path(output_path).mkdir(parents=True, exist_ok=False)
    # Go through all price strategies
    for price in pricing_strategies:
        # Go through all power levels
        for power in power_levels:
            # print('Pricing: ' + price + ' and Power: ' + str(power))
            # Create subfolder for different power levels
            Path(output_path + str(power)).mkdir(parents=True, exist_ok=True)
            # Create subfolder for different pricing strategies
            Path(output_path + str(power) + '/' + price).mkdir(parents=True, exist_ok=True)
