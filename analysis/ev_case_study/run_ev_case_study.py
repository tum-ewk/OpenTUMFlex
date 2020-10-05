import pandas as pd
from .ev_flex_computation import calc_ev_flex_offers
from .ev_opt_flex_aggregation import aggregate_ev_flex
from .time_plot_analysis import plot_flex_timeseries
from .hm_plot_analysis import plot_flex_heatmap
from .calc_overall_cost import calc_overall_cost

# Read veh availabilities from file
veh_availabilities = pd.read_csv('input/chts_veh_availability.csv')
# Extract a subsample for testing
veh_availabilities = veh_availabilities[0:20]
# Define where the data shall be written to
output_path = 'output/'
# Maximal power charging levels
max_charging_levels = [3.7, 11, 22]
# Pricing strategies
pricing_strategies = {'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'}

# Calculate ev flexibility offers
calc_ev_flex_offers(veh_availabilities,
                    output_path=output_path,
                    power_levels=max_charging_levels,
                    pricing_strategies=pricing_strategies,
                    conversion_distance_2_km=1.61,
                    conversion_km_2_kwh=0.2,
                    plotting=False)

# Aggregate single offers
aggregate_ev_flex(veh_availabilities)

# Plot aggregated flexibility offers over time
for power in max_charging_levels:
    plot_flex_timeseries(power)

# Plot aggregated flexibility offers in a heatmap
plot_flex_heatmap()

# Calculate overall costs of optimal charging
total_cost_tou, total_cost_con, total_cost_tou_mi, total_cost_con_mi, total_cost_rtp = calc_overall_cost()
