import arrow
from unittest.mock import patch
import datetime
import pytest
import pytz
import numpy as np
import pandas as pd

from pv60hz.loader.gfs import GFSLoader
from pv60hz.exceptions import LatLonInvalidException

simul_date_data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head><title>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</title></head><body bgcolor="#ffffff"><h2 align=center>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</h2><h2 align=center>g2sub V1.1</h2><p>g2subset (grib2 subset)  allows you to subset (time, field, level, or region) a GRIB2 file and
sends you the result<br>&nbsp;<br><br><font color=red>Subdirectory</font><p><table border=0><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210831">gfs.20210831</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830">gfs.20210830</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210829">gfs.20210829</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210828">gfs.20210828</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210827">gfs.20210827</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210826">gfs.20210826</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210825">gfs.20210825</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210824">gfs.20210824</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210823">gfs.20210823</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210822">gfs.20210822</a></tr></table></form><br><font color=red>Select subdirectory from above list.</font><small> <p align=left><p align=left><small>g2sub 1.1.0.beta-6 and comments: Wesley.Ebisuzaki@noaa.gov, Jun.Wang@noaa.gov<br></small></body></html>
"""

simul_datetime_data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head><title>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</title></head><body bgcolor="#ffffff"><h2 align=center>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</h2><h2 align=center>g2sub V1.1</h2><p>g2subset (grib2 subset)  allows you to subset (time, field, level, or region) a GRIB2 file and
sends you the result<br>&nbsp;<br><font color=red>Directory:&nbsp&nbsp&nbsp;</font>/gfs.20210830<br><br><font color=red>Subdirectory</font><p><table border=0><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F18">18</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F12">12</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F06">06</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F00">00</a></tr></table></form><br><font color=red>Select subdirectory from above list.</font><small> <p align=left><p align=left><small>g2sub 1.1.0.beta-6 and comments: Wesley.Ebisuzaki@noaa.gov, Jun.Wang@noaa.gov<br></small></body></html>
"""

simulate = [
    "2021083118",
    "2021083112",
    "2021083106",
    "2021083100",
    "2021083018",
    "2021083012",
    "2021083006",
    "2021083000",
    "2021082918",
    "2021082912",
    "2021082906",
    "2021082900",
    "2021082818",
    "2021082812",
    "2021082806",
    "2021082800",
    "2021082718",
    "2021082712",
    "2021082706",
    "2021082700",
    "2021082618",
    "2021082612",
    "2021082606",
    "2021082600",
    "2021082518",
    "2021082512",
    "2021082506",
    "2021082500",
    "2021082418",
    "2021082412",
    "2021082406",
    "2021082400",
    "2021082318",
    "2021082312",
    "2021082306",
    "2021082300",
    "2021082218",
    "2021082212",
    "2021082206",
    "2021082200",
]


def mock_get_html_page(*args, **kwargs):
    if "dir=" not in args[0]:
        return simul_date_data
    else:
        return simul_datetime_data


@patch("pv60hz.loader.gfs.GFSLoader.get_html_page")
def test_collect_simulate(mock_func):
    ins = GFSLoader()
    mock_func.side_effect = mock_get_html_page
    r = ins.refresh_simulation_time()
    assert len(r) == len(simulate)
    for i in range(len(simulate)):
        s = datetime.datetime.strptime(simulate[i], "%Y%m%d%H").replace(
            tzinfo=pytz.timezone("UTC")
        )
        assert s == r[i]


def test_latlon2grid():
    ins = GFSLoader()
    r = ins.latlon2grid(37.123, 126.598)
    assert r == ([105, 106], [253, 254])


def test_latlon2grid_invalid():
    ins = GFSLoader()
    with pytest.raises(LatLonInvalidException) as e_info:
        ins.latlon2grid(-999, -999)


