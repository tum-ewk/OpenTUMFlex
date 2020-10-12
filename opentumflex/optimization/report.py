"""
The "report.py" saves the optimization results in given path as spreadsheet
"""

__author__ = "Zhengjie You"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Zhengjie You"
__email__ = "zhengjie.you@tum.de"
__status__ = "Development"

from datetime import datetime
import os
import pandas as pd


def save_results(ems, path):
    """ save the optimization results in given path as spreadsheet
    Args:

        - ems: ems model instance
        - path: path where the results data is to be saved, e.g. path= r'tests\data'

    """

    try:
        os.mkdir(path)
    except OSError:
        print("Opmtization result are being saved in %s" % path)
    else:
        print("Successfully created the directory %s " % path)

    now = datetime.now().strftime('%Y%m%dT%H%M')
    resultfile = os.path.join(path, 'result_optimization_{}.xlsx'.format(now))
    writer = pd.ExcelWriter(resultfile)
    df = pd.DataFrame(data=ems['optplan'])
    df.to_excel(writer, 'operation_plan', merge_cells=False)
    writer.save()  # save
