"""
Displays views from arbitrary slices of a DataArray
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import xarray as xr

from iautil.utilities.ui import DataArrayImageView, DataArrayPlot, SlicingROI

# ----------------------------------------------------------------------------------

class SlicingWidget(QtGui.QWidget):
    """
    Allows user to view arbitrary slices/linecuts of a DataArray
    """
    
    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(SlicingWidget, self).__init__(parent)

        self.parent = parent
        self.data_array = data_array
        self.main_image_view = parent.data_array_image_view
        
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

    Planning to add 3 separate groupboxes (1 gbx for every degree of slicing)
    """
    
    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(SlicingWidgetLayout, self).__init__(parent)

        # ImageViews/Plot
        self.main_image_view = parent.main_image_view
        self.image_view_3d = DataArrayImageView()
        self.image_view_2d = DataArrayImageView()
        self.plot_1d = DataArrayPlot()

        # Slicing ROIs
        self.slicing_roi_4d_3d = None
        self.slicing_roi_3d_2d = None
        self.slicing_roi_2d_1d = None

        if data_array.ndim == 4:
            self.slicing_roi_4d_3d = SlicingROI(
                parent=self.main_image_view,
                child=self.image_view_3d
            )
            self.slicing_roi_3d_2d = SlicingROI(
                parent=self.image_view_3d, 
                child=self.image_view_2d
            )
            self.slicing_roi_2d_1d = SlicingROI(
                parent=self.image_view_2d, 
                child=self.plot_1d
            )
        if data_array.ndim == 3:
            self.slicing_roi_3d_2d = SlicingROI(
                parent=self.main_image_view, 
                child=self.image_view_2d
            )
            self.slicing_roi_2d_1d = SlicingROI(
                parent=self.image_view_2d, 
                child=self.plot_1d
            )
        if data_array.ndim == 2:
            self.slicing_roi_2d_1d = SlicingROI(
                parent=self.main_image_view,  
                child=self.plot_1d
            )

        # Populates GroupBoxes
        self.groupbox_3d, self.layout_3d = None, None
        self.groupbox_2d, self.layout_2d = None, None
        self.groupbox_1d, self.layout_1d = None, None

        if data_array.ndim >= 4:
            self.groupbx_3d = QtGui.QGroupBox("4D to 3D")
            self.layout_3d = QtGui.QGridLayout()
            self.groupbx_3d.setLayout(self.layout_3d)
            self.layout_3d.addWidget(self.image_view_3d)
            self.addWidget(self.groupbx_3d)
            self.setRowStretch(2, 1)

        if data_array.ndim >= 3:
            self.groupbx_2d = QtGui.QGroupBox("3D to 2D")
            self.layout_2d = QtGui.QGridLayout()
            self.groupbx_2d.setLayout(self.layout_2d)
            self.layout_2d.addWidget(self.image_view_2d)
            self.addWidget(self.groupbx_2d)
            self.setRowStretch(1, 1)

        if data_array.ndim >= 2:
            self.groupbx_1d = QtGui.QGroupBox("2D to 1D")
            self.layout_1d = QtGui.QGridLayout()
            self.groupbx_1d.setLayout(self.layout_1d)
            self.layout_1d.addWidget(self.plot_1d)
            self.addWidget(self.groupbx_1d)
            self.setRowStretch(0, 1)

# ----------------------------------------------------------------------------------