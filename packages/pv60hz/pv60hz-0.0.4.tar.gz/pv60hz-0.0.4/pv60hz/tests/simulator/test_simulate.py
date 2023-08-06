import arrow
from unittest.mock import patch
import datetime
import pytest
import pytz
import numpy as np
import pandas as pd

from pv60hz.simulator.simulate import PVWattsV5


def test_simulate():
    data = pd.read_pickle("pv60hz/tests/simulator/test.pkl")
    lat, lon, alt = 37.123, 126.598, 0
    capacity = 300
    kst = pytz.timezone("Asia/Seoul")
    start_dt = kst.localize(datetime.datetime(2021, 9, 2, 0, 0))
    end_dt = kst.localize(datetime.datetime(2021, 9, 3, 0, 0))
    simulator = PVWattsV5(
        lat,
        lon,
        alt,
        capacity=capacity,
        surface_azimuth=180,
        surface_tilt=25,
        albedo=0.2,
        transposition_model="perez",
        clearsky_model="ineichen",
        aoi_model="physical",
        spectral_model="no_loss",
    )
    r = simulator(data, start_dt, end_dt, kst)
    result = pd.read_pickle("pv60hz/tests/simulator/result.pkl")
    assert np.all(result == r)
