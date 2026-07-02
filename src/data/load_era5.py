import xarray as xr
import glob

def load_era5(dirpath: str) -> xr.Dataset:
    files = glob.glob(f"{dirpath}/*.nc")
    ds = xr.open_mfdataset(files, combine="by_coords")
    return ds

if __name__ == "__main__":
    ds = load_era5("data/raw/era5_sample")
    print(ds)