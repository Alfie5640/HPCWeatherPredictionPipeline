import cdsapi

client = cdsapi.Client()

dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "specific_humidity",
        "temperature"
    ],
    "year": ["2020"],
    "month": ["01"],
    "day": ["01", "02", "03"],
    "time": [
        "00:00", "06:00", "12:00",
        "18:00"
    ],
    "pressure_level": [
        "300", "400", "500",
        "600", "700", "850",
        "925", "1000"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [60, -10, 48, 2]
}

target = "data/raw/era5_cape_sample.nc"
result = client.retrieve(dataset, request)
result.download(target)