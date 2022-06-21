"""
Displays views from arbitrary slices of a DataArray
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from pyqtgraph import dockarea
from PyQt5 import QtGui, QtCore
import xarray as xr

from iautil import io
from iautil.utilities.ui import DataArrayImageView, DataArrayPlot
from iautil.plotting.image_tool.controller import DimensionController

# ----------------------------------------------------------------------------------

class ROITab(QtGui.QWidget):
    """
    
    """

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(ROITab, self).__init__(parent)
        
        self.parent = parent
        self.data_array = data_array

        self.roi_widgets = [ROIWidget(self, data_array) for i in range(4)]

        self.tab_widget = QtGui.QTabWidget()
        
        for i in range(len(self.roi_widgets)):
            self.tab_widget.addTab(self.roi_widgets[i], f"ROI #{i + 1}")

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)

# ----------------------------------------------------------------------------------

class ROIWidget(dockarea.DockArea):
    
    def __init__(self, tab, data_array) -> None:
        super(ROIWidget, self).__init__()

        # Parent tab and DataArrayController from overall ImageTool
        self.tab = tab
        self.main_controller = tab.parent.data_array_controller
        
        self.data_array = data_array

        # Creates SlicingROI
        self.roi = ROI()
        self.roi.hide()
        self.roi.roi_widget = self
        self.roi.parent_imv = tab.parent.data_array_image_view
        self.roi.parent_imv.addItem(self.roi)

        self.controller = ROIController(self, self.data_array)
        self.roi_image_view = ROIImageView(self)

        # Docks
        self.controller_dock = dockarea.Dock(
            name="Controller",
            size=(200, 100),
            widget=self.controller,
            hideTitle=True
        )
        self.roi_image_view_dock = dockarea.Dock(
            name="Image View",
            size=(200, 100),
            widget=self.roi_image_view,
            hideTitle=True
        )
        
        # Dock layout
        self.addDock(self.controller_dock)
        self.addDock(self.roi_image_view_dock, "bottom", self.controller_dock)
        
# ----------------------------------------------------------------------------------

class ROI(pg.RectROI):
    
    def __init__(self, position=(0,0), size=(1,1), parent=None) -> None:
        super(ROI, self).__init__(position, size)
        
        self.roi_widget = None

# ----------------------------------------------------------------------------------

class ROIController(QtGui.QWidget):

    def __init__(self, roi_widget, data_array) -> None:
            super(ROIController, self).__init__(roi_widget)

# ----------------------------------------------------------------------------------

class ROIImageView(DataArrayImageView):
    
    def __init__(self, parent=None) -> None:
        super(ROIImageView, self).__init__(
            parent
        )

# ----------------------------------------------------------------------------------

class ROIPlot():
    ...

# ----------------------------------------------------------------------------------