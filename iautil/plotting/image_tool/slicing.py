"""
Displays views from arbitrary slices of a DataArray
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from pyqtgraph import dockarea
from PyQt5 import QtGui, QtCore
import xarray as xr

from iautil.utilities.ui import DataArrayImageView, DataArrayPlot
from iautil.plotting.image_tool.controller import DimensionController

# ----------------------------------------------------------------------------------

class SlicingTab(QtGui.QWidget):
    """
    Houses SlicingWidgets
    """

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(SlicingTab, self).__init__(parent)
        
        self.parent = parent

        self.data_array = data_array

        # List of slicing widgets
        self.slicing_widgets = [
            SlicingWidget(i, parent=self) for i in range(data_array.ndim, 1, -1)
        ]

        # Sets parent ImageView for each ROI
        self.slicing_widgets[0].roi.set_parent_image_view(
            self.parent.data_array_image_view
        )
        for i in range(1, len(self.slicing_widgets)):
            self.slicing_widgets[i].roi.set_parent_image_view(
                self.slicing_widgets[i - 1].image_view
            )

        # Sets child ImageView for each ROI
        for i in range(len(self.slicing_widgets)):
            self.slicing_widgets[i].roi.set_child_image_view(
                self.slicing_widgets[i].image_view
            )

        # Sets child ROI
        for i in range(len(self.slicing_widgets) - 1):
            self.slicing_widgets[i].roi.set_child_roi(
                self.slicing_widgets[i + 1].roi
            )
    

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        for i in range(len(self.slicing_widgets)):
            self.layout.addWidget(self.slicing_widgets[i])
            self.layout.setRowStretch(i, 1)

# ----------------------------------------------------------------------------------

class SlicingWidget(dockarea.DockArea):

    def __init__(self, dim: int, parent) -> None:
        super(SlicingWidget, self).__init__(parent)
        
        self.parent = parent
        self.data_array = parent.data_array
        
        # Slicing ROI
        self.roi = SlicingROI()

        self.roi.parent = self

        # ImageView
        if dim > 2:
            self.image_view = DataArrayImageView()
        else:
            self.image_view = DataArrayPlot()
        self.image_view_dock = dockarea.Dock(
            name="ImageView",
            size=(200, 300),
            widget=self.image_view,
            hideTitle=True
        )

        # Controller
        self.controller = SlicingController(self)
        self.controller_dock = dockarea.Dock(
            name="Controller",
            size=(200, 100),
            widget=self.controller,
            hideTitle=True
        )

        # 4D->3D Slider
        if dim == 4:
            self.slider = DimensionController(
                data_array=self.parent.data_array, 
                dim=3
            )
            self.slider_dock = dockarea.Dock(
                name="Slider",
                size=(200, 100),
                widget=self.slider,
                hideTitle=True
            )

        # Dock layout
        self.addDock(self.controller_dock)
        self.addDock(self.image_view_dock, "right", 
            self.controller_dock)
        if dim == 4:
            self.addDock(self.slider_dock, "bottom", self.image_view_dock)

        self.controller.center_btn.clicked.connect(self.roi.center_roi)
        

# ----------------------------------------------------------------------------------

class SlicingController(QtGui.QWidget):

    def __init__(self, parent) -> None:
        super(SlicingController, self).__init__(parent)

        self.parent = parent
        self.data_array = parent.data_array

        self.center_btn = QtGui.QPushButton("Center ROI")
        self.export_btn = QtGui.QPushButton("Export Slice")

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.center_btn, 0, 0)
        #self.layout.addWidget(self.export_btn, 0, 1)

        '''
        for i in range(self.data_array.ndim):
            dim_lbl = QtGui.QLabel(self.data_array.dims[i])
            min_spbx = QtGui.QSpinBox()
            max_spbx = QtGui.QSpinBox()

            self.layout.addWidget(dim_lbl, i, 0)
            self.layout.addWidget(min_spbx, i, 1)
            self.layout.addWidget(max_spbx, i, 2)
        '''

        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

# ----------------------------------------------------------------------------------

class SlicingDimensionController(QtGui.QWidget):
    ...

# ----------------------------------------------------------------------------------

class SlicingROI(pg.LineSegmentROI):
    
    def __init__(self, position=(0,0)) -> None:
        super(SlicingROI, self).__init__(position)

        self.parent = None

        self.parent_imv, self.child_imv = None, None
        self.child_roi = None, None

        self.sigRegionChanged.connect(self.slice_data_array)

    # ------------------------------------------------------------------------------

    def set_parent_image_view(self, image_view):
        self.parent_imv = image_view
        self.parent_imv.addItem(self)

    # ------------------------------------------------------------------------------

    def set_child_image_view(self, image_view):
        self.child_imv = image_view

    # ------------------------------------------------------------------------------

    def set_child_roi(self, roi):
        self.child_roi = roi
        self.sigRegionChangeFinished.connect(
            self.child_roi.slice_data_array
        )

    # ------------------------------------------------------------------------------

    def slice_data_array(self):
        p_data_array = self.parent_imv.data_array
        p_data_array_slice = self.parent_imv.data_array_slice

        data, coords = self.getArrayRegion(
            data=p_data_array_slice,
            img=self.parent_imv.getImageItem(),
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
            c_data_array_slice = c_data_array[
                :, :, self.parent.slider.value_slider.value()
            ]
        else:
            c_data_array_slice = c_data_array

        self.child_imv.set_data_array_slice(
            c_data_array,
            c_data_array_slice
        )

    # ------------------------------------------------------------------------------

    def center_roi(self):

        p_data_array = self.parent_imv.data_array
        x_1 = p_data_array.coords[p_data_array.dims[0]].values[0]
        x_2 = p_data_array.coords[p_data_array.dims[0]].values[-1]
        y_1 = p_data_array.coords[p_data_array.dims[1]].values[0]
        y_2 = p_data_array.coords[p_data_array.dims[1]].values[-1]

        self.movePoint(self.getHandles()[0], (x_1, y_1))
        self.movePoint(self.getHandles()[1], (x_2, y_2))

# ----------------------------------------------------------------------------------