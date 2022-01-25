"""
Displays views from arbitrary slices of a DataArray
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

class SlicingWidget(QtGui.QWidget):
    """
    Allows user to view arbitrary slices/linecuts of a DataArray
    """
    
    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(SlicingWidget, self).__init__(parent)

        self.parent = parent
        self.data_array = data_array
        
        # Custom layout
        self.layout = SlicingWidgetLayout(data_array, parent=self)
        self.setLayout(self.layout)

# ----------------------------------------------------------------------------------

class SlicingWidgetLayout(QtGui.QGridLayout):
    """
    Custom dynamic grid layout for slicing widget.

    WORKFLOW:
    2D: LineROI in ImageView -> 1D Plot
    3D: LineROI in ImageView -> 2D ImageView -> 1D Plot
    4D: LineROI in ImageView -> 3D ImageView w/ slider -> 2D ImageView -> 1D Plot
    """
    
    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(SlicingWidgetLayout, self).__init__(parent)

# ----------------------------------------------------------------------------------

