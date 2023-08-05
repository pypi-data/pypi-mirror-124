from rasterio.crs import CRS
import rioxarray as rxr


def reproject_raster(rf: rxr, new_crs: str) -> rxr:
    """
    Reproject the raster from a current CRS to a user specified CRS.

    :param rf: (r)aster (f)ile sent for reprojection
    :param new_crs: user defined new CRS projection

    :Example:

    from omdenalore.satellite_imagery.reproject_crs import reproject_raster
    new_raster_object = reproject_raster(current_raster, 'EPSG:4326')

    """

    # open the raster with rioxarray
    file_crs = rxr.open_rasterio(rf, masked=True).squeeze()

    # display current CRS
    print(f"Raster file current CRS: {file_crs.rio.crs}")

    # obtain new CRS
    crs_wgs84 = CRS.from_string(new_crs)

    # Reproject the dataset with the new crs
    new_wgs84 = file_crs.rio.reproject(crs_wgs84)

    # display new CRS
    print(f"New reprojected raster file CRS: {new_wgs84.rio.crs}")

    return new_wgs84
