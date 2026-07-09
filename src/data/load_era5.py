# src/data/load_era5.py
import xarray as xr
import glob
import os

def load_era5(path: str) -> xr.Dataset:
    if os.path.isdir(path):
        files = glob.glob(f"{path}/*.nc")
        ds = xr.open_mfdataset(files, combine="by_coords")
    else:
        ds = xr.open_dataset(path)
    return ds

def convert_longitude(ds: xr.Dataset) -> xr.Dataset:
    """Convert longitude from 0-360 to -180/180 convention and sort"""
    ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180))
    ds = ds.sortby("longitude")
    return ds

def subset_area(ds: xr.Dataset, north: float, south: float, west: float, east: float) -> xr.Dataset:
    """Subset a dataset to a lat/lon bounding box, longitude must be in -180/180 form"""
    return ds.sel(latitude=slice(north, south), longitude=slice(west, east))

