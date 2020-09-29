=======
OpenTUMflex
=======

An open-source Python based flexibility model to quantify and price the flexibility of household devices.

Publication
===========
[Z. You: Flexibility quantification and pricing of household heat pump and combined heat and power unit, ISGT-Europe, 2019](http://dx.doi.org/10.1109/isgteurope.2019.8905594)

Description
===========

With the increasing share of renewable energy, alternative methods are ought to provide power system ancillary services to ensure stable operation of the electricity grids. Recent research have inclined their interests towards the aggregation of the small-scale system flexibility potentials to accommodate the grid variations. The advancements towards local flexibility markets (LFMs) allow prosumers participation in the solving grid congestion problems. In order to allow prosumers to interact with the LFMs and submit their bids, a flexibility estimation is required. This research proposes an open-source flexibility estimation model that quantifies all possible flexibilities from the available prosumer devices.

Features
===========
* OpenTUMFlex uses (mixed integer) linear programming model to obatin the cost-optimal operational plans of household devices. 
* It calculates the flexibility of household devices and finds its marginal prices
* It considers reoptimization as a solution when the flexibility is called by the system operator 
* It focuses on the flexibility of PV, battery, Electric Vehicle (EV), Heat Pump, Combined Heat and Power (CHP)
* It allows suitable formats which can be directly used in FlexMarket (ReFlex, comax and ALF).

Installation
===========
1. First of all you need to install python distrubution as follows:
   * (recommend) [Pycharm](https://www.jetbrains.com/pycharm/) include all the tools needed in OpenTUMFlex exceplt the solver. You can follow the instuctions in the offcial website and install it easily.
   * [Anaconda](https://www.anaconda.com/) is also widely used as Python editor. 
2. [download](https://github.com/tum-ewk/OpenTUMFlex.py/archive/master.zip) or clone (with [git](https://github.com/tum-ewk/OpenTUMFlex.py)) this repository to a directory of your choice.

Input file formats
===========
OpenTUMflex accepts two different file formats (.xlsx/.csv) as input. An example input file is available inside the folder test->data. CSV files reduces the overall optimization time. THe model converts Excel file into CSV files for future use.  

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
