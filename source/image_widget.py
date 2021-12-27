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

class ImageWidget(QtGui.QWidget):

    def __init__(self, parent) -> None:
        super(ImageWidget, self).__init__(parent)
        self.main_window = parent

        # ImageView widget that displays data
        self.image_plot = ImagePlot(self)
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.image_plot, 0, 0)

    def plot():
        ...

# ==============================================================================

class ImagePlot(pg.ImageView):

    def __init__(self, parent=None, view=None) -> None:
        super(ImagePlot, self).__init__(parent, view=pg.PlotItem())

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()


