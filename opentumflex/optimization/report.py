from datetime import datetime
import os
import pandas as pd


def save_results(ems, path):
    """ save the optimization results in given path as spreadsheet
    Args:

        - ems: ems model instance
        - path: path where the results data is to be saved, e.g. path= r'tests\data'

    """
    now = datetime.now().strftime('%Y%m%dT%H%M')
    resultfile = os.path.join(path, 'result_optimization_{}.xlsx'.format(now))
    writer = pd.ExcelWriter(resultfile)
    df = pd.DataFrame(data=ems['optplan'])
    df.to_excel(writer, 'operation_plan', merge_cells=False)
    writer.save()  # save
