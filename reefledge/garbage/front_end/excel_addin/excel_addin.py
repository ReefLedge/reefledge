import os
os.environ['MPLBACKEND'] = 'Qt5Agg'
os.environ['RUNNING_XLWINGS_UDF_SERVER'] = 'True'

import sys


def unload_reefledge_package() -> None:
    k: str
    for k in sys.modules.copy():
        if 'reefledge' in k:
            sys.modules.pop(k)


from reefledge.reefledge.front_end.excel_addin import package_update

if package_update.conditionally_update_reefledge_package():
    unload_reefledge_package()

from reefledge.reefledge.front_end.excel_addin._excel_addin import *
