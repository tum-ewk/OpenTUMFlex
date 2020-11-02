# Analysis Toolbox

This folder contains toolboxes that use the opentumflex package to perform various studies. 

## EV Case Study

The run_ev_case_study.py executes a sample case study for the quantification of flexibility of electric vehicles. The case study can be used to analyze the impact of different controller/user strategies, pricing tariffs, and charging power levels on the flexibility of electric vehicles. A thorough case study has been published here: https://doi.org/10.3390/en13215617.

### Input 
As an input, a small data set with 100 vehicle availabilities is stored in the input folder in a csv format. Furthermore, real-time prices are stored in the folder input/RTP/ in a hdf-format. 

### Output
The case study will store the individual flexibility offers as txt files in the folder output/. The folder will be created at execution. 

### Duration
Depending on your computer, the cores and the configuration of charging power levels, controller strategies and pricing tariffs, the execution will take approximately 5-10 minutes. 
