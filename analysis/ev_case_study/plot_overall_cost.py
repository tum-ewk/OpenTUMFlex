import matplotlib.pyplot as plt
from matplotlib import rcParams, ticker
from .calc_overall_cost import calc_overall_cost


def plot_overall_cost(overall_costs, figure_path='figures/'):
    # Create a bar plot showing the different prices
    # Set font/figure style
    rcParams["font.family"] = "Times New Roman"
    rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [6, 2.5]

    # Subplots
    ax = plt.subplot(111)
    w = 0.5
    x = [3.7, 11, 22]
    ax.bar([i - 2*w for i in x], [overall_costs['_37_total_cost_con'],
                                  overall_costs['_11_total_cost_con'],
                                  overall_costs['_22_total_cost_con']],
           label='Con', width=w, color='b', align='center')
    ax.bar([i - 1*w for i in x], [overall_costs['_37_total_cost_con_mi'],
                                  overall_costs['_11_total_cost_con_mi'],
                                  overall_costs['_22_total_cost_con_mi']], label='Con + MI', width=w)
    ax.bar(x, [overall_costs['_37_total_cost_tou'],
               overall_costs['_11_total_cost_tou'],
               overall_costs['_22_total_cost_tou']], label='ToU', width=w)
    ax.bar([i + 1*w for i in x], [overall_costs['_37_total_cost_tou_mi'],
                                  overall_costs['_11_total_cost_tou_mi'],
                                  overall_costs['_22_total_cost_tou_mi']], label='ToU + MI', width=w)
    ax.bar([i + 2*w for i in x], [overall_costs['_37_total_cost_rtp'],
                                  overall_costs['_11_total_cost_rtp'],
                                  overall_costs['_22_total_cost_rtp']], label='RTP', width=w)
    ax.xaxis_date()
    ax.autoscale(tight=True)
    ax.set_xlim([0, 25])
    # ax.set_ylim([0, 16000])
    ax.set_xticks(x)
    ax.legend(bbox_to_anchor=(1.3, 0.5), loc="center right", borderaxespad=0.5)
    ax.grid(axis='y')
    ax.set_xlabel('Maximum charging power level (kW)')
    ax.set_ylabel('Cumulated charging costs (€)')
    ax.set_xticklabels(['3.7', '11', '22'])
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.subplots_adjust(left=0.13, bottom=0.2, right=0.8, top=0.95, wspace=0.2, hspace=0.2)
    plt.savefig(figure_path + 'Total_charging_cost' + '.png', dpi=600)

    return


if __name__ == '__main__':
    overall_cost = calc_overall_cost('../output/')

    plot_overall_cost(overall_cost, figure_path='figures/')

