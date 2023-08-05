from typing import Tuple
import pandas as pd
import geopandas as gpd
import ee


def geom_to_json(
    df: pd.DataFrame,
    i: int,
) -> Tuple[ee.geometry.Geometry, str]:
    """Converts shapefile or any geometry input into JSON format for GEE.

    :param df: panda dataframe containing shapefile contents
    :param i: integer value indicating which row in the dataframe to process
    :return: Tuple of (JSON string, label)
    """

    # extract the geometry for the given AOI
    g = df.iloc[i, :]

    geom = gpd.GeoSeries(g["geometry"])
    # reflecting the new geopandas API for json conversion
    # 'geometry' is the built in label commonly used in shapefiles,
    # see dataframe
    # [0]th location of the 'features' index in the JSON dictionary order
    jsonDict = eval(geom.to_json())
    geojsonDict = jsonDict["features"][0]

    # call to the GEE API
    region = ee.FeatureCollection(ee.Feature(geojsonDict)).geometry()

    # label the geometry for easy reference
    d = str(g["District Name"]).lower().strip()
    admin = d.replace(" ", "_")

    return region, admin
