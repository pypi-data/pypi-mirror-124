# -*- coding: utf-8 -*-

import numpy as np


from pvlib.pvsystem import PVSystem
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

from ..common.utils import build_kwargs, watts_to_energy


DEFAULT_MODULE_PARAMS = {
    "pdc0": 260,
    "gamma_pdc": -0.004,
}


DEFAULT_INVERTER_PARAMS = {
    "pdc0": 260,
    "eta_inv_nom": 0.96,
    "eta_inv_ref": 0.9637,
}


DEFAULT_LOSSES = {
    "soiling": 2,
    "shading": 3,
    "snow": 0,
    "mismatch": 2,
    "wiring": 2,
    "connections": 0.5,
    "lid": 1.5,
    "nameplate_rating": 1,
    "age": 0,
    "availability": 3,
}


class PVWattsV5(object):

    # self.ac = self.system.pvwatts_ac(self.dc).fillna(0)
    # prevent replaceing nans with 0
    # corresponding to the times weather data's are missing
    def __init__(
        self,
        latitude,
        longitude,
        altitude=0,
        tz="Asia/Seoul",
        surface_azimuth=180,
        surface_tilt=25,
        albedo=0.2,
        capacity=3,  # kw
        temperature_model="open_rack_glass_glass",
        transposition_model="perez",
        clearsky_model="ineichen",
        aoi_model="physical",
        spectral_model="no_loss",
        losses_model="pvwatts",
        **kwargs
    ):
        """__init__

        Parameters
        ----------

        latitude : float
        longitude : float
        altitude : float
        tz : str
        surface_azimuth : float
            - 0-360 degree
            - (north, east, south, west) order
        surface_tilt : float
            - 0-90 degree
            - 0 for horizontal 90 for vertical
        albedo : float
            - [0-1]
        capacity : flaot
            - unit: kW
            - capacity of pv plant
        temperature_model : str
        transposition_model : str
        clearsky_model : str
        aoi_model : str
        spectral_model : str
        losses_model : str
        **kwargs :

        Returns
        -------
        """

        kwargs["pdc0"] = capacity * 1000

        temp_params = TEMPERATURE_MODEL_PARAMETERS["sapm"][temperature_model]
        module_params = build_kwargs(DEFAULT_MODULE_PARAMS, **kwargs)
        inverter_params = build_kwargs(DEFAULT_INVERTER_PARAMS, **kwargs)
        loss_params = build_kwargs(DEFAULT_LOSSES, **kwargs)

        self._system = PVSystem(
            surface_azimuth=surface_azimuth,
            surface_tilt=surface_tilt,
            albedo=albedo,
            temperature_model_parameters=temp_params,
            module_parameters=module_params,
            inverter_parameters=inverter_params,
            losses_parameters=loss_params,
        )

        self._location = Location(
            latitude=latitude, longitude=longitude, tz=tz, altitude=altitude
        )

        # passing clearsky_model argument does not make any difference
        # if weather data contains all of the ghi, dni, dhi columns
        self._mc = ModelChain(
            system=self._system,
            location=self._location,
            transposition_model=transposition_model,
            clearsky_model=clearsky_model,
            aoi_model=aoi_model,
            spectral_model=spectral_model,
            losses_model=losses_model,
        )
        self.energy = None

    def __call__(self, weather, start_dt, end_dt, tz, unit="kwh"):
        """__init__

        Parameters
        ----------

        weather : pandas.DataFrame
        start_dt : datetime.datetime
        end_dt : datetime.datetime
        tz : str
        unit : str
            
        Returns
        -------
        pandas.DataFrame
            Solar power prediction power generation simulation result
        """
        self._mc.run_model(weather)
        ac_power = self._mc.ac
        ac_power.loc[weather.ghi.isnull()] = np.nan

        # TODO: set losses_model as 'no_loss'
        # generate dc/ac power assuming no loss model and
        # post-process the output with specified DEFAULT_LOSSES
        self.energy = watts_to_energy(ac_power)
        self.energy.loc[ac_power.isnull()] = np.nan
        self.energy.name = "predict_yield"
        self.energy = self.energy.to_frame()

        self.energy = self.energy[
            (self.energy.index >= start_dt) & (self.energy.index <= end_dt)
        ]
        self.energy = self.energy.tz_convert(tz)
        return self.energy


# if __name__ == "__main__":

#     from ..preprocessor.preprocess import GFSPreprocessor
#     import pandas as pd
#     from ..loader.gfs import GFSLoader
#     import pytz
#     import datetime

#     kst = pytz.timezone("Asia/Seoul")
#     start_dt = kst.localize(datetime.datetime(2021, 9, 2, 0, 0))
#     end_dt = kst.localize(datetime.datetime(2021, 9, 3, 0, 0))
#     lat, lon, alt = 37.123, 126.598, 0
#     # ins.latest_simulation(start_dt, end_dt, verbose=True)
#     loader = GFSLoader()
#     # loader.collect_data(start_dt, end_dt)
#     data = loader(lat, lon, start_dt, end_dt)

#     preproc_model = GFSPreprocessor(decomp_model="disc", clearsky_interpolate=True)
#     weather_preproc = preproc_model(
#         lat,
#         lon,
#         altitude=0,
#         weather=data,
#         keep_solar_geometry=False,
#         unstable_to_nan=True,
#     )
#     print(weather_preproc)
#     simulator = PVWattsV5(
#         lat,
#         lon,
#         alt,
#         capacity=300,
#         surface_azimuth=180,
#         surface_tilt=25,
#         albedo=0.2,
#         transposition_model="perez",
#         # transposition_model='haydavies',
#         clearsky_model="ineichen",
#         aoi_model="physical",
#         spectral_model="no_loss",
#         # losses_model='no_loss',
#         # eta_inv_nom=1, # kwarg test
#         # gamma_pdc=-0.03
#     )
#     r = simulator(weather_preproc, start_dt, end_dt, kst)
#     print(r)