def test_latest_simulation():
    ins = GFSLoader()
    ins.simulation_time = []
    sdt = datetime.datetime(2021, 7, 20, 18, 0, 0).replace(tzinfo=pytz.timezone("UTC"))
    for i in range(10):
        ins.simulation_time.append(sdt - datetime.timedelta(hours=6))
    fct_start_dt = datetime.datetime(2021, 7, 22, 18, 0, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    fct_end_dt = datetime.datetime(2021, 7, 24, 18, 0, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    assert ins.latest_simulation(fct_start_dt, fct_end_dt) == datetime.datetime(
        2021, 7, 20, 12, 0
    ).replace(tzinfo=pytz.timezone("UTC"))


@patch("pv60hz.loader.gfs.GFSLoader.latest_simulation")
@patch("pv60hz.loader.gfs.GFSLoader.download_data")
def test_collect_data(mock_download_data, mock_latest_simulation):
    ins = GFSLoader()
    mock_download_data.return_value = True
    mock_latest_simulation.return_value = datetime.datetime(2021, 7, 20, 12, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    fct_start_dt = datetime.datetime(2021, 7, 22, 18, 0, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    fct_end_dt = datetime.datetime(2021, 7, 24, 18, 0, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    ins.collect_data(fct_start_dt, fct_end_dt)


def test_smooth():
    ins = GFSLoader
    a = np.arange(72)
    a = np.reshape(a, (4, 3, 2, 3))

    r = np.array(
        (
            [
                [9.0, 10.0, 11.0],
                [27.0, 28.0, 29.0],
                [45.0, 46.0, 47.0],
                [63.0, 64.0, 65.0],
            ]
        )
    )
    assert np.all(r == ins.smooth(a, [1], [1]))


@patch("pv60hz.loader.gfs.GFSLoader.smooth")
@patch("pv60hz.loader.gfs.GFSLoader.latlon2grid")
def test_processs_latlon(mock1, mock2):
    ins = GFSLoader()
    mock1.return_value = [1], [1]
    r = np.array(
        (
            [
                [9.0, 10.0, 11.0],
                [27.0, 28.0, 29.0],
                [45.0, 46.0, 47.0],
                [63.0, 64.0, 65.0],
            ]
        )
    )
    mock2.return_value = r

    a = np.arange(72)
    a = np.reshape(a, (4, 3, 2, 3))

    assert np.all(r == ins._process_latlon(a, 1, 1))


def mock_load_dataset(*args, **kwargs):
    if args[1]["shortName"] == "dswrf":
        return pd.read_pickle("pv60hz/tests/loader/tmp_dswrf.pkl")
    elif args[1]["shortName"] == "t":
        return pd.read_pickle("pv60hz/tests/loader/tmp_temp.pkl")
    elif args[1]["shortName"] == "10u":
        return pd.read_pickle("pv60hz/tests/loader/tmp_uwind.pkl")
    elif args[1]["shortName"] == "10v":
        return pd.read_pickle("pv60hz/tests/loader/tmp_vwind.pkl")
    return None


@patch("pv60hz.loader.gfs.GFSLoader._load_dataset")
def test_read_gfs(mock1):
    ins = GFSLoader()
    mock1.side_effect = mock_load_dataset
    fct_start_dt = datetime.datetime(2021, 7, 22, 18, 0, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    fct_end_dt = datetime.datetime(2021, 7, 22, 23, 0, 0).replace(
        tzinfo=pytz.timezone("UTC")
    )
    dt_index, array = ins.read_gfs(fct_start_dt, fct_end_dt)

    assert np.all(
        pd.DatetimeIndex(
            [
                datetime.datetime(2021, 7, 22, 15, 0).replace(
                    tzinfo=pytz.timezone("UTC")
                ),
                datetime.datetime(2021, 7, 22, 18, 0).replace(
                    tzinfo=pytz.timezone("UTC")
                ),
                datetime.datetime(2021, 7, 22, 21, 0).replace(
                    tzinfo=pytz.timezone("UTC")
                ),
                datetime.datetime(2021, 7, 23, 00, 0).replace(
                    tzinfo=pytz.timezone("UTC")
                ),
            ]
        )
        == dt_index
    )

