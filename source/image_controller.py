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

# ==============================================================================

class ImageController(QtGui.QWidget):
    """
    Controllers image options, colormap.
    """

    def __init__(self, parent) -> None:
        super(ImageController, self).__init__(parent)
        self.main_window = parent