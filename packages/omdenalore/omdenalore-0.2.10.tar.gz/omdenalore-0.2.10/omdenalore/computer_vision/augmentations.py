from typing import List
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2


class Augmenter:
    """Basic augmentations for images"""

    @staticmethod
    def get_basic_train_transforms(
        height: int,
        width: int,
        means: List[float],
        stds: List[float],
    ):
        """
        Apply only basic training transformations such as Resize and Normalize.

        :param height: int specifying new height
        :param width: int specifying new width
        :param means: List of means for normalization
        :param stds: List of stds for normalization
        :returns: Albumentation compose transform object for training dataset

        :Example:

        from omdenalore.computer_vision.augmentations import Augmenter
        import cv2

        >>> transform = Augmenter.get_basic_train_transforms(
                height=256,
                width=256,
                means=[0.485, 0.456, 0.406],
                stds=[0.229, 0.224, 0.225],
            )

        # Read an image with OpenCV and convert it to the RGB colorspace
        >>> image = cv2.imread("image.jpg")
        >>> image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Augment an image
        >>> transformed = transform(image=image)
        >>> transformed_image = transformed["image"]
        """
        trn_transform = A.Compose(
            [
                A.Resize(height, width, cv2.INTER_NEAREST),
                A.Normalize(mean=means, std=stds),
                ToTensorV2(),
            ]
        )
        return trn_transform

    @staticmethod
    def get_mild_train_transforms(
        height: int,
        width: int,
        means: List[float],
        stds: List[float],
    ):
        """
        Apply few mild training transformations such as Resize,
        horizontal and vertical, Gaussian Noise,
        Perspective Shift and Normalize.

        :param height: int specifying new height
        :param width: int specifying new width
        :param means: List of means for normalization
        :param stds: List of stds for normalization
        :returns: Albumentation compose transform object for training dataset

        :Example:

        from omdenalore.computer_vision.augmentations import Augmenter
        import cv2

        >>> transform = Augmenter.get_mild_train_transforms(
                height=256,
                width=256,
                means=[0.485, 0.456, 0.406],
                stds=[0.229, 0.224, 0.225],
            )

        # Read an image with OpenCV and convert it to the RGB colorspace
        >>> image = cv2.imread("image.jpg")
        >>> image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Augment an image
        >>> transformed = transform(image=image)
        >>> transformed_image = transformed["image"]
        """
        trn_transform = A.Compose(
            [
                A.Resize(height, width, cv2.INTER_NEAREST),
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.5),
                A.GaussNoise(p=0.2),
                A.Perspective(p=0.5),
                A.Normalize(mean=means, std=stds),
                ToTensorV2(),
            ]
        )
        return trn_transform

    @staticmethod
    def get_val_transforms(
        height: int,
        width: int,
        means: List[float],
        stds: List[float],
    ):
        """
        Apply only basic transformation such as Resize and Normalize.
        :param height: int specifying new height
        :param width: int specifying new width
        :param means: List of means for normalization
        :param stds: List of stds for normalization
        :returns: Albumentation compose transform object for validation dataset

        :Example:

        from omdenalore.computer_vision.augmentations import Augmenter
        import cv2

        >>> transform = Augmenter.get_val_transforms(
                height=256,
                width=256,
                means=[0.485, 0.456, 0.406],
                stds=[0.229, 0.224, 0.225],
            )

        # Read an image with OpenCV and convert it to the RGB colorspace
        >>> image = cv2.imread("image.jpg")
        >>> image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Augment an image
        >>> transformed = transform(image=image)
        >>> transformed_image = transformed["image"]

        """
        val_transform = A.Compose(
            [
                A.Resize(height, width, cv2.INTER_NEAREST),
                A.Normalize(mean=means, std=stds),
                ToTensorV2(),
            ]
        )
        return val_transform
