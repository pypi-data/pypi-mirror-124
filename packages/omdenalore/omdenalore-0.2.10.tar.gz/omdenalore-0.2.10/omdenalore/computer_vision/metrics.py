from math import log10, sqrt
from typing import List, Tuple

from image_similarity_measures.quality_metrics import sre as _sre
from image_similarity_measures.quality_metrics import fsim as _fsim
from image_similarity_measures.quality_metrics import issm as _issm
from image_similarity_measures.quality_metrics import sam as _sam
from image_similarity_measures.quality_metrics import uiq as _uiq
import numpy as np
from skimage.metrics import structural_similarity


class Metrics:
    """Image similarity metrics"""

    @staticmethod
    def ssim(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate Structural Similarity Index (SSIM) between two
        3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: SSIM SCORE  which calculated between the two input images.

        :Example:

        from omdenalore.computer_vision.metrics import Metrics
        >>> ssim_score = Metrics.ssim(image1, image2)
        """

        score = 0.0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = structural_similarity(
                    predicted_image, target_image, multichannel=True
                )
            if predicted_image.ndim == 1:
                score = structural_similarity(
                    predicted_image, target_image, multichannel=False
                )
        return score

    # Peak signal-to-noise ratio (PSNR)
    @staticmethod
    def psnr(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculates the Peak Signal-to-Noise Ratio (PSNR) between two
        3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: PSNR SCORE  which calculated between the two input images.

        :Example:

        from omdenalore.computer_vision.metrics import Metrics
        >>> psnr_score = Metrics.psnr(image1, image2)
        """
        score = 0.0

        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate PSNR
            mse = np.mean((target_image - predicted_image) ** 2)
            if mse == 0:
                return 100
            max_pixel = 255.0
            score = 20 * log10(max_pixel / sqrt(mse))
        return score

    # Mean Squared Error (MSE)
    @staticmethod
    def mse(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate the Mean Squared Error (MSE) between two
        3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: MSE SCORE  which calculated between the two input images.

        :Example:

        from omdenalore.computer_vision.metrics import Metrics
        >>> mse_score = Metrics.mse(image1, image2)
        """
        error = np.sum(
            (target_image.astype("float",) - predicted_image.astype("float",)) ** 2,
        )
        error /= float(target_image.shape[0] * target_image.shape[1],)

        # return the MSE
        return error

    # Root Mean Squared Error (RMSE)
    @staticmethod
    def rmse(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate the Root Mean Squared Error (RMSE) between two
        3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: RMSE SCORE  which calculated between the two input images.

        :Example:

        >>> from omdenalore.computer_vision.metrics import Metrics
        >>> rmse_score = Metrics.rmse(image1, image2)
        """
        error = np.sum(
            (target_image.astype("float",) - predicted_image.astype("float",)) ** 2,
        )
        error /= float(target_image.shape[0] * target_image.shape[1])

        root_error = sqrt(error)
        # return the RMSE
        return root_error

    # Intersection over Union (IoU)
    @staticmethod
    def iou(
        predicted_box: List[List[int]], target_box: List[List[int]],
    ) -> Tuple[float, float, float]:
        """
        Calculates the Intersection over Union (IoU) between a Predicted Bounding-box & Target Bounding-box of objects in an image.

        :param predicted_box: Array containing predicted bounding box points [x1,x2,y1,y2]
        :type predicted_box: array
        :param target_box: Array containing target bounding box points [x1,x2,y1,y2]
        :type target_image: array
        :returns: IoU, Union and Intersection SCORES.

        :Example:
        >>> from omdenalore.computer_vision.metrics import Metrics
        >>> iou, union, intersection = Metrics.iou(predicted_box, target_box)

        """
        inter_box_top_left = [
            max(target_box[0], predicted_box[0]),
            max(target_box[1], predicted_box[1]),
        ]
        inter_box_bottom_right = [
            min(target_box[0] + target_box[2], predicted_box[0] + predicted_box[2],),
            min(target_box[1] + target_box[3], predicted_box[1] + predicted_box[3],),
        ]

        inter_box_width = inter_box_bottom_right[0] - inter_box_top_left[0]
        inter_box_height = inter_box_bottom_right[1] - inter_box_top_left[1]

        intersection = inter_box_width * inter_box_height
        union = (
            target_box[2] * target_box[3]
            + predicted_box[2] * predicted_box[3]
            - intersection
        )

        iou = intersection / union

        return iou, union, intersection

    # Structural Dissimilarity (DSSIM)
    @staticmethod
    def dssim(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate the Structural Dissimilarity(DSSIM) between two 3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: DSSIM SCORE  which calculated between the two input images

        :Example:
        >>> from omdenalore.computer_vision.metrics Metrics
        >>> dssim_score = Metrics.dssim(image1, image2)
        """
        dssim_score = 0.0
        score = 0.0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = structural_similarity(
                    predicted_image, target_image, multichannel=True
                )
            if predicted_image.ndim == 1:
                score = structural_similarity(
                    predicted_image, target_image, multichannel=False
                )

            dssim_score = (1 - score) / 2
        return dssim_score

    # Signal to Reconstruction Error ratio (SRE)
    @staticmethod
    def sre(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """

        Calculate the Signal to Reconstruction Error ratio (SRE) between
        two 3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: SRE SCORE  which calculated between the two input images.

        :Example:
        >>> from omdenalore.computer_vision.metrics import Metrics
        >>> sre_score = Metrics.sre(image1, image2)

        """

        score = 0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = _sre(target_image, predicted_image)
            if predicted_image.ndim == 1:
                score = _sre(target_image, predicted_image)

        return score

    # Feature-based similarity index (FSIM)
    @staticmethod
    def fsim(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate the Feature-based similarity index (FSIM) between
        two 3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: FSIM SCORE  which calculated between the two input images.

        """

        score = 0.0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = _fsim(target_image, predicted_image)
            if predicted_image.ndim == 1:
                score = _fsim(target_image, predicted_image)

        return score

    # Information theoretic-based Statistic Similarity Measure (ISSM)
    @staticmethod
    def issm(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculates the Information theoretic-based
        Statistic Similarity Measure (ISSM)
        between two 3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: ISSIM SCORE  which calculated between the two input images.

        :Example:
        from omdenalore.computer_vision.metrics import Metrics
        >>> issm_score = Metrics.issm(image1, image2)
        """

        score = 0.0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = _issm(target_image, predicted_image)
            if predicted_image.ndim == 1:
                score = _issm(target_image, predicted_image)

        return score

    # Spectral angle mapper (SAM)
    @staticmethod
    def sam(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate the Spectral angle mapper (SAM) between two
        3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: SAM SCORE  which calculated between the two input images.

        :Example:

        from omdenalore.computer_vision.metrics import Metrics
        >>> sam_score = Metrics.sam(image1, image2)

        """

        score = 0.0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = _sam(target_image, predicted_image)
            if predicted_image.ndim == 1:
                score = _sam(target_image, predicted_image)

        return score

    # Universal image quality index (UIQ)
    @staticmethod
    def uiq(predicted_image: np.ndarray, target_image: np.ndarray,) -> float:
        """
        Calculate the Universal image quality index (UIQ) between two
        3 Colored Channel/Grayscale images.

        :param predicted_image: Image Data for predicted image as numpy array
        :type predicted_image: np.array
        :param target_image: Image Data for target image as numpy array
        :type target_image: np.array
        :returns: UIQ SCORE  which calculated between the two input images.

        :Example:
        from omdenalore.computer_vision.metrics import Metrics
        >>> uiq_score = Metrics.uiq(image1, image2)

        """

        score = 0.0

        # check image dimensions
        if predicted_image.ndim == target_image.ndim:
            if predicted_image.ndim == 4:
                predicted_image = np.squeeze(predicted_image, axis=0)
                target_image = np.squeeze(target_image, axis=0)

            # calculate for multichannel images
            if predicted_image.ndim > 1:
                score = _uiq(target_image, predicted_image)
            if predicted_image.ndim == 1:
                score = _uiq(target_image, predicted_image)

        return score
