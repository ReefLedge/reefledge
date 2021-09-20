import os
os.environ['MPLBACKEND'] = 'Qt5Agg'

from typing import Union, Optional, List
import datetime

import xlwings as xw
import pandas as pd

from reefledge.front_end.excel_addin.utils.docstrings import *
from reefledge.front_end.excel_addin.core import worker, rl_plot as _rl_plot
from reefledge.front_end.excel_addin.gui import launch_gui


@xw.func(async_mode='threading')
@xw.ret(index=True, header=True)
def rl_metrics(caller: xw.Range) -> Union[pd.DataFrame, str]:
    """Exposes the meaning of ReefLedge's metric code names."""
    return worker(caller, function_name='rl_metrics')

@xw.func(async_mode='threading')
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
    ####################################################################
    """Returns a specific data point (scalar)."""

    args = [
        target,
        metric,
        ticker,
        reference_date,
        forecasted_date,
        short_position,
        confidence_level,
    ]

    return worker(caller, function_name='rl_data_point', args=args)

@xw.func(async_mode='threading')
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

    args = [
        target,
        metric,
        tickers,
        reference_date,
        forecasted_date,
        short_position,
        confidence_level
    ]

    return worker(caller, function_name='rl_data_matrix', args=args)

@xw.func(async_mode='threading')
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

    args = [
        target,
        metric,
        reference_date,
        forecasted_date,
        short_position,
        confidence_level
    ]

    return worker(caller, function_name='rl_bulk_data_matrix', args=args)

@xw.func(async_mode='threading')
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
    forecasted_date = None

    args = [
        target,
        metric,
        tickers,
        reference_date,
        forecasted_date,
        short_position,
        confidence_level
    ]

    return _rl_plot(caller, picture_name, args)


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
