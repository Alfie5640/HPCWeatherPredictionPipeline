from dask import array as da

x = da.random.random((10000, 10000), chunks=(1000, 1000))
y = (x + x.T).mean()

print(y.compute())