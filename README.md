OpenTUMflex
=======

An open-source Python based flexibility model to quantify and price the flexibility of household devices.


## Description

Increasing share of renewable energy requires alternative methods to provide power system ancillary services to ensure stable operation of the electricity grids. Recent research have inclined their interests towards the aggregation of the small-scale system flexibility potentials to accommodate the grid variations. The advancements towards local flexibility markets (LFMs) allow prosumers participation in the solving grid congestion problems. In order to allow prosumers to interact with the LFMs and submit their bids, a flexibility estimation is required. This research proposes an open-source flexibility estimation model that quantifies all possible flexibilities from the available prosumer devices.


## Features

* OpenTUMFlex uses mixed integer linear programming (MILP) to obtain cost-optimal operational plans for household devices. 
* Calculates the flexibility potential and flexibility prices of household devices.
* Supported devices: PV, Battery Storage Systems (BSS), Electric Vehicle (EV), Heat Pump (HP), Combined Heat and Power (CHP).
* Outputs flexibility offers of each device in suitable formats which can be directly used in FlexMarket (ReFlex, comax and ALF).


## Installation

1. Install a Python distrubution (64-bit installation recommended): [PyCharm](https://www.jetbrains.com/pycharm/)/[Miniconda](https://docs.conda.io/en/latest/miniconda.html).
2. [Download](https://github.com/tum-ewk/OpenTUMFlex.py/archive/master.zip) or clone the OpenTUMflex repository `git clone https://github.com/tum-ewk/OpenTUMFlex.py.git`
3. Create an environment and install the [requirements](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/requirements.txt) file using [Anaconda prompt](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)/[PyCharm](https://www.jetbrains.com/help/idea/conda-support-creating-conda-virtual-environment.html) plugin.
    * Pycharm: `File->Settings->Project->Python Interpreter->Setting icon->Add->New environment->Base interpretor-Python 3.7`
4. Install the optimization modeling language: [Pyomo](http://www.pyomo.org/installation)
    * PyCharm: Add Pyomo package using `File->Settings->Project->Python Interpreter->Add(+)->Search for Pyomo->Install`
    * Manual installation: `pip install pyomo` (only necessary if the automatic installation of packages did not detect Pyomo)
5. Install a Solver: [GLPK](https://pypi.org/project/glpk/). You can also use Gurobi or other MILP solvers. 


## Test your installation

* Run the [example.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/example_1.py) file to test if the OpenTUMflex model is correctly installed. 

* You will get following results if everything works perfectly:

![](https://user-images.githubusercontent.com/42935122/97186850-1b97b500-17a2-11eb-9a86-97674ffad6d0.png)|![](https://user-images.githubusercontent.com/40628466/97216385-09c80900-17c6-11eb-98ac-615b77bbed0b.png)
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/40628466/97215739-23b51c00-17c5-11eb-8915-19cce5d8f42c.png)|![](https://user-images.githubusercontent.com/40628466/97215750-26b00c80-17c5-11eb-8795-9c3032ef36a8.png)


## Getting started

* **Change your scenario (use predefined sample configurations in [scenario.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/opentumflex/scenarios/scenarios.py)):**
  * `scenario_hp`: Heat storage, boiler and HP
  * `scenario_simple_house`: PV, BSS, heat storage and boiler
  * `scenario_apartment`: PV, BSS, heat storage, boiler, CHP, HP and EV
  
  **Change the arguments in run_scenario() to enable/disable each plot:
   * show_opt_res: show the optimiaztion results (power and heat balance, SoCs)
   * show_opt_res: save the optimiaztion results in spreedsheet 
   * show_flex_res: show the flexibility results (power, energy and price)
   * show_aggregated_flex: show the summay of all flexibility power and prices

* **Create your own scenario:** 
   * A scenario based approach is incorported in OpenTUMflex design. Here, a scenario refers to the device configurations installed at the prosumer premises. For example: A scenario can refer to just a household with PV, BSS and EV. 
   * Once you have succesfully installed OpenTUMflex, you can choose or create your own scenario inside [scenario.py](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/opentumflex/scenarios/scenarios.py). To give an idea, we have already created 10 sample scenarios. 
   * For more information refer to our [documentation](https://github.com/tum-ewk/OpenTUMFlex.py/wiki).
   
* **Analysis Toolbox:**
   * [Quantifying the Flexibility of Electric Vehicles in Germany and California](/https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/analysis/README.md)


<!---
## Conflict of Interest: 

The authors declare no conflict of interest. All authors have equally contributed to the development of this software. 
--->

## References

<sub>[Z. You, B. K. Nalini, M. Zade, P. Tzscheutschler and U. Wagner, "Flexibility quantification and pricing of household heat pump and combined heat and power unit," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905594.](http://dx.doi.org/10.1109/isgteurope.2019.8905594)<sub>

<sub>[B. K. Nalini, M. Eldakadosi, Z. You, M. Zade, P. Tzscheutschler and U. Wagner, "Towards Prosumer Flexibility Markets: A Photovoltaic and Battery Storage Model," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905622.](http://dx.doi.org/10.1109/isgteurope.2019.8905622)<sub>

<sub>[M. Zade, Y. Incedag, W. El-Baz, P. Tzscheutschler and U. Wagner, "Prosumer Integration in Flexibility Markets: A Bid Development and Pricing Model," 2018 2nd IEEE Conference on Energy Internet and Energy System Integration (EI2), Beijing, 2018, pp. 1-9, doi: 10.1109/EI2.2018.8582022.](http://dx.doi.org/10.1109/EI2.2018.8582022)<sub>


## License

OpenTUMFlex can be used to optimize and calculate a households flexibility potential and price it. 
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
