import tensorflow as tf
from tensorflow.keras import backend as K


class LossFunctions:
    """Various loss functions using Keras"""

    @staticmethod
    def class_tversky(y_true, y_pred):
        """
        Returns Tversky Class for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> loss = LossFunctions.class_tversky(y_true,y_pred)
        """
        smooth = 1

        y_true = K.permute_dimensions(y_true, (3, 1, 2, 0))
        y_pred = K.permute_dimensions(y_pred, (3, 1, 2, 0))

        y_true_pos = K.batch_flatten(y_true)
        y_pred_pos = K.batch_flatten(y_pred)
        true_pos = K.sum(y_true_pos * y_pred_pos, 1)
        false_neg = K.sum(y_true_pos * (1 - y_pred_pos), 1)
        false_pos = K.sum((1 - y_true_pos) * y_pred_pos, 1)
        alpha = 0.7
        return (true_pos + smooth) / (
            true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth
        )

    @staticmethod
    def focal_tversky_loss(y_true, y_pred):
        """
        Returns focal Tversky loss for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> loss = LossFunctions.focal_tversky_loss(y_true, y_pred)
        """
        pt_1 = LossFunctions.class_tversky(y_true, y_pred)
        gamma = 0.75
        return K.sum(K.pow((1 - pt_1), gamma))

    @staticmethod
    def dice_coef(y_true, y_pred):
        """
        Returns dice coefficient for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> dice_coef = LossFunctions.dice_coef(y_true, y_pred)
        """
        smooth = 1.0
        y_true_f = K.flatten(y_true)
        y_pred_f = K.flatten(y_pred)
        intersection = K.sum(y_true_f * y_pred_f)
        return (2.0 * intersection + smooth) / (
            K.sum(y_true_f) + K.sum(y_pred_f) + smooth
        )

    @staticmethod
    def dice_coef_loss(y_true, y_pred):
        """
        Returns dice_coef_loss for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> loss = LossFunctions.dice_coef_loss(y_true, y_pred)
        """
        return 1 - LossFunctions.dice_coef(y_true, y_pred)

    @staticmethod
    def generalized_dice_coefficient(y_true, y_pred):
        """
        Returns generalized_dice_coefficient for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions

        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> gdc = LossFunctions.generalized_dice_coefficient(
                y_true, y_pred
            )
        """
        smooth = 1.0
        y_true_f = K.flatten(y_true)
        y_pred_f = K.flatten(y_pred)
        intersection = K.sum(y_true_f * y_pred_f)
        score = (2.0 * intersection + smooth) / (
            K.sum(y_true_f) + K.sum(y_pred_f) + smooth
        )
        return score

    @staticmethod
    def dice_loss(y_true, y_pred):
        """
        Returns dice_loss for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor

        :Example:

        >>> from omdenalore.computer_vision.loss_functions_semantic import LossFunctions

        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> gdcl = LossFunctions.generalized_dice_coefficient_loss(
        >>>     y_true, y_pred
        >>>)
        """
        loss = 1 - LossFunctions.generalized_dice_coefficient(y_true, y_pred)
        return loss

    @staticmethod
    def confusion_matrix(y_true, y_pred):
        """
        Returns confusion matrix for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> confusion_matrix = LossFunctions.confusion_matrix(y_true, y_pred)
        """
        smooth = 1
        y_pred_pos = K.clip(y_pred, 0, 1)
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.clip(y_true, 0, 1)
        y_neg = 1 - y_pos
        tp = K.sum(y_pos * y_pred_pos)
        fp = K.sum(y_neg * y_pred_pos)
        fn = K.sum(y_pos * y_pred_neg)
        prec = (tp + smooth) / (tp + fp + smooth)
        recall = (tp + smooth) / (tp + fn + smooth)
        return prec, recall

    @staticmethod
    def true_positive(y_true, y_pred):
        """
        Returns True positives for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> tp = LossFunctions.true_positive(y_true, y_pred)
        """
        smooth = 1
        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pos = K.round(K.clip(y_true, 0, 1))
        tp = (K.sum(y_pos * y_pred_pos) + smooth) / (K.sum(y_pos) + smooth)
        return tp

    @staticmethod
    def true_negative(y_true, y_pred):
        """
        Returns true negetive for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> tn = LossFunctions.true_negative(y_true, y_pred)
        """
        smooth = 1
        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.round(K.clip(y_true, 0, 1))
        y_neg = 1 - y_pos
        tn = (K.sum(y_neg * y_pred_neg) + smooth) / (K.sum(y_neg) + smooth)
        return tn

    @staticmethod
    def tversky_index(y_true, y_pred):
        """
        Returns Tversky index for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> tversky_index = LossFunctions.tversky_index(y_true, y_pred)
        """
        y_true_pos = K.flatten(y_true)
        y_pred_pos = K.flatten(y_pred)
        true_pos = K.sum(y_true_pos * y_pred_pos)
        false_neg = K.sum(y_true_pos * (1 - y_pred_pos))
        false_pos = K.sum((1 - y_true_pos) * y_pred_pos)
        alpha = 0.7
        smooth = 1
        return (true_pos + smooth) / (
            true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth
        )

    @staticmethod
    def tversky_loss(y_true, y_pred):
        """
        Returns Tversky loss for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> tversky_loss = LossFunctions.tversky_loss(y_true, y_pred)
        """
        return 1 - LossFunctions.tversky_index(y_true, y_pred)

    @staticmethod
    def focal_tversky(y_true, y_pred):
        """
        Returns focal Tversky loss for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> focal_tversky = LossFunctions.focal_tversky(y_true, y_pred)
        """
        pt_1 = LossFunctions.tversky_index(y_true, y_pred)
        gamma = 0.75
        return K.pow((1 - pt_1), gamma)

    @staticmethod
    def log_cosh_dice_loss(y_true, y_pred):
        """
        Returns log_cosh_dice loss for truth vs prediction values

        :param y_true: A tensor of the same shape as `y_pred`
        :type y_true: tensor
        :param y_pred: A tensor resulting from a softmax
        :type y_pred: tensor
        :return: Output tensor.

        :Example:

        from omdenalore.computer_vision.loss_functions_semantic import LossFunctions
        >>> y_true = [1.0, 2.0, 3.0]
        >>> y_pred = [0.0, 1.0, 3.0]
        >>> lcdl = LossFunctions.log_cosh_dice_loss(y_true, y_pred)
        """
        x = LossFunctions.dice_loss(y_true, y_pred)
        return tf.math.log((tf.exp(x) + tf.exp(-x)) / 2.0)
