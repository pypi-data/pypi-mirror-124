from tensorflow.keras.layers import (
    Input,
    concatenate,
    MaxPooling2D,
    Conv2D,
    UpSampling2D,
)
from tensorflow.keras.models import Model


class GreenPixelDetector:
    """Detect the green pixels in an image"""

    @staticmethod
    def detect(pretrained_weights, optimizer, loss, input_size):
        """

        :param pretrained_weights: pretrained weight matrix
        :param input_size: image dimension tuple
        :param input_size: (img_height, img_width, input_channel)
        :param optimizer: optimization strategy
        :param loss: loss function
        :type pretrained_weights: numpy ndarray
        :type input_size: tuple
        :type optimizer: optimizer object
        :type loss: loss object
        :return: compiled Keras model
        :rtype: Keras model object
        """

        inputs = Input(input_size)

        conv1_1 = Conv2D(16, (3, 3), padding="same",)(inputs)
        pool1 = MaxPooling2D(2, 2,)(conv1_1)

        conv3_1 = Conv2D(32, (5, 5), activation="relu", padding="same",)(pool1)
        conv3_1 = Conv2D(32, (5, 5), activation="relu", padding="same",)(conv3_1)

        up2_1 = UpSampling2D(size=2, interpolation="bilinear",)(conv3_1)

        output = concatenate([up2_1, conv1_1], axis=3,)
        output = Conv2D(1, (1, 1), activation="sigmoid", padding="same",)(output)

        model = Model(inputs, output)
        model.compile(optimizer=optimizer, loss=loss)

        if pretrained_weights:
            model.load(pretrained_weights)

        return model
