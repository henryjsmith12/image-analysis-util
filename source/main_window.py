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

from source.image_controller import *
from source.image_plot import *
from source.roi import *
from source.slicing import *

# ==============================================================================

class MainWindow(QtGui.QWidget):
    """
    Houses widgets for analysis window
    """

    def __init__(self, file_path) -> None:
        super().__init__()

        self.resize(1200, 800)

        self.file_path = file_path
        self.data = None
        self.axes = None
        self.axis_labels = None
        
        # Subwidgets
        self.dock_area = DockArea()

        # Layout
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.dock_area)

        self.readFile()
        self.createWidgets()
        self.createWidgetDocks()

    # --------------------------------------------------------------------------

    def readFile(self):
        """
        Reads information from .iau file.
        """

        with h5py.File(self.file_path, 'r') as file:
            self.data = file["data"][...]
            self.axes = [dim[0][...].tolist() for dim in file["data"].dims]
            self.axis_labels = [dim.label for dim in file["data"].dims]
            
    # --------------------------------------------------------------------------

    def createWidgets(self):
        """
        Instantiates widgets used in main window.
        """

        self.image_plot = ImagePlot(self)
        self.image_controller = ImageController(self)
        self.roi_window = ROIWindow(self)
        self.slicing_window = SlicingWindow(self)

    # --------------------------------------------------------------------------

    def createWidgetDocks(self):
        """
        - Creates docks, 
        - Adds instantiated widgets to docks,
        - Adds docks to dock area.
        """

        self.image_plot_dock = Dock("ImagePlot", size=(100, 100), hideTitle=True)
        self.image_controller_dock = Dock("ImageController", size=(100, 100), hideTitle=True)
        self.roi_window_dock = Dock("ROI", size=(100, 200))
        self.slicing_window_dock = Dock("Slicing", size=(100, 200))

        # Adds widgets to docks
        self.image_plot_dock.addWidget(self.image_plot)
        self.image_controller_dock.addWidget(self.image_controller)
        self.roi_window_dock.addWidget(self.roi_window)
        self.slicing_window_dock.addWidget(self.slicing_window)

        # Adds docks to dock area
        self.dock_area.addDock(self.image_plot_dock)
        self.dock_area.addDock(self.slicing_window_dock, "right", self.image_plot_dock)
        self.dock_area.addDock(self.roi_window_dock, "above", self.slicing_window_dock)
        self.dock_area.addDock(self.image_controller_dock, "bottom", self.image_plot_dock)
        