EV Case Study
====

This readme gives a short overview of all the modules that are used to perform the ev case study. The modules are listed in the order of their execution in a full case study, as described in the run_ev_case_study.py

1. calc_ev_flex_offers.py: calculates the flexibility offers for all vehicle availabilities.
2. aggregate_ev_flex.py: reads and aggregates all single ev flex offers for weekdays and weekends.
3. plot_time_series.py: plots number of vehicles during a week and also the optimal and flexible power for weekdays and weekends.
4. plot_flex_heatmap.py: plots heat maps for positive and negative flexibility. 
5. calc_overall_cost.py: reads and sums up the overall cost of the optimal charging schedules.
6. plot_overall_cost.py: plots the overall costs for the charging power levels and the pricing and controller strategies. 
