import pandas as pd
import analysis.ev_case_study as ev_case_study

# Read veh availabilities from file
veh_availabilities = pd.read_csv('input/chts_veh_availability.csv')
# Extract a subsample for testing
veh_availabilities = veh_availabilities[14:15]
veh_availabilities = veh_availabilities.reset_index()
# Define where the data shall be written to
output_path = 'output/'
# Maximal power charging levels
max_charging_levels = [3.7, 11, 22]
# Pricing strategies
pricing_strategies = {'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'}

# Calculate ev flexibility offers
ev_case_study.calc_ev_flex_offers(veh_availabilities,
                                  output_path=output_path,
                                  power_levels=max_charging_levels,
                                  pricing_strategies=pricing_strategies,
                                  conversion_distance_2_km=1.61,
                                  conversion_km_2_kwh=0.2,
                                  plotting=False)

# Aggregate single offers
ev_case_study.aggregate_ev_flex(veh_availabilities,
                                output_path=output_path)

# Plot number of available vehicles at home over a week (only for one power level, since it won't change)
ev_case_study.plot_n_avail_veh(output_path='output/3.7/',
                               figure_path='figures/')

# Plot aggregated flexibility offers over time
for power in max_charging_levels:
    ev_case_study.plot_opt_flex_timeseries(output_path='output/' + str(power) + '/', figure_path='figures/')

# Plot aggregated flexibility offers in a heatmap
ev_case_study.plot_flex_heatmap(output_path='output/')

# Calculate overall costs of optimal charging
overall_cost = ev_case_study.calc_overall_cost(output_path='output/')

# Plot overall cost
ev_case_study.plot_overall_cost(overall_cost, figure_path='figures/')

