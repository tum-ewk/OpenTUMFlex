#####################
Configuring scenarios
#####################
A scenario-based approach is incorporated in the OpenTUMFlex design. The term scenarios in OpenTUMflex means cases or examples. A scenario refers to the device configurations installed in a household. For example, a scenario can refer to a household with PV, BSS and EV while a different household with just PV and HP is considered as another scenario. 

You can create scenarios of your own or modify/use the existing scenarios. The file inside ``OpenTUMflex->Scenario->scenario.py`` serves as the main file to decide which scenarios are available.

*****************
Default scenarios
*****************
Once you have successfully installed and test run your OpenTUMFle, then ``scenario_apartment`` is executed by default. You can choose to change your scenario by replacing the desired keyword in line 12 in ``example.py``. To give an idea, we have already created 8 sample scenarios inside scenario.py.

Following scenarios are created based on possible combination of devices installed at any prosumers premises. 

+---------------------------------+-----------------------------------------------+
|             Scenario            |                     Devices                   |
+=================================+===============================================+
|          ``scenario_hp``        |                   HP and boiler               |
+---------------------------------+-----------------------------------------------+
|          ``scenario_pv``        |                   PV and boiler               |
+---------------------------------+-----------------------------------------------+
|          ``scenario_bat``       |                   BSS and boiler              |
+---------------------------------+-----------------------------------------------+
|          ``scenario_ev``        |                   EV and boiler               |
+---------------------------------+-----------------------------------------------+
|    ``scenario_simple_house``    |          PV, BSS, heat storage and boiler     |
+---------------------------------+-----------------------------------------------+
| ``scenario_residential_house``  |          PV, BSS, heat storage and boiler     | 
+---------------------------------+-----------------------------------------------+
|   ``scenario_mini_apartment``   |    PV, BSS, heat storage, boiler, HP and EV   |
+---------------------------------+-----------------------------------------------+
|       ``scenario_apartment``    | PV, BSS, heat storage, boiler, CHP, HP and EV |
+---------------------------------+-----------------------------------------------+

.. admonition:: Scenario from file

   OpenTUMFlex allows to you to directly create a scenario from your input file based on the devices included. To allow this use ``scenario_fromfile`` as keyword. 

******************
Creating scenarios
******************
OpenTUMFlex allows two ways to create a new scenario.

**Using .xlsx/.csv input file** |br|

* Inside the input folder, we have added an example .xlsx file to understand the input format.
* Modify the excel cells based on your scenario.
* Add zeros to parameters in case the device is not available in your scenario.
* Point the input directory variable ``input_file=Path`` to the input .xlsx/.csv
* Use ``opentumflex.scenario_fromfile`` as the argument while calling ``run_scenario`` function. 
* To speed up the total time, we have the option to create/use CSV. See x.x.
* Remember this method uses both the input file sheets namely properties and time_series.
* This method is useful if you wish to run OpenTUMflex for a single case study.

**Using functions** |br|

* Create a new function inside ``OpenTUMflex->Scenario->scenario.py``. 
* As an example, let's say the function name is ``scenario_happyhouse``.
* Use ``opentumflex.scenario_happyhouse`` as the argument while calling the run_scenario function.
* Remember this method also uses the input file but only the time_series sheet. 
* Make changes to the .xlsx/.csv input file to amend the input time series data.
* This method is useful during analysis, e.g. modify device parameters iteratively.

************
File formats
************
**Input file formats**

* OpenTUMflex accepts two different file formats (.xlsx/.csv) as input. 
* Example input file is available inside the input folder. 
* CSV files are generally preferred as they reduce the overall optimization time.
* XLSX file can be also used for better readability and practice. 
* The model has an inbuilt option to convert any .xlsx file to .csv files.

.. Warning::
   Do not change the structure of the .csv/.xlsx files. OpenTUMFlex can read the inputs only using the defined sheet settings. Sample .csv/.xlsx formats are available in the input folder. 
   
**Converting .xlsx files to .csv**

To convert your .xlsx file to .csv format, run ``example.py`` once with .xlsx file as your input and make sure to assign ``convert_input_tocsv= True``. After the execution a CSV file is automatically generated and saved into the input folder. For the subsequent runs you may use the CSV format and disable ``convert_input_tocsv = False``.

