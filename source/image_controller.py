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
    Controls the orthogonal slice in view and slicing direction.

    TODO: Add "Swap Axes" button/area with radio button grid
    """

    def __init__(self, parent) -> None:
        super(ImageController, self).__init__(parent)
        self.main_window = parent

        # Subwidgets
        self.slider1 = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider1_lbl = QtGui.QLabel()
        self.slider1_cbx = QtGui.QComboBox()
        self.slider2 = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider2_lbl = QtGui.QLabel()
        self.slider2_cbx = QtGui.QComboBox()

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.slider1_lbl, 0, 0)
        self.layout.addWidget(self.slider1, 0, 1, 1, 6)
        self.layout.addWidget(self.slider1_cbx, 0, 7)
        self.layout.addWidget(self.slider2_lbl, 1, 0)
        self.layout.addWidget(self.slider2, 1, 1, 1, 6)
        self.layout.addWidget(self.slider2_cbx, 1, 7)

        # Connections