OpenTUMflex
=======

An open-source Python based flexibility model to quantify and price the flexibility of household devices.

Description
===========

Increasing share of renewable energy requires alternative methods to provide power system ancillary services to ensure stable operation of the electricity grids. Recent research have inclined their interests towards the aggregation of the small-scale system flexibility potentials to accommodate the grid variations. The advancements towards local flexibility markets (LFMs) allow prosumers participation in the solving grid congestion problems. In order to allow prosumers to interact with the LFMs and submit their bids, a flexibility estimation is required. This research proposes an open-source flexibility estimation model that quantifies all possible flexibilities from the available prosumer devices.

Features
===========
* OpenTUMFlex uses mixed integer linear programming (MILP) to obtain cost-optimal operational plans for household devices. 
* Calculates the flexibility potential and flexibility prices of household devices.
* Supported devices: PV, Battery Storage Systems (BSS), Electric Vehicle (EV), Heat Pump, Combined Heat and Power (CHP).
* Output flexibility offers of each devices in suitable formats which can be directly used in FlexMarket (ReFlex, comax and ALF).

Installation
===========
1. Install a Python distrubution (64-bit installation recommended): [PyCharm](https://www.jetbrains.com/pycharm/)/[Miniconda](https://docs.conda.io/en/latest/miniconda.html) 
2. Install a Solver: [GLPK](https://pypi.org/project/glpk/). You can also use Gurobi or other MILP solvers. 
3. [Download](https://github.com/tum-ewk/OpenTUMFlex.py/archive/master.zip) or clone the OpenTUMflex repository `git clone https://github.com/tum-ewk/OpenTUMFlex.py.git`
4. Create an environment and install the [requirements](https://github.com/tum-ewk/OpenTUMFlex.py/blob/master/requirements.txt) file.
    * Using [Anaconda prompt](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
    * Using [PyCharm](https://www.jetbrains.com/help/idea/conda-support-creating-conda-virtual-environment.html) 


Getting started
===========
1. Run the given **example.py** in the **tests** folder. 
2. You will learn how to: 
    * set up the time interval, start and end time.
    * read input data from **tests/data/input_data.xlsx**
    * change/add device parameters (boiler and heat pump) by using **update(devices(device_name))**
    * obtain the optimal plans of each device
    * calculate the flexibility offers of battery and heat pump
    * visualize the results
3. If you have installed all the packages/solver, you will get results (e.g. electricity balance and flexibility of battery) as follows:
<img src="https://github.com/zxc8063898/emstest/blob/master/Figure_1-1.png" alt="electricity balance" width="380" height="250"> <img src="https://github.com/zxc8063898/emstest/blob/master/Figure_6.png" alt="electricity balance" width="380" height="250">

4. For more information refer to our [documentaion](https://github.com/tum-ewk/OpenTUMFlex.py/wiki/Usage-and-Functions-in-OpenTUMFlex)

Input file formats
===========
OpenTUMflex accepts two different file formats (.xlsx/.csv) as input. An example input file is available inside the folder test->data. CSV files reduces the overall optimization time. THe model converts Excel file into CSV files for future use.  

References
===========
[Z. You, B. K. Nalini, M. Zade, P. Tzscheutschler and U. Wagner, "Flexibility quantification and pricing of household heat pump and combined heat and power unit," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905594.](http://dx.doi.org/10.1109/isgteurope.2019.8905594)

[B. K. Nalini, M. Eldakadosi, Z. You, M. Zade, P. Tzscheutschler and U. Wagner, "Towards Prosumer Flexibility Markets: A Photovoltaic and Battery Storage Model," 2019 IEEE PES Innovative Smart Grid Technologies Europe (ISGT-Europe), Bucharest, Romania, 2019, pp. 1-5, doi: 10.1109/ISGTEurope.2019.8905622.](http://dx.doi.org/10.1109/isgteurope.2019.8905622)

[M. Zade, Y. Incedag, W. El-Baz, P. Tzscheutschler and U. Wagner, "Prosumer Integration in Flexibility Markets: A Bid Development and Pricing Model," 2018 2nd IEEE Conference on Energy Internet and Energy System Integration (EI2), Beijing, 2018, pp. 1-9, doi: 10.1109/EI2.2018.8582022.](http://dx.doi.org/10.1109/EI2.2018.8582022)

License
===========
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
