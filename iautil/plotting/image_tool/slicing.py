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

        # ImageViews/Plot
        self.main_image_view = parent.main_image_view
        self.image_view_3d = DataArrayImageView()
        self.image_view_2d = DataArrayImageView()
        self.plot_1d = DataArrayPlot()

        # Slicing ROIs
        self.slicing_roi_4d = None
        self.slicing_roi_3d = None
        self.slicing_roi_2d = None

        if data_array.ndim == 4:
            self.slicing_roi_4d = SlicingROI(
                parent=self.main_image_view,
                child=self.image_view_3d
            )
            self.slicing_roi_3d = SlicingROI(
                parent=self.image_view_3d, 
                child=self.image_view_2d
            )
            self.slicing_roi_2d = SlicingROI(
                parent=self.image_view_2d, 
                child=self.plot_1d
            )
        if data_array.ndim == 3:
            self.slicing_roi_3d = SlicingROI(
                parent=self.main_image_view, 
                child=self.image_view_2d
            )
            self.slicing_roi_2d = SlicingROI(
                parent=self.image_view_2d, 
                child=self.plot_1d
            )
        if data_array.ndim == 2:
            self.slicing_roi_2d = SlicingROI(
                parent=self.main_image_view,  
                child=self.plot_1d
            )

        self.groupbox_3d = None
        self.groupbox_2d = None
        self.groupbox_1d = None

        if data_array.ndim >= 4:
            self.groupbox_3d = SlicingGroupBox(
                parent_roi=self.slicing_roi_4d,
                child_roi=self.slicing_roi_3d,
                child_gbx=self.groupbox_2d,
                image_view=self.image_view_3d,
                ndim=3
            )
            self.addWidget(self.groupbox_3d)
            self.setRowStretch(2, 1)

        if data_array.ndim >= 3:
            self.groupbox_2d = SlicingGroupBox(
                parent_roi=self.slicing_roi_3d,
                child_roi=self.slicing_roi_2d,
                parent_gbx=self.groupbox_3d,
                child_gbx=self.groupbox_1d,
                image_view=self.image_view_2d,
                ndim=2
            )
            self.addWidget(self.groupbox_2d)
            self.setRowStretch(1, 1)

        if data_array.ndim >= 2:
            self.groupbox_1d = SlicingGroupBox(
                parent_roi=self.slicing_roi_2d,
                parent_gbx=self.groupbox_2d,
                image_view=self.plot_1d,
                ndim=1
            )
            self.addWidget(self.groupbox_1d)
            self.setRowStretch(0, 1)

# ----------------------------------------------------------------------------------

class SlicingROI(pg.LineSegmentROI):
    
    def __init__(self, position=(0,0), parent=None, child=None) -> None:
        super(SlicingROI, self).__init__(position)

        self.parent = parent
        self.child = child

        self.parent.addItem(self)

        self.sigRegionChanged.connect(self.slice_data_array)

    # ------------------------------------------------------------------------------

    def slice_data_array(self):
        p_data_array = self.parent.data_array
        p_data_array_slice = self.parent.data_array_slice

        data, coords = self.getArrayRegion(
            data=p_data_array_slice,
            img=self.parent.getImageItem(),
            returnMappedCoords=True
        )
        x_coords, y_coords = coords.astype(int)

        for i in range(len(x_coords)):
            if x_coords[i] < 0:
                x_coords[i] = 0
            if x_coords[i] >= p_data_array.values.shape[0]:
                x_coords[i] = p_data_array.values.shape[0] - 1
        for i in range(len(y_coords)):
            if y_coords[i] < 0:
                y_coords[i] = 0
            if y_coords[i] >= p_data_array.values.shape[1]:
                y_coords[i] = p_data_array.values.shape[1] - 1

        c_data_array = xr.concat(
            [p_data_array[x, y] for x, y in zip(x_coords, y_coords)],
            f"{p_data_array.dims[0]}, {p_data_array.dims[1]}"
        )

        if c_data_array.ndim == 3:
            c_data_array_slice = c_data_array[:, :, 0]
        else:
            c_data_array_slice = c_data_array

        self.child.set_data_array_slice(
            c_data_array,
            c_data_array_slice
        )

   # ------------------------------------------------------------------------------

    def center(self):
        p_data_array = self.parent.data_array
        x_1 = p_data_array.coords[p_data_array.dims[0]].values[0]
        x_2 = p_data_array.coords[p_data_array.dims[0]].values[-1]
        y_1 = p_data_array.coords[p_data_array.dims[1]].values[0]
        y_2 = p_data_array.coords[p_data_array.dims[1]].values[-1]

        self.movePoint(self.getHandles()[0], (x_1, y_1))
        self.movePoint(self.getHandles()[1], (x_2, y_2))

# ----------------------------------------------------------------------------------

class SlicingGroupBox(QtGui.QGroupBox):

    def __init__(
        self, 
        parent_roi=None, 
        child_roi=None, 
        parent_gbx=None,
        child_gbx=None,
        image_view=None, 
        ndim=None
    ) -> None:
        super(SlicingGroupBox, self).__init__()

        self.parent_roi = parent_roi
        self.child_roi = child_roi
        self.data_array_image_view = image_view

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.slider_lbl = QtGui.QLabel()
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.enable_chkbx = QtGui.QCheckBox("Enable ROI")
        self.center_btn = QtGui.QPushButton("Center ROI")

        if ndim == 3:
            self.layout.addWidget(image_view, 0, 0, 4, 4)
            self.layout.addWidget(self.slider_lbl, 4, 0, 1, 1)
            self.layout.addWidget(self.slider, 4, 1, 1, 3)
            self.layout.addWidget(self.enable_chkbx, 5, 0)
            self.layout.addWidget(self.center_btn, 5, 1)
        else:
            self.layout.addWidget(image_view, 0, 0, 4, 4)
            self.layout.addWidget(self.enable_chkbx, 4, 0)
            self.layout.addWidget(self.center_btn, 4, 1)

        self.parent_roi.center()

        self.center_btn.clicked.connect(self.parent_roi.center)
        if self.child_roi is not None:
            self.parent_roi.sigRegionChanged.connect(self.child_roi.slice_data_array)

    # ------------------------------------------------------------------------------

    def _toggle_enabled(self):
        ...

    # ------------------------------------------------------------------------------

