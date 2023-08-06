# pv60hz

[![CircleCI](https://circleci.com/gh/60hz-io/pv60hz/tree/main.svg?style=svg)](https://circleci.com/gh/60hz-io/pv60hz/tree/main)
[![codecov](https://codecov.io/gh/60hz-io/pv60hz/branch/main/graph/badge.svg?token=D2N9RKHCK3)](https://codecov.io/gh/60hz-io/pv60hz)
[![Documentation Status](https://readthedocs.org/projects/pv60hz/badge/?version=latest)](https://pv60hz.readthedocs.io/en/latest/?badge=latest)
[![Python: 3.6](https://img.shields.io/badge/Python-3.6-blue)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-lightgrey)](https://github.com/60hz-io/pv60hz/blob/main/LICENSE)


<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/29847262/132467329-20c7b1a7-0f90-47bc-85f2-e629ac752fec.png" />
</p>


The pv60hz library is an solar forecast simulation powered by the 60hz company. This library provides easy download to the [Global Forecast System](https://www.nco.ncep.noaa.gov/pmb/products/gfs/), a numerical forecasting model provided by the National Oceanic and Atmospheric Administration, and preprocessing steps required for solar power generation estimation. This library uses the open source [pvlib-python](https://github.com/pvlib/pvlib-python) to simulate the predicted solar power generation.

## Intro
As interest in climate change and environmental issues is growing around the world, renewable energy power plants are continuously increasing.

However, as renewable energy increases, it becomes increasingly difficult to operate the power grid.
Renewable energy power plants are an intermittent resource whose power generation varies depending on the weather, making it difficult to balance the supply and demand for electricity.
In addition, relatively small power plants are characterized by decentralization, making them difficult to manage with traditional methods.

Therefore, if you can accurately predict the amount of renewable energy generation across the country, you can balance supply and demand by adjusting the utilization rate of flexible resources such as fossil fuels.
In addition, this generation forecasting technology can be used for grid operation, monitoring and maintenance of solar and wind power plants.


## Getting started
This library recommends a virtual environment using [conda](https://docs.conda.io/en/latest/).
```
$ conda create -y -n venv python==3.6.10
$ conda activate venv
```

And install the [cfgrib](https://github.com/ecmwf/cfgrib) library.
```
conda install -c conda-forge cfgrib
```

## Installation
```
$ pip install pv60hz
```


## QuickStart
```
>>> from pv60hz.preprocessor.preprocess import GFSPreprocessor
>>> from pv60hz.loader.gfs import GFSLoader
>>> from pv60hz.simulator.simulate import PVWattsV5
>>> import pytz
>>> import datetime
>>>
>>> kst = pytz.timezone("Asia/Seoul")
>>> start_dt = kst.localize(datetime.datetime(2021, 9, 2, 0, 0)) # Change datetime to recent datetime
>>> end_dt = kst.localize(datetime.datetime(2021, 9, 3, 0, 0)) # Change datetime to recent datetime
>>> lat, lon, alt = 37.123, 126.598, 0
>>> capacity = 300  # kw
>>> azimuth = 180
>>> tilt = 25
>>>
>>>
>>> loader = GFSLoader()
>>> loader.collect_data(start_dt, end_dt)
Latest GFS Simulation Datetime: 2021-09-01 06:00:00+00:00
Download Global Forecast System Data
====================================
100%|█████████████████████████████████████████████████████████████████████████| 10/10 [00:18<00:00
>>>
>>>
>>> data = loader(lat, lon, start_dt, end_dt)
Read Global Forecast System Grib file
====================================
100%|█████████████████████████████████████████████████████████████████████████| 10/10 [00:18<00:00
>>>
>>> preproc_model = GFSPreprocessor(decomp_model="disc", clearsky_interpolate=True)
>>> weather_preproc = preproc_model(lat, lon, altitude=alt, weather=data, keep_solar_geometry=False)
>>>

>>> simulator = PVWattsV5(lat, lon, alt, capacity=capacity, surface_azimuth=azimuth, surface_tilt=tilt)
>>> simulator(weather_preproc, start_dt, end_dt, kst)
                           predict_yield
dt                                      
2021-09-02 00:00:00+09:00       0.000000
2021-09-02 01:00:00+09:00       0.000000
2021-09-02 02:00:00+09:00       0.000000
2021-09-02 03:00:00+09:00       0.000000
2021-09-02 04:00:00+09:00       0.000000
2021-09-02 05:00:00+09:00       0.000000
2021-09-02 06:00:00+09:00       0.000000
2021-09-02 07:00:00+09:00       0.000000
2021-09-02 08:00:00+09:00       0.837611
2021-09-02 09:00:00+09:00       4.288974
2021-09-02 10:00:00+09:00      17.897454
2021-09-02 11:00:00+09:00      43.032267
2021-09-02 12:00:00+09:00      72.636298
2021-09-02 13:00:00+09:00      97.711072
2021-09-02 14:00:00+09:00     112.442749
2021-09-02 15:00:00+09:00     117.264219
2021-09-02 16:00:00+09:00     114.608081
2021-09-02 17:00:00+09:00      94.638939
2021-09-02 18:00:00+09:00      49.883874
2021-09-02 19:00:00+09:00      11.370596
2021-09-02 20:00:00+09:00       0.000000
2021-09-02 21:00:00+09:00       0.000000
2021-09-02 22:00:00+09:00       0.000000
2021-09-02 23:00:00+09:00       0.000000
2021-09-03 00:00:00+09:00       0.000000
```

## Documentation
Full documentation can be found at [here](https://pv60hz.readthedocs.io/en/latest/)


## Related to
* [Global Forecast System](https://www.nco.ncep.noaa.gov/pmb/products/gfs/)
* [pvlib-python](https://github.com/pvlib/pvlib-python)

## License
BSD-3-Clause

## Citing
William F. Holmgren, Clifford W. Hansen, and Mark A. Mikofski.
"pvlib python: a python package for modeling solar energy systems."
Journal of Open Source Software, 3(29), 884, (2018). https://doi.org/10.21105/joss.00884
