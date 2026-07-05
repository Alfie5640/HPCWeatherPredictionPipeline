import numpy as np
import xarray as xr
from dask import delayed
import dask
from metpy.units import units
from metpy.calc import dewpoint_from_specific_humidity
from metpy.calc import parcel_profile
from metpy.calc import cape_cin

def compute_single_cape_point(ds: xr.Dataset, time: int, lat: int, lon: int) -> float:
    """
    Find CAPE at a single given point
    """
    profile = ds.isel(valid_time=time, latitude=lat, longitude=lon)
    pressure = profile['pressure_level'].values * units.hPa
    temperature = profile['t'].values * units.K
    specific_humidity = profile['q'].values * units("kg/kg")
    dewpoint = dewpoint_from_specific_humidity(pressure, specific_humidity)
    parcelProfile = parcel_profile(pressure, temperature[0], dewpoint[0])
    cape, cin = cape_cin(pressure, temperature, dewpoint, parcelProfile)
    return cape.magnitude

def compute_cape_sequential(ds: xr.Dataset) -> xr.DataArray:
    """Sequential CAPE computation"""
    capeArr = np.full(
        (len(ds['latitude']), len(ds['longitude']), len(ds['valid_time'])),
        np.nan
    )
    for lat in range(0, len(ds['latitude'])):
        for lon in range(0, len(ds['longitude'])):
            for time in range(0, len(ds['valid_time'])):
                try:
                    capeArr[lat, lon, time] = compute_single_cape_point(ds, time, lat, lon)
                except Exception as e:
                    print(f"error at lat={lat}, lon={lon}, time={time}: {e}")
    return xr.DataArray(
        capeArr,
        dims=["latitude", "longitude", "valid_time"],
        coords={
            "latitude": ds["latitude"].values,
            "longitude": ds["longitude"].values,
            "valid_time": ds["valid_time"].values,
        },
        name="cape"
    )

def compute_cape_for_timestep(ds: xr.Dataset, time: int) -> np.ndarray:
    """Compute CAPE for every lat/lon point at a single timestep"""
    n_lat = len(ds['latitude'])
    n_lon = len(ds['longitude'])
    slice_arr = np.full((n_lat, n_lon), np.nan)

    for lat in range(n_lat):
        for lon in range(n_lon):
            try:
                slice_arr[lat, lon] = compute_single_cape_point(ds, time, lat, lon)
            except Exception as e:
                print(f"error at lat={lat}, lon={lon}, time={time}: {e}")

    return slice_arr


def compute_cape_dask_batched(ds: xr.Dataset) -> xr.DataArray:
    """Dask parallelized CAPE computation, batched by timestep"""
    n_time = len(ds['valid_time'])

    promises = [delayed(compute_cape_for_timestep)(ds, t) for t in range(n_time)]
    results = dask.compute(*promises)
    capeArr = np.stack(results, axis=-1)

    return xr.DataArray(
        capeArr,
        dims=["latitude", "longitude", "valid_time"],
        coords={
            "latitude": ds["latitude"].values,
            "longitude": ds["longitude"].values,
            "valid_time": ds["valid_time"].values,
        },
        name="cape"
    )



def compute_shear_features(ds: xr.Dataset) -> xr.Dataset:
    """
    Compute bulk and directional shear for 10m->850hPa and 850hPa->500hPa layers.
    Expects ds to have u10, v10, u, v (with pressure_level dim including 850 and 500).
    Returns a new Dataset containing the shear variables
    """
    u850, v850 = ds['u'].sel(pressure_level=850), ds['v'].sel(pressure_level=850)
    u500, v500 = ds['u'].sel(pressure_level=500), ds['v'].sel(pressure_level=500)

    features = xr.Dataset({
        "bulk_shear_10m_850": wind_shear(ds['u10'], ds['v10'], u850, v850),
        "bulk_shear_850_500": wind_shear(u850, v850, u500, v500),
        "dir_shear_10m_850": directional_shear(ds['u10'], ds['v10'], u850, v850),
        "dir_shear_850_500": directional_shear(u850, v850, u500, v500),
    })
    return features

def wind_shear(u1: xr.DataArray, v1: xr.DataArray, u2: xr.DataArray, v2: xr.DataArray) -> xr.DataArray:
    """
    Bulk wind shear magnitude between two levels
    u1, v1 show wind components at the lower level
    u2, v2 show wind components at the upper level
    find euclidean distance between change vectors
    """
    du = u2 - u1
    dv = v2 - v1
    return np.sqrt(du**2 + dv**2)

def directional_shear(u1: xr.DataArray, v1: xr.DataArray, u2: xr.DataArray, v2: xr.DataArray) -> xr.DataArray:
    """
    Directional wind shear between two level
    """
    dir1 = np.degrees(np.arctan2(v1, u1))
    dir2 = np.degrees(np.arctan2(v2, u2))
    return (dir2 - dir1 + 180) % 360 - 180
