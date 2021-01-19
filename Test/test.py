
import pandas as pd
import numpy as np
import geopandas as gpd

df = gpd.read_file('https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson')
print(df)
