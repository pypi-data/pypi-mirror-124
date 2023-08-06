# -*- coding: utf-8 -*-

import math
import arrow
import os
from datetime import datetime

import pandas as pd


def build_kwargs(params, **kwargs):
    """build_kwargs
    update params dictionary by iterating over kwargs.items()

    Parameters
    ----------

    params : dict
    **kwargs : dict

    Returns
    -------
    dict
    """

    for k, v in kwargs.items():
        if k in params:
            params[k] = v

    return params


def watts_to_energy(watts, unit="kwh"):
    """watts_to_energy

    Parameters
    ----------

    watts : pd.Series
    unit : str

    Returns
    -------
    """

    conv_dict = {
        "w": lambda x: x,
        "kwh": lambda x: x.rolling("1h", closed="both").mean() / 1000.0,
        "mj": lambda x: x * 3600.0 / 10 ** 6,
    }

    unit = unit.lower()
    formula = conv_dict.get(unit)

    if formula is None:
        raise ValueError(
            "pass one of {} as unit parameter".format(list(conv_dict.keys()))
        )

    energy = formula(watts)

    return energy


def custom_round(x):
    """custom_round
    see below for more details
    - https://stackoverflow.com/questions/10825926/python-3-x-rounding-behavior

    Parameters
    ----------

    x : float

    Returns
    -------
    """

    f = math.floor(x)
    val = x if x - f < 0.5 else f + 1

    return int(val)


def make_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

