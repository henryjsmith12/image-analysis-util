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

class ROIWindow(QtGui.QWidget):
    """
    Houses ROI widgets.

    TODO: Populate widget with subwidgets/layout
    """

    def __init__(self, parent) -> None:
        super(ROIWindow, self).__init__(parent)
        self.main_window = parent

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)