from typing import Tuple, Optional, List
import cv2
import numpy as np

import json


class ObjectDetection:
    """Various object detection methods"""

    def __init__(self, image_path: str) -> None:
        """
        :param image_path: Path of the input image
        :type image_path: str
        """
        self.image_path = image_path
        if not self.image_path:
            raise Exception("Please pass the path to the image")

    def hog_detection(self) -> List[Tuple[int, int, int, int]]:
        """
        Histogram of gradients-based people detection function

        :returns: List of (x,y,w,h) tuples for all the
        bbox of people detected in the image
        :rtype: list

        :Example:

        from omdenalore.computer_vision.object_detection import ObjectDetection
        >>> detector = ObjectDetection(image_path="sample.jpeg")
        >>> hog_regions = detector.hog_detection()
        """
        # Initializing the HOG person detector
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Reading the Image
        image = cv2.imread(self.image_path)

        # Resizing the Image
        image = self.__resize(image, width=min(400, image.shape[1]))

        # Detects all the regions in the image that has a pedestrians inside it
        regions, _ = hog.detectMultiScale(
            image,
            winStride=(4, 4),
            padding=(4, 4),
            scale=1.05,
        )

        return regions

    def __resize(
        self,
        image: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None,
        inter: int = cv2.INTER_AREA,
    ) -> np.ndarray:
        """Resizes an image to a specific width and height"""
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def mobile_net(self) -> List[Tuple[str, np.ndarray]]:
        """
        Use MobileNet_SSD Object detector to detect classes as mentioned below

        ["background", "aeroplane", "bicycle", "bird", "boat","bottle",
        "bus", "car", "cat", "chair", "cow", "diningtable","dog", "horse",
        "motorbike", "person", "pottedplant", "sheep","sofa", "train",
        "tvmonitor"]

        :param image_path: Path of the image
        :type image_path: str
        :returns: list of tuples and tuples are in the form (label, [bbox])
        :rtype: list of tuples

        :Example:

        from omdenalore.computer_vision.object_detection import ObjectDetection
        >>> detector = ObjectDetection(image_path="sample.jpeg")
        >>> results = detector.mobile_net()
        """

        with open("./components/computervision/config.json") as d:
            config = json.load(d)

        prototxt = config["MobileNet_SSDObjectDetector"]["prototxt"]
        model = config["MobileNet_SSDObjectDetector"]["model"]

        # initialize the list of class labels MobileNet SSD was trained to
        # detect, then generate a set of bounding box colors for each class
        CLASSES = [
            "background",
            "aeroplane",
            "bicycle",
            "bird",
            "boat",
            "bottle",
            "bus",
            "car",
            "cat",
            "chair",
            "cow",
            "diningtable",
            "dog",
            "horse",
            "motorbike",
            "person",
            "pottedplant",
            "sheep",
            "sofa",
            "train",
            "tvmonitor",
        ]

        try:
            net = cv2.dnn.readNetFromCaffe(prototxt, model)
        except Exception:
            raise Exception("Error loading in the neural network")

        # by resizing to a fixed 300x300 pixels and then normalizing it
        # (note: normalization is done via the authors of the MobileNet SSD
        # implementation)

        image = cv2.imread(self.image_path)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)),
            0.007843,
            (300, 300),
            127.5,
        )

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        result = []

        # loop over detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability)
            # associated with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.2:
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)

                result.append((label, [box]))

        return result
