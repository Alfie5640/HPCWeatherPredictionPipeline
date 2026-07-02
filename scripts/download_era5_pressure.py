import cdsapi

client = cdsapi.Client()

dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "u_component_of_wind",
        "v_component_of_wind"
    ],
    "year": ["2020"],
    "month": ["01"],
    "day": ["01", "02", "03"],
    "time": [
        "00:00", "06:00", "12:00",
        "18:00"
    ],
    "pressure_level": ["500", "850"],
    "data_format": "netcdf",
    "download_format": "unarchived"
}


target = "data/raw/era5_sample.nc"
client.retrieve(dataset, request).download()