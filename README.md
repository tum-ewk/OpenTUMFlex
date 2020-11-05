OpenTUMflex
=======

An open-source Python based flexibility model to quantify and price the flexibility of household devices.


## Description

The increasing share of renewable energy requires alternative methods to provide power system ancillary services to ensure a stable operation of the electricity grids. Recent research has inclined their interests towards the aggregation of the small-scale system flexibility potentials to accommodate the grid variations. The advancements towards local flexibility markets (LFMs) allow prosumers participation in solving grid congestion problems. In order to allow prosumers to interact with the LFMs and submit their bids, a flexibility estimation is required. This research proposes an open-source flexibility estimation model that quantifies all possible flexibilities from the available prosumer devices.


## Features

* OpenTUMFlex uses mixed-integer linear programming (MILP) to obtain cost-optimal operational plans for household devices. 
* Calculates the flexibility potential and flexibility prices of household devices.
* Supported devices: PV, Battery Storage Systems (BSS), Electric Vehicle (EV), Heat Pump (HP), Combined Heat and Power (CHP).
* Outputs flexibility offers of each device in suitable formats that can be directly used in FlexMarket (ReFlex, comax and ALF).


## Installation

### Environment and required packages
The easiest way to create the environment and install all required packages is via Ana- or Miniconda.
1. Install Anaconda or Miniconda
2. Create the virtual environment: open an "Anaconda Prompt" -> type `conda env create -f environment_v1.0.yml`
3. Activate conda environment 

	a. In the command prompt type `conda activate OpenTUMFlex`
	
	b. In an IDE like PyCharm go to `File->Settings->Project->Python Interpreter->Show all->Add->Conda Environment->Existing environment->Select folder->OK` 

### Test your installation
Test
Run the [example_1.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/example_1.py) file to test if the OpenTUMflex model is correctly installed. You will obtain the following results if everything works perfectly:

![](https://user-images.githubusercontent.com/42935122/97186850-1b97b500-17a2-11eb-9a86-97674ffad6d0.png)|![](https://user-images.githubusercontent.com/40628466/97216385-09c80900-17c6-11eb-98ac-615b77bbed0b.png)
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/40628466/97215739-23b51c00-17c5-11eb-8915-19cce5d8f42c.png)|![](https://user-images.githubusercontent.com/40628466/97215750-26b00c80-17c5-11eb-8795-9c3032ef36a8.png)


## Getting started
A scenario-based approach is incorporated in the OpenTUMflex design. Here, a scenario refers to the device configurations installed at the prosumer premises. For example, a scenario can refer to just a household with PV, BSS and EV. 

* **Change your scenario**
   Once you have successfully installed OpenTUMflex, you can choose to change your scenario by replacing the desired name in line 12 in [example.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/example_1.py). To give an idea, we have already created 10 sample scenarios inside [scenario.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/opentumflex/scenarios/scenarios.py). 
   
  *For example the following scenarios portray the devices installed at the prosumers premises*
   * `scenario_hp`: Heat storage, boiler and HP
   * `scenario_simple_house`: PV, BSS, heat storage and boiler
   * `scenario_apartment`: PV, BSS, heat storage, boiler, CHP, HP and EV
  
  *Change the arguments to enable/disable each plot:*
   * `show_opt_res`: plot the optimization results (energy balance and device SoCs)
   * `save_opt_res`: save the optimization results in a spreedsheet 
   * `show_flex_res`: plot the flexibility results of all available devices individually (power, energy and price)
   * `show_aggregated_flex`: plot the cumulative flexibility power and price of all the available devices

* **Create your own scenario:** 
   * Refer our [documentation](https://github.com/tum-ewk/OpenTUMFlex.py/wiki).
   
* **Analysis Toolbox:**
   * [EV Case Study](analysis/)


<!---
## Conflict of Interest: 

The authors declare no conflict of interest. All authors have equally contributed to the development of this software. 
--->

## References

<sub>[Z. You, B. K. Nalini, M. Zade, P. Tzscheutschler and U. Wagner, "Flexibility quantification and pricing of household heat pump and combined heat and power unit," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905594.](http://dx.doi.org/10.1109/isgteurope.2019.8905594)<sub>

<sub>[B. K. Nalini, M. Eldakadosi, Z. You, M. Zade, P. Tzscheutschler and U. Wagner, "Towards Prosumer Flexibility Markets: A Photovoltaic and Battery Storage Model," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905622.](http://dx.doi.org/10.1109/isgteurope.2019.8905622)<sub>

<sub>[M. Zade, Y. Incedag, W. El-Baz, P. Tzscheutschler and U. Wagner, "Prosumer Integration in Flexibility Markets: A Bid Development and Pricing Model," 2018 2nd IEEE Conference on Energy Internet and Energy System Integration (EI2), Beijing, 2018, pp. 1-9, doi: 10.1109/EI2.2018.8582022.](http://dx.doi.org/10.1109/EI2.2018.8582022)<sub>


## License

OpenTUMFlex can be used to optimize and calculate a household flexibility potential and price it. 
Copyright (C) 2020 TUM-EWK 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
