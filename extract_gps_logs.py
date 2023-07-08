#!/usr/bin/env python
# coding: utf-8

import sys
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString


def main():
    # Read the command line argument as the GPS directory
    if len(sys.argv) < 2:
        print("Please provide the GPS directory path as a command line argument.")
        return

    gps_directory = Path(sys.argv[1])

    # Path to the actual track file
    actual_track_file = gps_directory / 'ActualTrack.dat'

    # Read the actual track data into a DataFrame
    df = pd.read_table(actual_track_file, header=None, names=['lon', 'lat', 'altitude'])
    df = df.drop_duplicates()

    # Create Point geometries from lon and lat columns
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]

    # Create a GeoDataFrame from the DataFrame and Point geometries
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

    # Create a LineString from the Point geometries
    line = LineString(geometry)

    # Create a GeoSeries with the LineString
    line_series = gpd.GeoSeries([line])

    # Create a new GeoDataFrame with the LineString geometry
    line_gdf = gpd.GeoDataFrame(geometry=line_series, crs=gdf.crs)

    # Save the GeoDataFrames to GeoJSON files
    gdf.to_file(gps_directory / 'track.geojson')
    line_gdf.to_file(gps_directory / 'track_line.geojson')


if __name__ == '__main__':
    main()
