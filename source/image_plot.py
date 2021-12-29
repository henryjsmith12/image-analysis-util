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

class ImagePlot(pg.ImageView):
    """
    Displays image.
    """

    def __init__(self, parent=None, view=None) -> None:
        super(ImagePlot, self).__init__(parent, view=pg.PlotItem())
        self.main_window = parent

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
    
    # --------------------------------------------------------------------------

    def plot(self):
        """
        Plots specific image from dataset.
        """

        ...