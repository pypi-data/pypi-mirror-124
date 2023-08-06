import arrow
from unittest.mock import patch
import datetime
import pytest
import pytz
import numpy as np
import pandas as pd
import pvlib

from pv60hz.preprocessor.preprocess import GFSPreprocessor, BasePreprocessor


def test_uv_to_speed():
    ins = BasePreprocessor()
    u = pd.Series([1])
    v = pd.Series([2])
    assert 2.23606797749979 == ins.uv_to_speed(u, v)[0]


def test_kelvin_to_celsius():
    ins = BasePreprocessor()
    temp = pd.Series([273.15])

    assert 0 == int(ins.kelvin_to_celsius(temp)[0])


def test_get_clearsky_index():
    ins = BasePreprocessor()
    ghi = pd.Series([1])
    cs_ghi = pd.Series([1])
    assert 1 == round(ins.get_clearsky_index(ghi, cs_ghi)[0], 2)


def test_decompose():
    ins = BasePreprocessor()
    ghi = pd.Series([1])
    solar_zenith = pd.Series([1])

    r = ins.decompose(ghi, solar_zenith, ins._decomp_model)
    assert 1 == int(r.ghi[0])
    assert 0 == int(r.dni[0])
    assert 1 == int(r.dhi[0])


def test_preprocess():
    data = pd.read_pickle("pv60hz/tests/preprocessor/test.pkl")
    preproc_model = GFSPreprocessor(decomp_model="disc", clearsky_interpolate=True)
    lat, lon = 37.123, 126.598
    weather_preproc = preproc_model(
        lat,
        lon,
        altitude=0,
        weather=data,
        keep_solar_geometry=False,
        unstable_to_nan=True,
    )
    result = pd.read_pickle("pv60hz/tests/preprocessor/result.pkl")
    assert np.all(result == weather_preproc)

