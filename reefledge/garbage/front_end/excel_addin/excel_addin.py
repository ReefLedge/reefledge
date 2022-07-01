import os
os.environ['MPLBACKEND'] = 'Qt5Agg'
os.environ['RUNNING_XLWINGS_UDF_SERVER'] = 'True'

from typing import Union, List, Optional
import datetime

import xlwings as xw
import pandas as pd

try:
    from reefledge.reefledge.front_end.excel_addin.UDFs import xw_func_kwargs
    from reefledge.reefledge.front_end.excel_addin.UDFs.worker import Worker
    from reefledge.reefledge.front_end.excel_addin.UDFs.utils.docstrings import *
    from reefledge.reefledge.front_end.excel_addin.gui import launch_gui
except ModuleNotFoundError:
    from reefledge.front_end.excel_addin.UDFs import xw_func_kwargs
    from reefledge.front_end.excel_addin.UDFs.worker import Worker
    from reefledge.front_end.excel_addin.UDFs.utils.docstrings import *
    from reefledge.front_end.excel_addin.gui import launch_gui


@xw.func(**xw_func_kwargs())
@xw.ret(index=True, header=True)
def rl_metrics(caller: xw.Range) -> Union[pd.DataFrame, str]:
    """Exposes the meaning of ReefLedge's metric code names."""
    return Worker('rl_metrics', caller).data

@xw.func(**xw_func_kwargs())
@xw.arg('target')
@xw.arg('reference_date', doc=REFERENCE_DATE_DOCSTRING)
@xw.arg('transpose', doc="Boolean, defaults to 'FALSE'.")
def rl_tickers(
    caller: xw.Range,
    target: str,
    reference_date: Union[str, datetime.datetime, None] = None,
    transpose: bool = False) -> Union[List[List[str]], str]:
    ####################################################################
    """Returns a sorted list of all available tickers."""

    kwargs = {
        'target': target,
        'reference_date': reference_date,
        'transpose': transpose,
    }

    worker = Worker(
        target_function_name='rl_tickers',
        caller=caller,
        target_function_kwargs=kwargs,
        format_destination_range=False
    )

    return worker.data


@xw.func(**xw_func_kwargs())
@xw.arg('target')
@xw.arg('metric')
@xw.arg('ticker')
@xw.arg('reference_date', doc=REFERENCE_DATE_DOCSTRING)
@xw.arg('forecasted_date')
@xw.arg('short_position', doc=SHORT_POSITION_DOCSTRING)
@xw.arg('confidence_level', doc=CONFIDENCE_LEVEL_DOCSTRING)
def rl_data_point(
    caller: xw.Range,
    target: str,
    metric: str,
    ticker: str,
    reference_date: Union[str, datetime.datetime, None],
    forecasted_date: Union[str, datetime.datetime],
    short_position: bool = False,
    confidence_level: Optional[float] = None) -> Union[float, str]:
    ###########################################################################
    """Returns a specific data point (scalar)."""

    kwargs = {
        'target': target,
        'metric': metric,
        'tickers': ticker,
        'reference_date': reference_date,
        'forecasted_date': forecasted_date,
        'short_position': short_position,
        'confidence_level': confidence_level,
    }

    return Worker('rl_data_point', caller, target_function_kwargs=kwargs).data

@xw.func(**xw_func_kwargs())
@xw.arg('target')
@xw.arg('metric')
@xw.arg('tickers', ndim=2, doc='Range/array of strings.')
@xw.arg('reference_date', doc=EXTENDED_REFERENCE_DATE_DOCSTRING)
@xw.arg('forecasted_date', doc=FORECASTED_DATE_DOCSTRING)
@xw.arg('short_position', doc=SHORT_POSITION_DOCSTRING)
@xw.arg('confidence_level', doc=CONFIDENCE_LEVEL_DOCSTRING)
@xw.ret(index=True, header=True)
def rl_data_matrix(
    caller: xw.Range,
    target: str,
    metric: str,
    tickers: List[List[str]],
    reference_date: Union[str, datetime.datetime, None] = None,
    forecasted_date: Union[str, datetime.datetime, None] = None,
    short_position: bool = False,
    confidence_level: Optional[float] = None) -> Union[pd.DataFrame, str]:
    ###########################################################################
    """Returns a data matrix with forecasted dates laid out row-wise."""

    kwargs = {
        'target': target,
        'metric': metric,
        'tickers': tickers,
        'reference_date': reference_date,
        'forecasted_date': forecasted_date,
        'short_position': short_position,
        'confidence_level': confidence_level,
    }

    return Worker('rl_data_matrix', caller, target_function_kwargs=kwargs).data

@xw.func(**xw_func_kwargs())
@xw.arg('target')
@xw.arg('metric')
@xw.arg('reference_date', doc=EXTENDED_REFERENCE_DATE_DOCSTRING)
@xw.arg('forecasted_date', doc=FORECASTED_DATE_DOCSTRING)
@xw.arg('short_position', doc=SHORT_POSITION_DOCSTRING)
@xw.arg('confidence_level', doc=CONFIDENCE_LEVEL_DOCSTRING)
@xw.ret(index=True, header=True)
def rl_bulk_data_matrix(
    caller: xw.Range,
    target: str,
    metric: str,
    reference_date: Union[str, datetime.datetime, None] = None,
    forecasted_date: Union[str, datetime.datetime, None] = None,
    short_position: bool = False,
    confidence_level: Optional[float] = None) -> Union[pd.DataFrame, str]:
    ###########################################################################
    """Calls the 'rl_data_matrix' function for all available tickers."""

    kwargs = {
        'target': target,
        'metric': metric,
        'reference_date': reference_date,
        'forecasted_date': forecasted_date,
        'short_position': short_position,
        'confidence_level': confidence_level,
    }

    worker = Worker(
        target_function_name='rl_bulk_data_matrix',
        caller=caller,
        target_function_kwargs=kwargs
    )

    return worker.data

@xw.func(**xw_func_kwargs())
@xw.arg('picture_name')
@xw.arg('target')
@xw.arg('metric')
@xw.arg('tickers', ndim=2, doc='Range/array of strings.')
@xw.arg('reference_date', doc=EXTENDED_REFERENCE_DATE_DOCSTRING)
@xw.arg('short_position', doc=SHORT_POSITION_DOCSTRING)
@xw.arg('confidence_level', doc=CONFIDENCE_LEVEL_DOCSTRING)
def rl_plot(
    caller: xw.Range,
    picture_name: str,
    target: str,
    metric: str,
    tickers: List[List[str]],
    reference_date: Union[str, datetime.datetime, None] = None,
    short_position: bool = False,
    confidence_level: Optional[float] = None) -> str:
    ###########################################################################
    """Calls the function 'rl_data_matrix' and plots the resulting output."""

    kwargs = {
        'picture_name': picture_name,
        'target': target,
        'metric': metric,
        'tickers': tickers,
        'reference_date': reference_date,
        'short_position': short_position,
        'confidence_level': confidence_level,
    }

    worker = Worker(
        target_function_name='rl_plot',
        caller=caller,
        target_function_kwargs=kwargs,
        format_destination_range=False
    )

    return worker.data


@xw.sub
def rl_login() -> None:
    """Performs user authentication to the ReefLedge API."""
    launch_gui('LoginGUI')

@xw.sub
def rl_animate() -> None:
    """Returns an animation for the given triple \n(target, metric, ticker)."""
    launch_gui('DataAnimationGUI')

@xw.sub
def rl_dump() -> None:
    """Downloads data in bulk and dumps it to a new Excel file."""
    launch_gui('DataDumpGUI')
