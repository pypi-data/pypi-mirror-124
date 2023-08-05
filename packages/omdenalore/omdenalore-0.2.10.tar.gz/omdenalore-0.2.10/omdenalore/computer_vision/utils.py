import json
from typing import Any, Sequence, Tuple, Optional, List

from PIL import Image
import cv2
import numpy as np


class Params:
    """
    Class that loads hyperparameters from a json file.

    :Example:

    from omdenalore.computer_vision.utils import Params
    >>> params = Params(json_path)
    >>> print(params.learning_rate)
    >>> params.learning_rate = 0.5
    # change the value of learning_rate in params

    """

    def __init__(self, json_path: str):
        """
        :param json_path: patht to save files in
        :paramtype json_path: str:
        """
        self.update(json_path)

    def save(self, json_path: str):
        """
        Saves parameters to json file

        :param json_path: patht to save files in
        :paramtype json_path: str:
        """
        with open(json_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def update(self, json_path: str):
        """
        Loads parameters from json file

        :param json_path: patht to save files in
        :paramtype json_path: str:
        """
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    def __str__(self) -> str:
        """
        String presentation of the class Params
        """
        return str(self.__dict__)

    @property
    def dict(self):
        """
        Gives dict-like access to Params instance by
        `params.dict['learning_rate']`
        """
        return self.__dict__


def check_imshow():
    """
    Check if environment supports image displays

    :return: Return true of false if you can display image using opencv or not
    :rtype: Boolean

    :Example:

    from omdenalore.computer_vision.utils import check_imshow
    >>> imshow = check_imshow()
    """
    try:
        cv2.imshow("test", np.zeros((1, 1, 3)))
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        return True
    except Exception as e:
        print(
            "WARNING: Environment does not support cv2.imshow()"
            f"or PIL Image.show() image displays\n{e}"
        )
        return False


def zoom_to_fill(
    image: np.ndarray,
    mask: np.ndarray,
    padding: int,
) -> np.ndarray:
    """
    Use the mask to make the object as the center object of
    the image with paddings

    :param image: image from which the object is taken out of
    :type image:  numpy.array
    :param mask: 2d mask array
    :type mask:  numpy.array
    :param padding: add black pixel padding around the image
    :type padding: int
    :return: Image array
    :rtype: numpy.array

    :Example:

    from omdenalore.computer_vision.utils import zoom_to_fill
    >>> padding = 1
    >>> image_ = zoom_to_fill(image, mask, padding)
    """

    (y, x) = np.where(mask == 255)
    (topy, topx) = (np.min(y), np.min(x))
    (bottomy, bottomx) = (np.max(y), np.max(x))
    image = image[
        topy - padding : bottomy + padding,  # noqa: E203
        topx - padding : bottomx + padding,  # noqa: E203
    ]

    return image


def translate_boxes(
    boxes: Sequence[Sequence[Any]], left: Tuple[int], top: Tuple[int]
) -> Sequence[Sequence[Any]]:
    """
    Translates bounding box by moving its cooridantes left-wise by `left`
    pixels and top-wise by `top` pixels.

    :param boxes: list of box coordinates (label,left,top,right,bottom)
    :type boxes: sequence
    :param left: Number of pixels to subtract from horizontal coordinates
    of the bounding box. Moving bounding box to the left is done with
    *left* > 0, and moving to the right with *left* < 0
    :type left: int
    :param top: Number of pixels to subtract from vertical coordinates of
    the bounding box. Moving bounding box top is done with *top* > 0,
    and moving it down with *top* < 0.
    :type top: int
    :returns: list of new box coordinates
    :rtype: list,same as input

    :Example:

    from omdenalore.computer_vision.utils import translate_boxes
    >>> translated_boxes = translate_boxes(boxes, left, top)
    """

    transl_boxes = []
    for box in boxes:
        label, xmin, ymin, xmax, ymax = box
        transl_box = [
            label,
            int(xmin - left[0]),
            int(ymin - top[1]),
            int(xmax - left[0]),
            int(ymax - top[1]),
        ]
        transl_boxes.append(transl_box)

    return transl_boxes


def load_image(path: str) -> Optional[Tuple[Image.Image, int, int]]:
    """
    Load an image at `path` using PIL and return the Image object
    and the width and height

    :param path: path where the image to be loaded is
    :type path: str

    :returns:
        - (PIL.Image.Image): Image object of the image
        - (int): width of the image
        - (int): height of the image

    :Example:

    from omdenalore.computer_vision.utils import load_image
    >>> img, width, height = load_image("sample.jpeg")
    """

    try:
        img = Image.open(path)
        return img, img.size[0], img.size[1]
    except Exception:
        print(f"Image at path {path} cannot be loaded")
        return None


def compute_avg_precision(
    recall: List[float],
    precision: List[float],
) -> Tuple[float, float, float]:
    """
    Compute the average precision, given the recall and precision curves

    :param recall: The recall curve (list)
    :param precision: The precision curve (list)
    :returns:
        - Average precision, precision curve, recall curve

    :Example:

    from omdenalore.computer_vision.utils import compute_avg_precision
    >>> avg_precision, precision_curve, recall_curve = compute_avg_precision(
            recall,
            precision,
        )
    """

    # Append sentinel values to beginning and end
    mrec = np.concatenate(([0.0], recall, [recall[-1] + 0.01]))
    mpre = np.concatenate(([1.0], precision, [0.0]))

    # Compute the precision envelope
    mpre = np.flip(np.maximum.accumulate(np.flip(mpre)))

    # Integrate area under curve
    method = "interp"  # methods: 'continuous', 'interp'
    if method == "interp":
        x = np.linspace(0, 1, 101)  # 101-point interp (COCO)
        ap = np.trapz(np.interp(x, mrec, mpre), x)  # integrate
    else:  # 'continuous'
        # points where x axis (recall) changes
        i = np.where(mrec[1:] != mrec[:-1])[0]
        # area under curve
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])

    return ap, mpre, mrec


def show_cood(
    frame,
    x,
    y,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=1,
    thickness=2,
    color=(255, 0, 0),
    flag=True,
    radius=4,
    fill=-1,
    offset=(1, 1),
):
    """
    Shows the coordinates of the cursor in the OpenCV window.

    :param frame: OpenCV frame/window.
    :param x: The x-coordinate of the point that is to be shown.
    :param y: The y-coordinate of the point that is to be shown.
    :param font: Coordinate text font.
    :param fontScale: Font scale factor that is multiplied by
    the font-specific base size.
    :param color: Text color.
    :param flag: Default True, does not show coordinate values if False.
    :param thickness: Thickness of the lines used to draw a text.
    :param radius: Radius of the circular coordinate point.
    :param fill: Thickness of the circle outline, if positive.
    Negative values, like -1, mean that a filled circle is to be drawn.
    :param offset: Text offset relative to point coordinates.
    :returns:
        - Frame with point at coordinates (x,y).
    :rtype: list,same as input frame.

    Example:
        >>> frame = cv2.imread("EXAMPLE_IMAGE.png")
        >>> frame = show_cursor_cood(frame,x=100,y=100)
        >>> cv2.imshow('frame',frame)
        >>> cv2.waitKey(0)
        >>> cv2.destroyAllWindows()
    """
    copy = frame.copy()
    cv2.circle(
        copy,
        (x, y),
        radius,
        color,
        fill,
    )
    if flag:
        return cv2.putText(
            copy,
            f"({x},{y})",
            (x + offset[0], y + offset[1]),
            font,
            fontScale,
            color,
            thickness,
            cv2.LINE_AA,
        )
    else:
        return copy
