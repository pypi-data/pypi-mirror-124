import os
from pprint import pprint
import rasterio
from rasterio.plot import show


def raster_summary(raster_dir: str, raster_file: str) -> None:
    """Reads a raster file and outputs the metadata and image.

    :param raster_dir: dir path location of the raster file
    :param raster_file:	raster file name
    """

    # for single file operation, use line by line commands
    # open file for rasterio
    fp = os.path.join(raster_dir, raster_file)

    # Open the file:
    raster = rasterio.open(fp)

    # from rasterio doc: attributes
    print(f"Raster shape:\t\t {raster.shape}")
    print(f"Raster band count:\t {raster.count}")
    print(f"Raster data types:\t {raster.dtypes} ")
    print(f"Raster valid data mask:\t {raster.nodatavals}")
    print(f"Raster not valid mask:\t {raster.nodata}")

    print("Raster metadata:\n")
    pprint(raster.meta)

    # the plot dimensions show the longitude, x, and latitude, y
    show(raster)

    raster.close()
