# -*- coding: utf-8 -*-

from collections import OrderedDict


GFS_SOLAR_DEFAULT = OrderedDict(
    {
        "dsw_radiance": "ghi",
        "temp_air_0m": "temp_air",
        "u_wind_speed_10m": "wind_speed_u",
        "v_wind_speed_10m": "wind_speed_v",
    }
)

GFS_GRIB = OrderedDict(
    {
        "dsw_radiance": {
            "level": 0,
            "name": "Downward short-wave radiation flux",
            "shortName": "dswrf",
            "typeOfLevel": "surface",
        },
        "temp_air_0m": {
            "level": 0,
            "name": "Temperature",
            "shortName": "t",
            "typeOfLevel": "surface",
        },
        "u_wind_speed_10m": {
            "level": 10,
            "name": "10 metre U wind component",
            "shortName": "10u",
            "typeOfLevel": "heightAboveGround",
        },
        "v_wind_speed_10m": {
            "level": 10,
            "name": "10 metre V wind component",
            "shortName": "10v",
            "typeOfLevel": "heightAboveGround",
        },
    }
)

GFS_GRIB_RENAME = {
    "dswrf": "dsw_radiance",
    "t": "temp_air_0m",
    "10u": "u_wind_speed_10m",
    "10v": "v_wind_speed_10m",
}
