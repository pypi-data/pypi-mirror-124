from typing import Tuple
import rasterio


def resolution(input_tiff: str) -> Tuple[int, int]:
    """
    Calculate the resolution of the given TIF file.

    :param input_tiff: Path to TIF file.
    :type input_tiff: str

    :returns: resolution as a (x, y) tuple
    """

    tiff = rasterio.open(input_tiff)
    # get dimensions, in units
    # 1 degree latitude is approx 111 kms
    # 1 degree longitude is approx 111 kms

    # longitude
    width = (
        (tiff.bounds.right - tiff.bounds.left) * 111 * 1000
    )  # converting kms to meters
    # latitude
    height = (tiff.bounds.top - tiff.bounds.bottom) * 111 * 1000

    # get dimensions in pixels
    px_width = tiff.width
    px_height = tiff.height
    print("Width {px_width} , height {px_height} in pixels")

    # meters in one pixel
    w = width / px_width
    h = height / px_height

    return (w, h)
