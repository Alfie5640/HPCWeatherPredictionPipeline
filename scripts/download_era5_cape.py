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
    "month": ["09", "10", "11", "12"],
    "day": [f"{d:02d}" for d in range(1, 32)],
    "time": ["00:00", "06:00", "12:00", "18:00"],
    "pressure_level": [
        "300", "400", "500",
        "600", "700", "850",
        "925", "1000"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [60, -10, 48, 2]
}
target = "data/raw/era5_cape_sample_autumn2020.nc"

result = client.retrieve(dataset, request)
result.download(target)