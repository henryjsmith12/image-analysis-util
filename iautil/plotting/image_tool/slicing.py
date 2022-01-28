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
        
        # Custom layout
        self.layout = SlicingWidgetLayout(data_array, parent=self)
        self.setLayout(self.layout)

# ----------------------------------------------------------------------------------

class SlicingWidgetLayout(QtGui.QVBoxLayout):
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

        if data_array.ndim >= 4:
            # 3D ImageView with slider
            # "Center ROI" button
            # "Change Color" button
            self.groupbx_4d = QtGui.QGroupBox("4D to 3D")
            self.groupbx_4d.setCheckable(True)
            self.image_view_4d = DataArrayImageView()
            self.center_btn_4d = QtGui.QPushButton("Center Line ROI")

            self.layout_4d = QtGui.QGridLayout()
            self.groupbx_4d.setLayout(self.layout_4d)
            self.layout_4d.addWidget(self.image_view_4d, 0, 0, 4, 6)
            self.layout_4d.addWidget(self.center_btn_4d, 4, 3, 1, 3)

            self.addWidget(self.groupbx_4d)

        if data_array.ndim >= 3:
            # 2D ImageView
            self.groupbx_3d = QtGui.QGroupBox("3D to 2D")
            self.groupbx_3d.setCheckable(True)
            self.image_view_3d = DataArrayImageView()
            self.center_btn_3d = QtGui.QPushButton("Center Line ROI")

            self.layout_3d = QtGui.QGridLayout()
            self.groupbx_3d.setLayout(self.layout_3d)
            self.layout_3d.addWidget(self.image_view_3d, 0, 0, 4, 6)
            self.layout_3d.addWidget(self.center_btn_3d, 4, 3, 1, 3)

            self.addWidget(self.groupbx_3d)

        if data_array.ndim >= 2:
            # 1D Plot
            self.groupbx_2d = QtGui.QGroupBox("2D to 1D")
            self.groupbx_2d.setCheckable(True)
            self.plot_2d = DataArrayPlot()
            self.center_btn_2d = QtGui.QPushButton("Center Line ROI")

            self.layout_2d = QtGui.QGridLayout()
            self.groupbx_2d.setLayout(self.layout_2d)
            self.layout_2d.addWidget(self.plot_2d, 0, 0, 4, 6)

            self.addWidget(self.groupbx_2d)

# ----------------------------------------------------------------------------------

app = pg.mkQApp()
slc = SlicingWidget(
    xr.DataArray(
        [[[1,2,3],
        [1,2,3],
        [1,2,3]],
        [[1,2,3],
        [1,2,3],
        [1,2,3]]]
    )
)

slc.show()
app.exec_()