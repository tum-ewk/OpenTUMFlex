from datetime import datetime
import os
import pandas as pd


def save_results(ems, path):
    """

    :param ems:
    :param path:
    :return:
    """
    now = datetime.now().strftime('%Y%m%dT%H%M')
    resultfile = os.path.join(path, 'result_optimization_{}.xlsx'.format(now))
    writer = pd.ExcelWriter(resultfile)
    df = pd.DataFrame(data=ems['optplan'])
    df.to_excel(writer, 'operation_plan', merge_cells=False)
    writer.save()  # save
