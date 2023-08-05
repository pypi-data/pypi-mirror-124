from typing import List, Tuple
import numpy as np
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt


class Plot:
    """Plotting functionality for images"""

    @staticmethod
    def plot_cm(
        true: List[float],
        preds: List[float],
        classes: List[int],
        figsize: Tuple[int, int] = (8, 6),
    ):
        """
        Plot unnormalized confusion matrix

        :param true: List of targets
        :param preds: List of predictions
        :param classes: List of classes
        :param figsize: Tuple specifying (height, width)
        :returns: matplotlib figure containing confusion matrix

        :Example:

        from omdenalore.computer_vision.visualisations import Plot
        >>> true = [1.0, 2.0, 3.0]
        >>> preds = [2.0, 2.0, 3.0]
        >>> classes = [0, 1, 2]
        >>> fig = Plot.plot_cm(true, preds, classes)
        """
        cm = metrics.confusion_matrix(true, preds)
        fig = plt.figure(figsize=figsize)
        sns.heatmap(
            cm,
            xticklabels=classes,
            yticklabels=classes,
            annot=True,
            fmt="d",
            cmap="Blues",
            vmin=0.2,
        )
        plt.title("Confusion Matrix")
        plt.ylabel("True Class")
        plt.xlabel("Predicted Class")
        return fig

    @staticmethod
    def unnormalize_image(
        img: List[List[List[int]]],
        means: List[float],
        stds: List[float],
    ):
        """
        Convert normalized image to get unnormalized image

        :param img: Tensor of shape (C, H, W)
        :param means: List of means used for normalization
        :param stds: List of stds used for normalization
        :returns: unnormalized input tensor which can be used to display image

        :Example:

        from omdenalore.computer_vision.visualisations import Plot
        >>> img = ...
        >>> means = [0.4948, 0.4910, 0.4921]
        >>> stds = [0.2891, 0.2896, 0.2880]
        >>> Plot.unnormalize_image(img, means, stds)
        """
        img = img.numpy()
        img = np.transpose(img, (1, 2, 0))
        # unnormalize
        img = img * np.array(stds) + np.array(means)
        return img

    @staticmethod
    def plot_hist(history):
        """
        Plotting train acc, loss and val acc and loss stored in history dict.
        History dict contains keys = {train_acc, val_acc, train_loss, val_loss}
        Each key contains list of scores for every epoch.

        :param history: Dict
        :returns: plot the loss and acc plots for train and val

        :Example:
        from omdenalore.computer_vision.visualisations import Plot
        >>> history = model.fit() # Keras model
        >>> Plot.plot_hist(history)
        """
        # summarize history for accuracy
        plt.plot(history["train_acc"])
        plt.plot(history["val_acc"])
        plt.title("model accuracy")
        plt.ylabel("accuracy")
        plt.xlabel("epoch")
        plt.legend(["train", "val"], loc="upper left")
        plt.show()
        # summarize history for loss
        plt.plot(history["train_loss"])
        plt.plot(history["val_loss"])
        plt.title("model loss")
        plt.ylabel("loss")
        plt.xlabel("epoch")
        plt.legend(["train", "val"], loc="upper left")
        plt.show()
