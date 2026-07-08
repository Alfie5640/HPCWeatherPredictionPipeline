import xarray as xr
import pandas as pd

def build_dataset(shearFeatures: xr.Dataset, xrCape: xr.DataArray, brn: xr.DataArray, precip: xr.DataArray, heavyRainThresh: float = 0.001) -> pd.DataFrame:
    all_features = xr.merge([shearFeatures, xrCape, brn, precip])
    dfFeatures = all_features.to_dataframe()
    dfFeatures = dfFeatures.drop(columns=['number', 'expver'])
    dfFeatures = dfFeatures.reset_index()
    dfFeatures['heavy_rain'] = (dfFeatures['tp'] >= heavyRainThresh).astype(int)
    return dfFeatures