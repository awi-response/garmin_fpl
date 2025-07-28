# %%
import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point


def parse_col_from_header(input_file):
    with open(input_file) as src:
        out = src.readlines()
    return [col.replace("\n", "") for col in out[1].split("\t") if col != ""]


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Process a GPS track file and convert coordinates."
    )

    # Add the --gps_file argument
    parser.add_argument(
        "--gps_file",
        type=str,
        required=True,
        help="Path to the input GPS track file (e.g., 2507211202_GPS.dat)",
    )

    # Add the --output_dir argument
    parser.add_argument(
        "--output_dir",
        type=Path,
        required=False,
        help="specify specific output directory where to save the files",
    )

    # Add the --output_dir argument
    parser.add_argument(
        "--output_basename",
        type=str,
        required=False,
        help="specify specific output directory where to save the files",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Use the provided input file path
    input_file = Path(args.gps_file)

    # %%
    df = pd.read_csv(
        input_file, sep=r"\t", decimal=",", engine="python", skiprows=4, header=None
    )

    cols = parse_col_from_header(input_file)

    # Assign meaningful column names for easier access.
    # df.columns = ["Date", "Time", "Lat_DDM", "Lon_DDM", "Altitude"]
    df.columns = ["Date", "Time"] + cols

    # %%
    # Define a function to convert Degrees Decimal Minutes (DDM) to Decimal Degrees (DD).
    def ddm_to_dd(ddm_value, direction):
        # Convert 'ddm_value' to string
        ddm_value_str = str(ddm_value)

        # Convert DDM string to float
        ddm_value_float = float(ddm_value_str)

        # Extract degrees and minutes
        degrees = int(ddm_value_float / 100)
        minutes = ddm_value_float % 100

        # Calculate decimal degrees
        decimal_degrees = degrees + (minutes / 60)

        # Apply direction (negative for West and South)
        if direction == "Lon":
            decimal_degrees = -abs(decimal_degrees)
        return decimal_degrees

    # Apply the conversion to Lat_DDM and Lon_DDM columns.
    df["lat"] = df["Lat"].apply(lambda x: ddm_to_dd(x, "Lat"))
    df["lon"] = df["Lon"].apply(lambda x: ddm_to_dd(x, "Lon"))

    df.drop(columns=["Lon", "Lat"], inplace=True)

    # Create a new column 'geometry' with Point objects from latitude and longitude
    # df['geometry'] = df.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    # Create Point geometries from lon and lat columns
    geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]

    # Create a GeoDataFrame from the DataFrame and Point geometries
    gdf_point = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Create a LineString from the Point geometries
    line = LineString(geometry)

    # Create a GeoSeries with the LineString
    line_series = gpd.GeoSeries([line])

    # Create a new GeoDataFrame with the LineString geometry
    gdf_line = gpd.GeoDataFrame(geometry=line_series, crs=gdf_point.crs)

    if not args.output_dir:
        output_dir = Path(".")
    else:
        output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    if not args.output_basename:
        basename = input_file.stem
    else:
        basename = args.output_basename

    # Save the GeoDataFrames to GeoJSON files
    gdf_point.to_file(output_dir / f"{basename}_points.gpkg")
    gdf_line.to_file(output_dir / f"{basename}_line.gpkg")


if __name__ == "__main__":
    main()
