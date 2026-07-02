import cdsapi

client = cdsapi.Client()

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "mean_sea_level_pressure",
        "total_precipitation"
    ],
    "year": ["2020"],
    "month": ["01"],
    "day": ["01", "02", "03"],
    "time": ["00:00", "06:00", "12:00", "18:00"],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [60, -10, 48, 2]
}
target = "data/raw/era5_sample.nc"

client.retrieve(dataset, request, target)