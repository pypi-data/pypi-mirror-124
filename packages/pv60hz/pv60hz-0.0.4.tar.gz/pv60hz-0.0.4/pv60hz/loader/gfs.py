import requests
import numpy as np
import arrow
import math
import datetime
import pytz
import pandas as pd
import numpy as np
import os
import xarray

from bs4 import BeautifulSoup
from tqdm import tqdm
from ..exceptions import (
    DataRootNullException,
    LatLonInvalidException,
    EccodesRuntimeErrorException,
)
from ..common.utils import custom_round, make_dir
from .gfs_variable import GFS_SOLAR_DEFAULT, GFS_GRIB, GFS_GRIB_RENAME


class GFSLoader(object):
    def __init__(self, data_root="/tmp"):
        """__init__

        Parameters
        ----------
        data_root: str
            gfs file save path

        Returns
        -------
        """
        if not data_root:
            raise DataRootNullException

        self.data_root = data_root
        self.GFS_URL = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
        self.col_mapping = list(GFS_SOLAR_DEFAULT.values())
        self.simulation_time = None
    
    def validate(self, start_dt:datetime.datetime, end_dt: datetime.datetime):
        diff = arrow.get(end_dt) - arrow.get(start_dt)
        if diff.total_seconds() < 0:
            err_msg = "end date must be later than start date."
            raise Exception(err_msg)
        arrow_end_dt = arrow.get(arrow.get(end_dt).astimezone(pytz.timezone('UTC')))
        arrow_now_dt = arrow.get(arrow.now().astimezone(pytz.timezone('UTC')))
        diff = arrow_end_dt - arrow_now_dt
        if diff.total_seconds() / 3600 / 24 >= 4:
            err_msg = "The forecast end datetime is currently within 4 days."
            raise Exception(err_msg)
    def get_html_page(self, url: str) -> str:
        """Get html page

        Parameters
        ----------
        url: str

        Returns
        -------
        str
            html data
        """
        return requests.get(url).text

    def refresh_simulation_time(self) -> list:
        """Refresh GFS simulation time

        Parameters
        ----------

        Returns
        -------
        list
            simulation times
        """
        print("Refresh Available Simulation Time")
        print("=================================")
        html = self.get_html_page(self.GFS_URL)
        soup = BeautifulSoup(html, features="html.parser")
        dts = [a.text for a in soup.findAll("a")]

        self.simulation_time = []
        for dt in tqdm(dts):
            url = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2F{dt}"
            html = self.get_html_page(url)
            soup = BeautifulSoup(html, features="html.parser")
            hours = [a.text for a in soup.findAll("a")]
            for h in hours:
                self.simulation_time.append(
                    datetime.datetime.strptime(
                        f"{dt.split('.')[-1]}{h}", "%Y%m%d%H"
                    ).replace(tzinfo=pytz.timezone("UTC"))
                )
        return self.simulation_time

    def latest_simulation(
        self,
        fct_start_dt: datetime.datetime,
        fct_end_dt: datetime.datetime,
        refresh=False,
        verbose=False,
    ) -> datetime.datetime:
        """Get latest GFS simulation time from forecast start datetime

        Parameters
        ----------
        fct_start_dt: datetime.datetime
            forecast start datetime
        fct_end_dt: datetime.datetime
            forecast end datetime
        refresh: bool
            Force refresh latest simulation time
        verbose: bool
            verbose
        Returns
        -------
        datetime.datetime
            latest simulation times from forecast start datetime
        """
        if refresh or self.simulation_time is None:
            self.refresh_simulation_time()

        st = (fct_start_dt - datetime.timedelta(hours=4)).astimezone(
            pytz.timezone("UTC")
        )
        dt_diff = [(st - dt).total_seconds() for dt in self.simulation_time]
        if verbose:
            print(st)
            for idx, val in enumerate(self.simulation_time):
                print(val, dt_diff[idx])
        argwhere = np.argwhere(np.array(dt_diff) > 0)
        
        if not list(argwhere):
            sdt = self.simulation_time[-1].strftime('%Y-%m-%d %H:%M:%S %Z')
            edt = self.simulation_time[0].strftime('%Y-%m-%d %H:%M:%S %Z')
            err_msg = f"GFS available data is from {sdt} to {edt}"
            raise Exception(err_msg)
        idx = argwhere[0][0]
        return self.simulation_time[idx]

    def download_data(self, url, filename):
        """download data

        Parameters
        ----------
        url: str
            url
        filename: str
            filename

        Returns
        -------
        
        """
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(
                "Something went wrong with the data download."
            ) from e
        os.umask(0)
        with open(os.open(filename, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as f:
            f.write(r.content)

    def collect_data(self, start_dt: datetime.datetime, end_dt: datetime.datetime):
        """Collect GFS data from forecast start datetime to forecast end datetime

        Parameters
        ----------
        start_dt: datetime.datetime
            forecast start datetime
        end_dt: datetime.datetime
            forecast end datetime
        Returns
        -------
        
        """
        self.validate(start_dt, end_dt)
        latest_simul_dt = self.latest_simulation(start_dt, end_dt)
        print(f"Latest GFS Simulation Datetime: {latest_simul_dt}")
        to_diff = end_dt.astimezone(pytz.timezone("UTC")) - latest_simul_dt
        from_diff = start_dt.astimezone(pytz.timezone("UTC")) - latest_simul_dt
        to_diff_hour = divmod(to_diff.total_seconds(), 3600)[0]
        from_diff_hour = divmod(from_diff.total_seconds(), 3600)[0]
        print("Download Global Forecast System Data")
        print("====================================")
        l = [
            i
            for i in range(int(to_diff_hour + 3))
            if i != 0 and i % 3 == 0 and i >= (from_diff_hour - 3)
        ]
        for hour in tqdm(l):
            simul_date = latest_simul_dt.strftime("%Y%m%d")
            simul_hour = latest_simul_dt.strftime("%H")
            url = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?file=gfs.t{simul_hour}z.pgrb2full.0p50.f{hour:03d}&lev_10_m_above_ground=on&lev_surface=on&var_DSWRF=on&var_TMP=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.{simul_date}%2F{simul_hour}%2Fatmos"
            filename = (latest_simul_dt + datetime.timedelta(hours=hour)).strftime(
                "%Y%m%d%H"
            )
            self.download_data(url, os.path.join(self.data_root, f"{filename}.grb"))

    @staticmethod
    def latlon2grid(latitude, longitude, top=1, bottom=1, left=1, right=1) -> tuple:
        """Get GFS grid index by latitude, longitude

        Parameters
        ----------
        latitude : float
        longitude : float
        top : int
        bottom : int
        left : int
        right : int

        Returns
        -------
        tuple
            GFS data index

        """
        if not -90 <= latitude <= 90:
            raise LatLonInvalidException
        if not -180 <= longitude <= 180:
            raise LatLonInvalidException
        # convert to 0-360 scale
        if longitude < 0:
            longitude += 360
        lat_degree = 0.5
        lon_degree = 0.5
        N_lat = int(180 / lat_degree + 1)
        N_lon = int(360 / lon_degree)
        lat_idx = (90 - latitude) / lat_degree
        lon_idx = longitude / lon_degree
        lat_target_idx = custom_round(lat_idx)
        lon_target_idx = custom_round(lon_idx)
        lat_idxs = math.floor(lat_idx), math.ceil(lat_idx)
        lon_idxs = math.floor(lon_idx), math.ceil(lon_idx)
        if top == 0 or bottom == 0:
            lat_idxs = [lat_target_idx]
        else:
            lat_idxs = list(range(lat_idxs[0] - top + 1, lat_idxs[1] + bottom))
        if left == 0 or right == 0:
            lon_idxs = [lon_target_idx]
        else:
            lon_idxs = list(range(lon_idxs[0] - left + 1, lon_idxs[1] + right))
        lat_idxs = [i for i in lat_idxs if 0 <= i < N_lat]
        lon_idxs = [i if i < N_lon else i - N_lon for i in lon_idxs]
        return lat_idxs, lon_idxs

    @staticmethod
    def smooth(array, lat_idxs, lon_idxs):
        """smooth

        Parameters
        ----------

        array : numpy.array
            gfs data
        lat_idxs : list
            gfs latitude index
        lon_idxs : list
            gfs longitude index

        Returns
        -------
        numpy.array

        """

        sub_array = array[:, lat_idxs, :, :][:, :, lon_idxs, :]
        smooth_array = np.nanmean(sub_array, axis=(1, 2))

        return smooth_array

    def _process_latlon(self, array, lat, lon, top=1, bottom=1, left=1, right=1):
        """_process_latlons

        Parameters
        ----------

        array : numpy.array
            gfs data
        shape : tuple
            numpy shape
        lat: float
            latitude
        lon: float
            longitude
        top : int
            how much read top index 
        bottom : int
            how much read bottom index 
        left : int
            how much read left index 
        right : int
            how much read right index 

        Returns
        -------
        numpy.array
        """
        lat_idxs, lon_idxs = self.latlon2grid(
            lat, lon, top=top, bottom=bottom, left=left, right=right
        )
        smooth_array = self.smooth(array, lat_idxs, lon_idxs)

        return smooth_array

    def _load_dataset(self, file_name, key):
        """Load Grib file

        Parameters
        ----------

        file_name : str
            file name
        key : dict
            grib key

        Returns
        -------
        pandas.DataFrame
        """
        try:
            dataset = xarray.load_dataset(
                file_name,
                engine="cfgrib",
                backend_kwargs={
                    "filter_by_keys": key,
                    "indexpath": "",
                    "read_keys": [],
                },
            )
        except RuntimeError:
            raise EccodesRuntimeErrorException
        return dataset.to_dataframe()

    def read_gfs(self, fct_start_dt, fct_end_dt):
        """read_gfs

        Parameters
        ----------
        fct_start_dt : datetime.datetime
            forecast start datetime
        fct_end_dt : datetime.datetime
            forecast end datetime
        
        Returns
        -------
        tuple
            tuple of pandas.DatetimeIndex and numpy array
        """
        print("Read Global Forecast System Grib file")
        print("====================================")
        st = arrow.get(fct_start_dt.astimezone(pytz.timezone("UTC")))
        et = arrow.get(fct_end_dt.astimezone(pytz.timezone("UTC")))

        diff_hour = divmod((et - st).total_seconds(), 3600)[0]

        datetimes = [st.shift(hours=i) for i in range(int(diff_hour))]
        datetimes = [i for i in datetimes if (i.hour) % 3 == 0]

        if datetimes:
            datetimes = (
                [datetimes[0].shift(hours=-3)]
                + datetimes
                + [datetimes[-1].shift(hours=3)]
            )

        array_sequence = np.zeros((len(datetimes), 361, 720, 4))

        for idx, datetime in enumerate(tqdm(datetimes)):
            file_name = os.path.join(
                self.data_root, f"{datetime.format('YYYYMMDDHH')}.grb"
            )
            df = None
            for grib_idx, (key, value) in enumerate(GFS_GRIB.items()):
                dataset_df = self._load_dataset(file_name, value)
                prev_col = dataset_df.columns[-1]
                new_col = GFS_GRIB_RENAME[value["shortName"]]
                dataset_df = dataset_df[[prev_col]]
                dataset_df.columns = [new_col]
                if grib_idx == 0:
                    df = dataset_df.copy()
                    continue
                df = df.join(dataset_df[[new_col]], how="left")

            columns = list(GFS_GRIB.keys())
            array_sequence[idx] = df[columns].to_numpy().reshape(361, 720, 4)

        dt_index = pd.DatetimeIndex(list(map(lambda i: i.naive, datetimes)), tz="UTC")

        return dt_index, array_sequence

    def __call__(
        self, lat, lon, fct_start_dt, fct_end_dt, top=1, bottom=1, left=1, right=1
    ):
        """__call__

        Parameters
        ----------
        lat : float
            latitude
        lon : float
            longitude
        fct_start_dt: datetime.datetime
            forecast start datetime
        fct_end_dt: datetime.datetime
            forecast end datetime
        top : int
            how much read top index 
        bottom : int
            how much read bottom index 
        left : int
            how much read left index 
        right : int
            how much read right index 
            
        Returns
        -------
        pandas.DataFrame
            GFS Raw data
        """
    
        dt_index, array = self.read_gfs(fct_start_dt, fct_end_dt)
        data_array = self._process_latlon(array, lat, lon)
        weather_data = pd.DataFrame(data_array.reshape(-1, 4), index=dt_index)
        weather_data.columns = self.col_mapping
        weather_data.index.name = "dt"
        return weather_data


if __name__ == "__main__":

    # ins.refresh_simulation_time()
    kst = pytz.timezone("Asia/Seoul")
    start_dt = kst.localize(datetime.datetime(2021, 10, 10, 0, 0))
    end_dt = kst.localize(datetime.datetime(2021, 10, 15, 0, 0))
    lat, lon = 37.123, 126.598
    # ins.latest_simulation(start_dt, end_dt, verbose=True)
    loader = GFSLoader()
    loader.collect_data(start_dt, end_dt)
    print(loader(lat, lon, start_dt, end_dt))
