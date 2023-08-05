try:
    import ee
except:  # noqa: E722
    print(
        "You need to install related package google-api-python-client & earthengine-api"  # noqa: E501
    )

try:
    ee.Initialize()
except:  # noqa: E722
    print(
        "Please follow this guidelines to authenticate"
        "https://earthlab.colorado.edu/introduction-google-earth-engine-python-api"  # noqa: E501
        "in case you get error certify error in MacOs go to"
        "Macintosh HD > Applications > Python3.6 folder"
        "(or whatever version of python you're using)"
        "double click on Install Certificates.command file"
    )


class Download:
    """
    Download is used to extract image and aggreagted image collection from
    GEE to gdrive in tiff format.
    It supports clip border & parallel progress monintor tasks at
    https://code.earthengine.google.com/

    :Example:

    >>> d = Download(url = "LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515",
    gdrive_folder = "ee")
    >>> border = d._border(
        border_url="FAO/GAUL/2015/level0",
        feature='ADM0_NAME',
        location='France'
        )
    """

    def __init__(self, url, gdrive_folder="ee") -> None:
        """
        :param url: path to GEE image/image collection
        :type url: str
        :param gdrive_folder: folder name to save tiff file(s).
        If not exists, it will create new folder
        :type gdrive_folder: str
        """
        self.url = f"{url}"
        self.gdrive_folder = gdrive_folder

    def _border(
        self,
        border_url="FAO/GAUL/2015/level0",
        feature="ADM0_NAME",
        location="France",  # noqa: E501
    ):
        """
        The border to clip in download
        :param:border_url: path to border image
        :type border_url: str
        :param feature: feature to crop border
        :type feature: str
        :param location: location want to be croped
        :type location: str
        """
        self.border_url = f"{border_url}"
        self.feature = feature
        self.location = location

        border = (
            ee.FeatureCollection(f"{self.border_url}")
            .filterMetadata(self.feature, "equals", self.location)
            .geometry()
        )
        return border

    def download_img(self, maxPixels=int(1e13), border=None, scale=None):
        """
        download image to gdrive
        :param maxPixels: restrict the number of pixels in the export.
        Default is nt(1e13)
        :type maxPixels: int
        :param border: border to crop. Default is None
        :type border: Geometry
        :param scale: resolution in meters per pixel. Default is None
        :type scale: int

        :Example:
        >>> url1 = "LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515"
        >>> d = Download(url = url1, gdrive_folder='ee_img')
        >>> border = d._border()
        >>> d.download_img(maxPixels = int(1e13),border = border, scale=1000)

            {'state': 'READY',
            'description': 'LANDSAT_LC08_C01_T1_TOA_LC08_123032_20140515_BQA',
            'creation_timestamp_ms': 1633232785552,
            'update_timestamp_ms': 1633232785552,
            'start_timestamp_ms': 0,
            'task_type': 'EXPORT_IMAGE',
            'id': 'KLRMMUXTXLF7BBSPZ7XWRMYL',
            'name':
            'projects/earthengine-legacy/operations/KLRMMUXTXLF7BBSPZ7XWRMYL'}
        """

        self.border = border
        self.scale = scale
        self.maxPixels = maxPixels

        image = ee.Image(self.url)

        meta = image.getInfo()
        props = meta["properties"]

        image_name = props.get("id") or meta["id"]
        image_name = image_name.replace("/", "_")

        if self.border:
            image = image.clip(self.border)
        else:
            image = image

        for i, band in enumerate(meta["bands"]):
            band_image = image.select(i)
            band_name = band["id"]
            task_name = f"{image_name}_{band_name}"
            crs = band["crs"]
            crs_transform = props.get("crs_transform") or band["crs_transform"]
            task = ee.batch.Export.image.toDrive(
                description=task_name,
                fileNamePrefix=task_name,
                folder=self.gdrive_folder,
                image=band_image,
                crs=crs,
                crs_transform=str(crs_transform),
                scale=self.scale,
                fileFormat="GeoTIFF",
                maxPixels=self.maxPixels,
            )
            task.start()
        return task.status()

    def download_imgcol(
        self,
        border=None,
        scale=None,
        start_date=None,
        end_date=None,
        aggfunc="median",
        maxPixels=int(1e13),
    ):
        """
        Aggregate image collection into a single image then export
        :param border: border to crop. Default is None
        :type border: Geometry
        :param scale: resolution in meters per pixel. Default is None
        :type scale: int
        :param start_date: applicable if you want to filter a specific date
        range. Default is None
        :type start_date: str format "%Y-%m-%d"
        :param end_date: applicable if you want to filter a specific date
        range. Default is None
        :type end_date: str format "%Y-%m-%d"
        :param aggfunc: function to aggregate image collections.
        Default is median
        :type: str
        :param maxPixels: restrict the number of pixels in the export.
        Default is nt(1e13)
        :type maxPixels: int

        :Example:

        >>> url2 = "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG"
        >>> d = Download(url = url2, gdrive_folder='ee_imgcol')
        >>> border = d._border()
        >>> d.download_imgcol(
            border = border,
            scale = 1000,
            start_date = '2018-01-01',
            end_date = '2018-06-12'
            )

            {'state': 'READY',
            'description': 'NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG_cf_cvg',
            'creation_timestamp_ms': 1633234067247,
            'update_timestamp_ms': 1633234067247,
            'start_timestamp_ms': 0,
            'task_type': 'EXPORT_IMAGE',
            'id': 'GVJ3FSIIVFWRG5YXR34TDR7S',
            'name':
            'projects/earthengine-legacy/operations/GVJ3FSIIVFWRG5YXR34TDR7S'}
        """

        self.start_date = start_date
        self.end_date = end_date
        self.border = border
        self.scale = scale
        self.aggfunc = aggfunc
        self.maxPixels = maxPixels

        imagecoll = ee.ImageCollection(self.url)
        image_name = imagecoll.getInfo()["id"]
        image_name = image_name.replace("/", "_")

        if self.start_date and self.end_date:
            imagecoll = imagecoll.filter(
                ee.Filter.date(self.start_date, self.end_date),
            )
        else:
            imagecoll = imagecoll
        if self.border:
            image = getattr(imagecoll, self.aggfunc)().clip(self.border)
        else:
            image = getattr(imagecoll, self.aggfunc)()

        meta = image.getInfo()
        props = meta["properties"]

        for i, band in enumerate(meta["bands"]):
            band_image = image.select(i)
            band_name = band["id"]
            task_name = f"{image_name}_{band_name}"
            crs = band["crs"]
            crs_transform = props.get("crs_transform") or band["crs_transform"]
            task = ee.batch.Export.image.toDrive(
                description=task_name,
                fileNamePrefix=task_name,
                folder=self.gdrive_folder,
                image=band_image,
                crs=crs,
                crs_transform=str(crs_transform),
                scale=self.scale,
                fileFormat="GeoTIFF",
                maxPixels=self.maxPixels,
            )
            task.start()
        return task.status()
