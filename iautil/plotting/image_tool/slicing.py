"""
Displays views from arbitrary slices of a DataArray
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import xarray as xr

from iautil.utilities.ui import DataArrayImageView, DataArrayPlot

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

        self.main_image_view = parent.main_image_view
        self.image_view_4d, self.line_roi_4d = None, None
        self.image_view_3d, self.line_roi_3d = None, None
        self.plot_2d, self.line_roi_2d = None, None

        if data_array.ndim >= 4:
            # 3D ImageView with slider
            self.groupbx_4d = QtGui.QGroupBox("4D to 3D")
            self.groupbx_4d.setCheckable(True)
            self.image_view_4d = DataArrayImageView()
            self.line_roi_4d = pg.LineSegmentROI(positions=(0, 1))
            self.main_image_view.addItem(self.line_roi_4d)
            
            self.layout_4d = QtGui.QGridLayout()
            self.groupbx_4d.setLayout(self.layout_4d)
            self.layout_4d.addWidget(self.image_view_4d, 0, 0, 4, 6)
            
            self.addWidget(self.groupbx_4d)
            self.setRowStretch(2, 1)

        if data_array.ndim >= 3:
            # 2D ImageView
            self.groupbx_3d = QtGui.QGroupBox("3D to 2D")
            self.groupbx_3d.setCheckable(True)
            self.image_view_3d = DataArrayImageView()
            self.line_roi_3d = pg.LineSegmentROI(positions=(0, 1))
            if data_array.ndim > 3:
                self.image_view_4d.addItem(self.line_roi_3d)
            else:
                self.main_image_view.addItem(self.line_roi_3d)
            
            self.layout_3d = QtGui.QGridLayout()
            self.groupbx_3d.setLayout(self.layout_3d)
            self.layout_3d.addWidget(self.image_view_3d, 0, 0, 4, 6)
            
            self.addWidget(self.groupbx_3d)
            self.setRowStretch(1, 1)

        if data_array.ndim >= 2:
            # 1D Plot
            self.groupbx_2d = QtGui.QGroupBox("2D to 1D")
            self.groupbx_2d.setCheckable(True)
            self.plot_2d = DataArrayPlot()
            self.plot_2d.setBackground('default')
            self.line_roi_2d = pg.LineSegmentROI(positions=(0, 1))
            if data_array.ndim > 2:
                self.image_view_3d.addItem(self.line_roi_2d)
            else:
                self.main_image_view.addItem(self.line_roi_2d)

            self.layout_2d = QtGui.QGridLayout()
            self.groupbx_2d.setLayout(self.layout_2d)
            self.layout_2d.addWidget(self.plot_2d, 0, 0, 4, 6)

            self.addWidget(self.groupbx_2d)
            self.setRowStretch(0, 1)

# ----------------------------------------------------------------------------------