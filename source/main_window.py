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
from pyqtgraph.dockarea import *

from source.image_plot import ImagePlot
from source.image_controller import ImageController

# ==============================================================================

class MainWindow(QtGui.QWidget):
    """
    Houses widgets for analysis window
    """

    def __init__(self, file_path) -> None:
        super().__init__()

        # Class Variables 
        self.file_path = file_path

        # Subwidgets
        self.dock_area = DockArea()

        # Layout
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.dock_area)

        self.createWidgets()
        self.createWidgetDocks()

    # --------------------------------------------------------------------------

    def createWidgets(self):
        """
        
        """

        self.image_plot = ImagePlot(self)
        self.image_controller = ImageController(self)

    # --------------------------------------------------------------------------

    def createWidgetDocks(self):
        """
        
        """

        self.image_plot_dock = Dock("ImagePlot", size=(100, 100), hideTitle=True)
        self.image_controller_dock = Dock("ImageController", size=(100, 100), hideTitle=True)

        # Adds widgets to docks
        self.image_plot_dock.addWidget(self.image_plot)
        self.image_controller_dock.addWidget(self.image_controller)

        # Adds docks to dock area
        self.dock_area.addDock(self.image_plot_dock)
        self.dock_area.addDock(self.image_controller_dock, "bottom", self.image_plot_dock)