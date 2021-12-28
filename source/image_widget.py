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
    """
    
    """

    def __init__(self, parent) -> None:
        super(ImageWidget, self).__init__(parent)
        self.main_window = parent

        # Subwidgets
        self.image_plot = ImagePlot(self) # ImageView widget that displays image
        self.image_controller = ImageController(self) # Controls image in view
        
        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.image_plot, 0, 0)
        self.layout.addWidget(self.image_controller, 1, 0)


    # --------------------------------------------------------------------------

    def plot():
        """
        Plots specific image from dataset.
        """

        ...

# ==============================================================================

class ImagePlot(pg.ImageView):
    """
    Displays image.
    """

    def __init__(self, parent=None, view=None) -> None:
        super(ImagePlot, self).__init__(parent, view=pg.PlotItem())

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

# ==============================================================================

class ImageController(QtGui.QWidget):
    """
    Controllers image options, colormap.
    """

    def __init__(self, parent) -> None:
        super(ImageController, self).__init__(parent)
        self.main_window = parent



