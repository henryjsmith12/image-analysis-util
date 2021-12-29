"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ==============================================================================

import h5py
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

from source.image_plot import ImagePlot
from source.image_controller import ImageController

# ==============================================================================

class MainWindow(QtGui.QWidget):
    """
    Houses widgets for analysis window
    """

    def __init__(self, file_path) -> None:
        super().__init__()

        self.file_path = file_path

        self.image_plot = ImagePlot(self)
        self.image_controller = ImageController(self)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.image_plot, 0, 0)
        self.layout.addWidget(self.image_controller, 1, 0)
