import matplotlib.pyplot as plt
import pandas as pd


def plot_overall_cost(overall_costs, figure_path='figures/'):
    # Create a bar plot showing the different prices
    # Set font/figure style
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 10
    # figsize und so
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))
    # plotten
    overall_costs.T.plot.bar(ax=ax)
    # Achsen und so
    plt.grid(axis='y')
    plt.xticks(rotation='horizontal')
    plt.xlabel('Maximum charging power level (kW)')
    # plt.ylim([0, 25])
    plt.ylabel('Cumulated charging costs (€)')
    # legende
    plt.legend(bbox_to_anchor=(1.1, 0.5), loc="center right", borderaxespad=0.2)
    # speichern
    plt.tight_layout()
    plt.show() # -> optional
    # plt.savefig(figure_path + 'total_charging_cost' + '.png', dpi=600)


if __name__ == '__main__':
    overall_costs = {'3.7': {'ToU': 14.538897959183677, 'Con': 18.976346938775514,
                            'ToU + MI': 14.540111016893244, 'Con + MI': 18.97749908073416, },
                     '11': {'ToU': 15.888316326530614, 'Con': 20.238877551020405,
                            'ToU + MI': 15.889490335526514, 'Con + MI': 20.240000003239743, },
                     '22': {'ToU': 16.581938775510196, 'Con': 20.938775510204074,
                            'ToU + MI': 16.58311048543813, 'Con + MI': 20.939909765919552, }}

    df = pd.DataFrame(overall_costs)

    plot_overall_cost(df, figure_path='../figures/')

