from typing import List, Tuple, Union
import cv2
import glob
import mahotas
import numpy as np
from matplotlib import pyplot as plt


class ImageFeatures:
    """Class containing image feature methods"""

    @staticmethod
    def surf_features(image_path: str) -> List[float]:
        """
        detect SURF features from an image path

        :param image_path: Path of the input image
        :type image_path: str
        :returns: SURF keypoints detected from an image

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.surf_features(image_path="sample.jpeg")
        """

        if not image_path:
            raise Exception("Please pass the path to the image")
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        surf = cv2.xfeatures2d.SURF_create(400)
        kp, _ = surf.detectAndCompute(gray, None)

        return kp

    @staticmethod
    def sift_features(image_path: str, grayscale: bool = True) -> List[float]:
        """
        detect SIFT features from an image path

        :param image_path: Path of the input image
        :type image_path: str
        :param grayscale: converts image to grayscale
        :type grayscale: boolean
        :returns: SIFT keypoints detected from an image

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.sift_features(image_path="sample.jpeg")
        """
        if not image_path:
            raise Exception("Please pass the path to the image")
        im = cv2.imread(image_path)

        if grayscale:
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            sift = cv2.xfeatures2d.SIFT_create()
            kp = sift.detect(gray, None)
        else:
            sift = cv2.xfeatures2d.SIFT_create()
            kp = sift.detect(im, None)

        return kp

    @staticmethod
    def brief_features(image_path: str) -> List[int]:
        """
        detect BRIEF features from an image path

        :param image_path: Path of the input image
        :type image_path: str
        :returns: BRIEF keypoints detected from an image

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.brief_features(image_path="sample.jpeg")
        """
        if not image_path:
            raise Exception("Please pass the path to the image")
        im = cv2.imread(image_path)
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kps = star.detect(im, None)
        kp, _ = brief.compute(im, kps)
        return kp

    @staticmethod
    def haralicks_features(image_path: str) -> List[Tuple[str, float]]:
        """
        Detects Harlicks features from images in meaned four directions
        inside an folder with certain extensions
        and returns array of retrieved features

        :param image_path: Path of the folder which contains the png images
        :type image_path: string

        :returns: array of extracted features - (image_name , features)

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.haralicks_features(image_path="sample.jpeg")
        """
        if not image_path:
            raise Exception("Please pass the path to the image")

        accepted_image_extentions = ["jpeg", "png"]

        data = []
        label = []

        for image_paths in glob.glob(image_path + "/*"):

            # check to see if a image is of acceptable format or not
            for i in range(len(accepted_image_extentions)):
                if not image_paths.endswith(accepted_image_extentions[i]):
                    raise Exception("File type not accepted",)

            # load the image, convert it into greyscalse,
            image = cv2.imread(image_paths)
            image = cv2.cvtColor(image, cv2.COLOR_BG2GRAY)

            # extract image name from the path
            label.append(image_paths[image_paths.rfind("/") + 1 :],)  # noqa: E203

            # extract haralicks texture features in 4 directions,
            # take mean if each direction
            features = mahotas.features.haralick(image).mean(axis=0)

            # update the data with features
            data.append(features)

        return list(zip(label, data))

    @staticmethod
    def describe_zernike_moments(image_path: str) -> List[Tuple[int, float]]:
        """
        Calculates the Zernike moments of images inside a folder.
        Returns list of features and corresponding image names
        Zernike moments are great for describing shapes of objects.

        :param image_path: Path of images
        :type image_path: string

        :returns: return a tuple of the contours and shapes

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.describe_zernike_moments(image_path="sample.jpeg")
        """
        if not image_path:
            raise Exception("Please pass the path to the image")

        accepted_image_extentions = ["jpeg", "png"]
        shapeFeatures = []

        for i in enumerate(accepted_image_extentions):
            if not image_path.endswith(accepted_image_extentions[i]):
                raise Exception("File type not accepted",)
        # load the image, convert it into greyscalse,
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BG2GRAY)
        blurred = cv2.GaussianBlur(gray, (13, 13), 9)
        thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]

        # perform a series of dilations and erosions to close holes
        # in the shapes
        thresh = cv2.dilate(thresh, None, iterations=4)
        thresh = cv2.erode(thresh, None, iterations=2)

        # detect contours in the edge map
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = ImageFeatures._grab_contours(cnts)
        # loop over the contours
        for c in cnts:
            # create an empty mask for the contour and draw it
            mask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            # extract the bounding box ROI from the mask
            (x, y, w, h) = cv2.boundingRect(c)
            roi = mask[y : y + h, x : x + w]  # noqa: E203

            # compute Zernike Moments for the ROI and update the list
            # of shape features
            features = mahotas.features.zernike_moments(
                roi, cv2.minEnclosingCircle(c)[1], degree=8
            )
            shapeFeatures.append(features)

        # return a tuple of the contours and shapes
        return (cnts, shapeFeatures)

    @staticmethod
    def find_contours(image_path: str, show: bool = False) -> List[List[int]]:
        """
        Detect contours from an image path

        :param image_path: Path of the input image
        :type image_path: str
        :param show: Whether to show the contours on a plot using matplotlib
        :type show: boolean
        :returns: contours detected from an image

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.find_contours(image_path="sample.jpeg", show=True)
        """
        if not image_path:
            raise Exception("Please pass the path to the image")

        im = cv2.imread(image_path)

        # convert to RGB
        rgb_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # convert to grayscale
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

        # create a binary thresholded image
        _, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE,)

        if show:
            image = cv2.drawContours(rgb_image, contours, -1, (0, 255, 0), 3,)
            plt.imshow(image)
            plt.show()

        return contours

    def _grab_contours(
        cnts: Union[List[List[int]], List[List[List[int]]]],
    ) -> List[int]:
        """Helper method to grab the contours from a cv2.findContours()"""
        # if the length the contours tuple returned by cv2.findContours
        # is '2' then we are using either OpenCV v2.4, v4-beta, or
        # v4-official
        if len(cnts) == 2:
            cnts = cnts[0]

        # if the length of the contours tuple is '3' then we are using
        # either OpenCV v3, v4-pre, or v4-alpha
        elif len(cnts) == 3:
            cnts = cnts[1]

        # otherwise OpenCV has changed their cv2.findContours return
        # signature yet again and I have no idea WITH is going on
        else:
            raise Exception(
                (
                    "Contours tuple must have length 2 or 3, "
                    "otherwise OpenCV changed their cv2.findContours return "
                    "signature yet again. Refer to OpenCV's documentation "
                    "in that case"
                )
            )

        # return the actual contours array
        return cnts

    @staticmethod
    def get_hough_lines(image_path: str, show: bool = False,) -> List[List[float]]:
        """
        Detect lines from an image path

        :param image_path: Path of the input image
        :type image_path: str
        :param show: Whether to show the lines on a plot using matplotlib
        :type show: boolean
        :returns: lines detected from an image

        :Example:

        from omdenalore.computer_vision.image_features import ImageFeatures
        >>> ImageFeatures.get_hough_lines(image_path="sample.jpeg", show=True)
        """
        if not image_path:
            raise Exception("Please pass the path to the image")

        img = cv2.imread(image_path)

        grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # perform edge detection
        edges = cv2.Canny(grayscale, 30, 100)

        # detect lines in the image using hough lines technique
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, np.array([]), 50, 5,)

        if show:
            # iterate over the output lines and draw them
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(
                        img, (x1, y1), (x2, y2), (20, 220, 20), 3,
                    )

            # show the image
            plt.imshow(img)
            plt.show()

        return lines
