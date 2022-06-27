"""
Displays  of a DataArray
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
        self.main_image_view = tab.parent.data_array_image_view
        
        self.data_array = data_array

        self.roi = ROI(parent=self, image_view=self.main_image_view)
        self.roi.removeHandle(0)
        self.controller = ROIController(parent=self, data_array=self.data_array)
        self.roi_image_view = ROIImageView(parent=self, data_array=self.data_array)

        # Docks
        self.controller_dock = dockarea.Dock(
            name="Controller",
            size=(100, 20),
            widget=self.controller,
            hideTitle=True
        )
        self.roi_image_view_dock = dockarea.Dock(
            name="Image View",
            size=(100, 200),
            widget=self.roi_image_view,
            hideTitle=True
        )
        
        # Dock layout
        self.addDock(self.controller_dock)
        self.addDock(self.roi_image_view_dock, "bottom", self.controller_dock)
        
# ----------------------------------------------------------------------------------

class ROI(pg.RectROI):
    
    def __init__(self, position=(0,0), size=(1,1), parent=None, image_view=None) -> None:
        super(ROI, self).__init__(position, size)
        
        self.parent = parent
        self.image_view = image_view

        self.addTranslateHandle(pos=(0.5, 0.5))
        self.addScaleHandle(pos=(0, 0.5), center=(0.5, 0.5))
        self.addScaleHandle(pos=(1, 0.5), center=(0.5, 0.5))
        self.addScaleHandle(pos=(0.5, 0), center=(0.5, 0.5))
        self.addScaleHandle(pos=(0.5, 1), center=(0.5, 0.5))
        
        self.hide()
        if type(self.image_view) == DataArrayImageView:
            self.image_view.addItem(self)

        self.sigRegionChanged.connect(self.get_data_array_region)

    # ------------------------------------------------------------------------------

    def get_data_array_region(self):

        data_array = self.image_view.data_array
        data_array_slice = self.image_view.data_array_slice

        data, coords = self.getArrayRegion(
            data=data_array_slice,
            img=self.image_view.getImageItem(),
            returnMappedCoords=True
        )
        print(coords[0][25][25])

        x_coords, y_coords = coords

        x_1 = x_coords[0][0]
        x_2 = x_coords[-1][-1]
        y_1 = y_coords[0][0]
        y_2 = y_coords[-1][-1]

        h = self.image_view.getImageItem().mapFromData(QtCore.QPoint(0,0)) 

        pg.ImageItem.mapFromData
        print(h)
        avgs = []
        '''for i in range(data_array.shape[2]):
            for j in range(data_array.shape[3]):
                avg = data_array[x_1:x_2, y_1:y_2, i, j].shape
                #print(avg)'''

        #data_array_slice = data_array[x_1:x_2,y_1:y_2]

        '''self.parent.roi_image_view.set_data_array_slice(
            data_array,
            data_array_slice
        )'''

    # ------------------------------------------------------------------------------

    def center(self):
        """
        Centers ROI.
        """
        data_array = self.image_view.data_array
        x_1 = data_array.coords[data_array.dims[0]].values[0]
        x_2 = data_array.coords[data_array.dims[0]].values[-1]
        y_1 = data_array.coords[data_array.dims[1]].values[0]
        y_2 = data_array.coords[data_array.dims[1]].values[-1]

        self.movePoint(self.getHandles()[0], ((x_1 + x_2)/2, (y_1+y_2)/2))
        self.movePoint(self.getHandles()[1], (x_1, (y_1+y_2)/2))
        self.movePoint(self.getHandles()[2], (x_2, (y_1+y_2)/2))
        self.movePoint(self.getHandles()[3], ((x_1 + x_2)/2, y_1))
        self.movePoint(self.getHandles()[4], ((x_1 + x_2)/2, y_2))

# ----------------------------------------------------------------------------------

class ROIController(QtGui.QWidget):

    def __init__(self, parent=None, data_array=None) -> None:
        super(ROIController, self).__init__()

        self.parent = parent
        self.data_array = data_array

        self.width_lbl = QtGui.QLabel("Width")
        self.center_px_lbl = QtGui.QLabel("Center")
        self.dim_1_lbl = QtGui.QLabel()
        self.dim_1_width_sbx = QtGui.QDoubleSpinBox()
        self.dim_1_center_cbx = QtGui.QComboBox()
        self.dim_2_lbl = QtGui.QLabel()
        self.dim_2_width_sbx = QtGui.QDoubleSpinBox()
        self.dim_2_center_cbx = QtGui.QComboBox()
        self.enable_chkbx = QtGui.QCheckBox("Enable")
        self.center_btn = QtGui.QPushButton("Center ROI")

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.width_lbl, 0, 1)
        self.layout.addWidget(self.center_px_lbl, 0, 2)
        self.layout.addWidget(self.dim_1_lbl, 1, 0)
        self.layout.addWidget(self.dim_1_width_sbx, 1, 1)
        self.layout.addWidget(self.dim_1_center_cbx, 1, 2)
        self.layout.addWidget(self.dim_2_lbl, 2, 0)
        self.layout.addWidget(self.dim_2_width_sbx, 2, 1)
        self.layout.addWidget(self.dim_2_center_cbx, 2, 2)
        self.layout.addWidget(self.enable_chkbx, 3, 0)
        self.layout.addWidget(self.center_btn, 3, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 2)
        self.layout.setRowStretch(2, 2)
        self.layout.setRowStretch(3, 2)

        self.enable_chkbx.stateChanged.connect(self.toggle_enabled)
        self.center_btn.clicked.connect(self.parent.roi.center)

    # ------------------------------------------------------------------------------

    def toggle_enabled(self):
        if self.enable_chkbx.isChecked():
            self.enable()
        else:
            self.disable()

    # ------------------------------------------------------------------------------

    def enable(self):
        self.enabled = True

        self.parent.roi.show()
        self.parent.roi.center()

    # ------------------------------------------------------------------------------

    def disable(self):
        self.enabled = False

        self.parent.roi_image_view.clear()
        self.parent.roi.hide()

# ----------------------------------------------------------------------------------

class ROIImageView(DataArrayImageView):

    def __init__(self, parent=None, data_array=None) -> None:
        super(ROIImageView, self).__init__(parent)

# ----------------------------------------------------------------------------------

class ROIPlot(DataArrayPlot):

    def __init__(self, parent=None, data_array=None, plotItem=None) -> None:
        super(ROIPlot, self).__init__(parent, plotItem)

# ----------------------------------------------------------------------------------
