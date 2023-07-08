#!/usr/bin/env python
# coding: utf-8

# In[29]:


import geopandas as gpd
from pathlib import Path
import pandas as pd
from shapely.geometry import Point, LineString
import sys


# In[3]:


#GPSDIR = Path('GPS_070723')
GPSDIR = Path(sys.argv[1])


# In[5]:


actual_track = GPSDIR / 'ActualTrack.dat'


# In[14]:


df = pd.read_table(actual_track, header=None, names=['lon','lat', 'altitude'])
df = df.drop_duplicates()


# In[19]:


geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]

# Create the GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')


# In[24]:


# Create a LineString from the points
line = LineString(geometry)

# Create a GeoSeries with the LineString
line_series = gpd.GeoSeries([line])

# Create a new GeoDataFrame with the LineString geometry
line_gdf = gpd.GeoDataFrame(geometry=line_series, crs=gdf.crs)


# In[27]:


gdf.to_file(GPSDIR / 'track.geojson')
line_gdf.to_file(GPSDIR / 'track_line.geojson')


# In[ ]:




