import numpy as np
import xarray as xr

def compute_shear_features(ds: xr.Dataset) -> xr.Dataset:
    """
    Compute bulk and directional shear for 10m->850hPa and 850hPa->500hPa layers.
    Expects ds to have u10, v10, u, v (with pressure_level dim including 850 and 500).
    Returns a new Dataset containing just the derived shear variables.
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
    Bulk wind shear magnitude between two levels.
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
