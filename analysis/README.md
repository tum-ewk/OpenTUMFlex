# Analysis Toolbox

This folder contains toolboxes that use the opentumflex package to perform various studies. 

## EV Case Study

The run_ev_case_study.py executes a sample case study for the quantification of flexibility of electric vehicles. The case study can be used to analyze the impact of different controller/user strategies, pricing tariffs, and charging power levels on the flexibility of electric vehicles. A thorough case study has been published here: https://doi.org/10.3390/en13215617.

### [Input](input/) 
As an input, a small data set with 100 vehicle availabilities is stored in the input folder in a csv format. Furthermore, real-time prices are stored in a hdf format [here](input/RTP/). 

### Output
The case study stores all generated flexibility offers as txt-files in the folder output/. Furthermore, all figures will be stored in the figures/-folder. The program will create subfolders for all charging power levels and pricing strategies and the aggregated results. All folders will be created at execution. 

### Duration
Depending on your computer, the cores and the configuration of the case study the execution time will differ. The configured example takes 3 minutes with an i7 processor and 24 GB RAM. 