**Output file format**

* OpenTUMFlex can generate a variety of plots such as optimal operation, SOC, flexibility, etc.
* These images can be stored as JPG files in the output folder. 
* X.X discusses the arguments to save the output images.
* Flexibility offers of each device in suitable formats can be generated as .csv files
* Formatted Output files can be used in FlexMarket trading - e.g. ALF/ COMAX platforms.
* X.X discusses the arguments to save the output files in defined format.

**************
I/O structure
**************

**Input file structure**

The input file consists of two parts which are namely the device properties and the forecasted time series values. In XLSX format, it is implemented as two sheets namely ``properties`` and ``time_series``. In the CSV format, the time series data is concatenated with the device properties and are seperated by ``;``. 

The following parameters are used for defining device properties. 

+--------+--------------------------------------------------------------------------------------------+
| Device |                                         Parameters                                         |
+========+============================================================================================+
| PV     | Peak power                                                                                 |
+--------+--------------------------------------------------------------------------------------------+
| BSS    |  Charging/discharging Power (Min & Max), Initial SOC, Capacity, Efficiency                 |
+--------+--------------------------------------------------------------------------------------------+
| EV     |  Charging/discharging Power (Min & Max), Initial & End SOC, Capacity, Efficiency           |
+--------+--------------------------------------------------------------------------------------------+
| HP     |  Min & Max Power utilized                                                                  |
+--------+--------------------------------------------------------------------------------------------+
| CHP    |  Min & Max Power utilized                                                                  |
+--------+--------------------------------------------------------------------------------------------+
| HS     |  Charging/discharging Power (Min & Max), Initial SOC, Capacity, Efficiency, Self discharge |
+--------+--------------------------------------------------------------------------------------------+


The following parameters are used for defining the time series forecast data.

+---------------------------------+-----------------------------------------------+
|             Forecast data       |                        Units                  |
+=================================+===============================================+
| Temperature                     |  °C                                           |
+---------------------------------+-----------------------------------------------+
| PV power                        |  kW                                           |
+---------------------------------+-----------------------------------------------+
| EV availability data            |  Binary                                       |
+---------------------------------+-----------------------------------------------+
| Heat load                       |  kW                                           |
+---------------------------------+-----------------------------------------------+
| Electrical load                 |  kW                                           |
+---------------------------------+-----------------------------------------------+
| Electricity import price        |  €/kWh                                        |
+---------------------------------+-----------------------------------------------+
| Electricity export price        |  €/kWh                                        | 
+---------------------------------+-----------------------------------------------+
| Gas price                       |  €/kWh                                        |
+---------------------------------+-----------------------------------------------+

**Output file structure** 

The output of the OpenTUMFlex model is the flexibility table that can be used for trading. The flexibility table consists of the scheduled operation along with the possible flexibility service that can be offered in terms of power, energy and price. 

The flexibility energy refers to the amount of negative or positive flexibility power that can last over a specific period (timesteps). The flexibility price is the cost that prosumer bids for providing a specific flexibility service. An excerpt from a sample table is provided below and uses COMAX flexibilty platform based output format. 

+------------------+--------+--------+-------+--------+---------+--------+--------+
|       Time       |  Sch_P | Neg_P  | Pos_P |  Neg_E |  Pos_E  | Neg_Pr | Pos_Pr |
+==================+========+========+=======+========+=========+========+========+
| 2019-12-18 01:30 | 0.6615 | -3.661 | 2.338 | -0.915 |  1.169  | -0.298 | 0.279  |
+------------------+--------+--------+-------+--------+---------+--------+--------+
| 2019-12-18 01:45 | 0.5808 | -3.580 | 2.419 | -0.895 |  0.604  | -0.298 | 0.279  |
+------------------+--------+--------+-------+--------+---------+--------+--------+
| 2019-12-18 02:00 | 0.0000 | -3.000 | 3.000 | -3.000 |  0.750  | -0.287 | 0.279  |
+------------------+--------+--------+-------+--------+---------+--------+--------+
| 2019-12-18 02:15 | 0.0000 | -3.000 | 3.000 | -3.000 |  0.750  | -0.287 | 0.279  |
+------------------+--------+--------+-------+--------+---------+--------+--------+



.. Line breaks HTML code
.. |br| raw:: html

      <br>