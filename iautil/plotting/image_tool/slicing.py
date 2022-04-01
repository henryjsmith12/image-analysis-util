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

class SlicingTab(QtGui.QWidget):
    """
    Houses SlicingWidget objects.
    """

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(SlicingTab, self).__init__(parent)
        
        self.parent = parent
        self.data_array = data_array

        # List of SlicingWidget objects housed in tab
        self.slicing_widgets = [
            SlicingWidget(i, self, data_array) for i in range(data_array.ndim, 1, -1)
        ]

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        # Connects each SlicingWidget to a parent and child SlicingWidget
        # Then adds SlicingWidget to layout
        for i in range(len(self.slicing_widgets)):
            if i == 0:
                self.slicing_widgets[i].set_parent(self.parent.data_array_image_view)
                if len(self.slicing_widgets) > 1:
                    self.slicing_widgets[i].set_child(self.slicing_widgets[i + 1])
            elif i == len(self.slicing_widgets) - 1:
                self.slicing_widgets[i].set_parent(self.slicing_widgets[i - 1])
                self.slicing_widgets[i].roi.parent_roi = self.slicing_widgets[i - 1].roi
            else:
                self.slicing_widgets[i].set_parent(self.slicing_widgets[i - 1])
                self.slicing_widgets[i].set_child(self.slicing_widgets[i + 1])
                self.slicing_widgets[i].roi.parent_roi = self.slicing_widgets[i - 1].roi

            self.slicing_widgets[i].roi.child_imv = self.slicing_widgets[i].image_view

            # Initially disables SlicingWidget
            self.slicing_widgets[i].disable()

            self.layout.addWidget(self.slicing_widgets[i])
            self.layout.setRowStretch(i, 1)

# ----------------------------------------------------------------------------------

class SlicingWidget(dockarea.DockArea):
    """
    A widget that visualizes a slice of the overall DataArray.
    """

    def __init__(self, dim: int, tab, data_array) -> None:
        super(SlicingWidget, self).__init__()
        
        # Parent tab and DataArrayController from overall ImageTool
        self.tab = tab
        self.main_controller = tab.parent.data_array_controller
        
        # Set to non-None values in SlicingTab constructor
        self.parent, self.child = None, None
        self.data_array = data_array

        # Creates SlicingROI
        self.roi = SlicingROI()
        self.roi.slicing_widget = self

        # ImageView and SlicingController creation based on dimension of DataArray
        if dim == 2:
            self.image_view = DataArrayPlot()
            self.controller = SlicingController(self, data_array)
            self.controller.layout.addWidget(self.controller.export_btn, 1, 2)
        elif dim == 3:
            self.image_view = DataArrayImageView()
            self.controller = SlicingController(self, data_array)
            self.controller.layout.addWidget(self.controller.export_btn, 1, 2)
        elif dim == 4:
            self.image_view = DataArrayImageView()
            self.controller = SlicingController(self, data_array)
            self.slider = DimensionController(data_array, 3, self.main_controller)
            
        # Docks
        self.image_view_dock = dockarea.Dock(
            name="ImageView",
            size=(200, 300),
            widget=self.image_view,
            hideTitle=True
        )
        self.controller_dock = dockarea.Dock(
            name="Controller",
            size=(200, 100),
            widget=self.controller,
            hideTitle=True
        )
        if dim == 4:
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

        # Connections
        self.controller.center_btn.clicked.connect(self.roi.center)
        self.controller.export_btn.clicked.connect(self.export)
        self.controller.enable_chkbx.stateChanged.connect(self.toggle_enabled)
        if dim == 4:
            self.main_controller.updated.connect(
                lambda: self.slider.set_dimension(3)
            )
            self.slider.updated.connect(
                self.roi.slice_data_array
            )
        
    # ------------------------------------------------------------------------------

    def set_parent(self, parent):
        """
        Sets parent SlicingWidget and connects the ROI
        """
        self.parent = parent

        if isinstance(parent, DataArrayImageView):
            self.roi.parent_imv = parent
        if isinstance(parent, SlicingWidget):
            self.roi.parent_imv = parent.image_view

        self.roi.parent_imv.addItem(self.roi)
        self.roi.sigRegionChanged.connect(self.roi.slice_data_array)

    # ------------------------------------------------------------------------------

    def set_child(self, child):
        """
        Sets child SlicingWidget and connects the ROI
        """
        self.child = child

        self.roi.child_roi = child.roi
        self.roi.sigRegionChanged.connect(self.roi.child_roi.slice_data_array)

    # ------------------------------------------------------------------------------

    def toggle_enabled(self):
        """
        Calls function to enable/disable SlicingWidget
        """
        if self.controller.enable_chkbx.isChecked():
            self.enable()
        else:
            self.disable()

    # ------------------------------------------------------------------------------

    def enable(self):
        """
        Enable SlicingWidget and enables "Enable" checkbox for child widget
        """
        self.enabled = True

        self.image_view.setEnabled(True)
        self.roi.show()
        self.roi.center()
        self.roi.center()
        self.controller.roi_controller.setEnabled(True)

        if self.child is not None:
            self.child.controller.setEnabled(True)

    # ------------------------------------------------------------------------------

    def disable(self):
        """
        Disables SlicingWidget and child widget
        """
        self.enabled = False

        self.image_view.clear()
        self.image_view.setEnabled(False)
        self.roi.hide()
        self.controller.roi_controller.setEnabled(False)
        
        if self.child is not None:
            self.child.controller.enable_chkbx.setChecked(False)
            self.child.controller.setEnabled(False)

    # ------------------------------------------------------------------------------

    def export(self):
        data = self.image_view.data_array.values
        coords = []
        labels = []

        for dim_ctrl in self.controller.roi_controller.dim_ctrls:
            coords.append(dim_ctrl.used_coords)
            labels.append(dim_ctrl.dim_lbl.text())

        export_dialog = SlicingExportDialog()
        export_dialog.exec_()

        if export_dialog is not None:
            if export_dialog.format == ".csv":
                io.create_csv(data, coords, labels, export_dialog.path)

# ----------------------------------------------------------------------------------

class SlicingExportDialog(QtGui.QDialog):

    def __init__ (self):
        super().__init__()

        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.format_lbl = QtGui.QLabel("Format:")
        self.format_cbx = QtGui.QComboBox()
        self.format_cbx.addItems([".csv"])
        self.dialog_btnbox = QtGui.QDialogButtonBox()
        self.dialog_btnbox.addButton("OK", QtGui.QDialogButtonBox.AcceptRole)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.format_lbl, 0, 0)
        self.layout.addWidget(self.format_cbx, 0, 1)
        self.layout.addWidget(self.dialog_btnbox, 1, 1)

        self.dialog_btnbox.accepted.connect(self.accept)

    # --------------------------------------------------------------------------

    def accept(self):

        """
        Sets class variables to values in dialog and closes the dialog window.
        """

        self.format = self.format_cbx.currentText()
        self.path = QtGui.QFileDialog.getSaveFileName(self, "", "", f"(*{self.format})")[0]
        self.close()

# ----------------------------------------------------------------------------------

class SlicingROI(pg.LineSegmentROI):
    """
    Custom LineSegmentROI to be used within a SlicingWidget
    """
    
    def __init__(self, position=(0,0), parent=None) -> None:
        super(SlicingROI, self).__init__(position)
        
        self.parent_imv, self.child_imv = None, None
        self.parent_roi, self.child_roi = None, None
        self.slicing_widget = None
        
    # ------------------------------------------------------------------------------

    def slice_data_array(self):
        """
        Creates new DataArray from slice coordinates and displays in ImageView
        """
        if self.slicing_widget.enabled:
            # DataArray and slice from parent ImageView
            p_data_array = self.parent_imv.data_array
            p_data_array_slice = self.parent_imv.data_array_slice

            # Slicing coords
            data, coords = self.getArrayRegion(
                data=p_data_array_slice,
                img=self.parent_imv.getImageItem(),
                returnMappedCoords=True
            )
            x_coords, y_coords = coords.astype(int)

            # For coordinate indicies outside those of image
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
            self.coords = x_coords, y_coords

            # Creates child data array from coords
            c_data_array = xr.concat(
                [p_data_array[x, y] for x, y in zip(x_coords, y_coords)],
                f"{p_data_array.dims[0]}, {p_data_array.dims[1]}"
            )

            # Takes slice
            if c_data_array.ndim == 3:
                # 3D slice based off slider value
                c_data_array_slice = c_data_array[
                    :, :, self.slicing_widget.slider.value_slider.value()
                ]
            else:
                c_data_array_slice = c_data_array

            self.child_imv.set_data_array_slice(
                c_data_array,
                c_data_array_slice
            )  

            # Updates ROIController
            self.slicing_widget.controller.roi_controller.update_controller()

    # ------------------------------------------------------------------------------

    def center(self):
        """
        Centers ROI.
        """
        p_data_array = self.parent_imv.data_array
        x_1 = p_data_array.coords[p_data_array.dims[0]].values[0]
        x_2 = p_data_array.coords[p_data_array.dims[0]].values[-1]
        y_1 = p_data_array.coords[p_data_array.dims[1]].values[0]
        y_2 = p_data_array.coords[p_data_array.dims[1]].values[-1]

        self.movePoint(self.getHandles()[0], (x_1, y_1))
        self.movePoint(self.getHandles()[1], (x_2, y_2))

    # ------------------------------------------------------------------------------

    def move(self, x_1, x_2, y_1, y_2):
        """
        Moves ROI to specific location.
        """
        self.movePoint(self.getHandles()[0], (x_1, y_1))
        self.movePoint(self.getHandles()[1], (x_2, y_2))

# ----------------------------------------------------------------------------------

class SlicingController(QtGui.QWidget):
    """
    Houses an ROIController, and various options for SlicingWidget
    """

    def __init__(self, slicing_widget, data_array) -> None:
        super(SlicingController, self).__init__(slicing_widget)

        self.slicing_widget = slicing_widget

        self.roi_controller = SlicingROIController(data_array, self)
        self.enable_chkbx = QtGui.QCheckBox("Enable")
        self.center_btn = QtGui.QPushButton("Center")
        self.export_btn = QtGui.QPushButton("Export")

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        # Add widgets to layout
        self.layout.addWidget(self.roi_controller, 0, 0, 1, 3)
        self.layout.addWidget(self.enable_chkbx, 1, 0)
        self.layout.addWidget(self.center_btn, 1, 1)
        #self.layout.addWidget(self.export_btn, 1, 2)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.setRowStretch(0, 6)
        self.layout.setRowStretch(1, 1)

# ----------------------------------------------------------------------------------

class SlicingROIController(QtGui.QWidget):
    """
    Houses coordinate bounds for each dimension of ROI
    """

    def __init__(self, data_array, parent=None) -> None:
        super(SlicingROIController, self).__init__()

        self.parent = parent
        self.roi = self.parent.slicing_widget.roi
        self.main_controller = self.parent.slicing_widget.main_controller

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.dim_ctrls = []
        for i in range(data_array.ndim):
            self.dim_ctrls.append(SlicingROIDimensionController(self))

            self.layout.addWidget(self.dim_ctrls[i], i, 0)

        self.main_controller.updated.connect(self.set_dimension_order)
        self.roi.sigRegionChanged.connect(self.update_controller)

        self.updating = None

        self.set_dimension_order()

    # ------------------------------------------------------------------------------

    def set_dimension_order(self):
        """ 
        Sets new dimension order for slice
        """
        self.data_array = self.main_controller.data_array
        
        for i in range(self.data_array.ndim):
            self.dim_ctrls[i].set_dimension(i)

        self.update_controller()    

    # ------------------------------------------------------------------------------

    def update_controller(self):
        """
        Sets dimension bounds in controller
        """
        try:
            if self.updating == "ROI":
                return  

            self.updating = "Controller"

            self.data_array = self.main_controller.data_array
            slice_degree = self.data_array.ndim - self.roi.parent_imv.data_array.ndim

            if slice_degree == 0:
                self.dim_ctrls[0].set_dimension(
                    0, 
                    indices=self.roi.coords[0]
                )
                self.dim_ctrls[1].set_dimension(
                    1, 
                    indices=self.roi.coords[1]
                )
                for i in range(2, self.data_array.ndim):
                    self.dim_ctrls[i].setEnabled(False)

            elif slice_degree == 1:
                x1_indicies = self.roi.parent_roi.coords[0]
                x2_indicies = self.roi.parent_roi.coords[1]
                y_indicies = self.roi.coords[1]

                self.dim_ctrls[0].set_dimension(
                    0, 
                    coords=[self.data_array.coords[self.data_array.dims[0]].values[i] for i in x1_indicies],
                    indices=self.roi.coords[0]
                )
                self.dim_ctrls[1].set_dimension(
                    1, 
                    coords=[self.data_array.coords[self.data_array.dims[1]].values[i] for i in x2_indicies],
                    indices=self.roi.coords[0]
                )
                self.dim_ctrls[2].set_dimension(
                    2, 
                    indices=self.roi.coords[1]
                )
                for i in range(3, self.data_array.ndim):
                    self.dim_ctrls[i].setEnabled(False)
                
            elif slice_degree == 2:
                x1_indicies = [self.roi.parent_roi.parent_roi.coords[0][i] for i in self.roi.parent_roi.coords[0]]
                x2_indicies = [self.roi.parent_roi.parent_roi.coords[1][i] for i in self.roi.parent_roi.coords[0]]
                x3_indicies = self.roi.parent_roi.coords[1]
                y_indicies = self.roi.coords[1]

                self.dim_ctrls[0].set_dimension(
                    0, 
                    coords=[self.data_array.coords[self.data_array.dims[0]].values[i] for i in x1_indicies],
                    indices=self.roi.coords[0]
                )
                self.dim_ctrls[1].set_dimension(
                    1, 
                    coords=[self.data_array.coords[self.data_array.dims[1]].values[i] for i in x2_indicies],
                    indices=self.roi.coords[0]
                )
                self.dim_ctrls[2].set_dimension(
                    2, 
                    coords=[self.data_array.coords[self.data_array.dims[2]].values[i] for i in x3_indicies],
                    indices=self.roi.coords[0]
                )
                self.dim_ctrls[3].set_dimension(
                    3, 
                    indices=self.roi.coords[1]
                )

            self.updating = None
        except:
            ...

    # ------------------------------------------------------------------------------

    def update_roi(self, dim: int):
        """
        Sets ROI location based on changes in the SlicingROIDimensionControllers
        """
        try:
            if self.updating == "Controller":
                return  

            def _is_monotonic(values: list) -> bool:
                """
                Checks list for monoticity.
                """
                # Differentiated list
                dx = np.diff(values)

                return np.all(dx <= 0) or np.all(dx >= 0)

            self.data_array = self.main_controller.data_array
            slice_degree = self.data_array.ndim - self.roi.parent_imv.data_array.ndim

            p_data_array = self.roi.parent_imv.data_array
            
            x_1_index = self.dim_ctrls[0].endpoint_1_cbx.currentIndex()
            x_2_index = self.dim_ctrls[0].endpoint_2_cbx.currentIndex()

            if slice_degree == 0:
                y_1_index = self.dim_ctrls[1].endpoint_1_cbx.currentIndex()
                y_2_index = self.dim_ctrls[1].endpoint_2_cbx.currentIndex()
                for i in range(2, self.data_array.ndim):
                    self.dim_ctrls[i].setEnabled(False)

            elif slice_degree == 1:
                if dim == 1:
                    x_1_index = self.dim_ctrls[1].endpoint_1_cbx.currentIndex()
                    x_2_index = self.dim_ctrls[1].endpoint_2_cbx.currentIndex()
                y_1_index = self.dim_ctrls[2].endpoint_1_cbx.currentIndex()
                y_2_index = self.dim_ctrls[2].endpoint_2_cbx.currentIndex()
                for i in range(3, self.data_array.ndim):
                    self.dim_ctrls[i].setEnabled(False)

            elif slice_degree == 2:
                if dim == 1:
                    x_1_index = self.dim_ctrls[1].endpoint_1_cbx.currentIndex()
                    x_2_index = self.dim_ctrls[1].endpoint_2_cbx.currentIndex()
                if dim == 2:
                    x_1_index = self.dim_ctrls[1].endpoint_1_cbx.currentIndex()
                    x_2_index = self.dim_ctrls[1].endpoint_2_cbx.currentIndex()
                y_1_index = self.dim_ctrls[3].endpoint_1_cbx.currentIndex()
                y_2_index = self.dim_ctrls[3].endpoint_2_cbx.currentIndex()

            if _is_monotonic(p_data_array.coords[p_data_array.dims[0]].values):
                x_1 = p_data_array.coords[p_data_array.dims[0]].values[x_1_index]
                x_2 = p_data_array.coords[p_data_array.dims[0]].values[x_2_index]
            else:
                x_1 = x_1_index
                x_2 = x_2_index

            if _is_monotonic(p_data_array.coords[p_data_array.dims[1]].values):
                y_1 = p_data_array.coords[p_data_array.dims[1]].values[y_1_index]
                y_2 = p_data_array.coords[p_data_array.dims[1]].values[y_2_index]
            else:
                y_1 = y_1_index
                y_2 = y_2_index

            self.roi.move(x_1, x_2, y_1, y_2)

            self.updating = None
        except:
            ...

# ----------------------------------------------------------------------------------

class SlicingROIDimensionController(QtGui.QWidget):

    def __init__(self, parent=None) -> None:
        super(SlicingROIDimensionController, self).__init__()

        self.parent = parent
        self.main_controller = self.parent.main_controller

        self.dim = 0
        self.used_coords = []

        self.dim_lbl = QtGui.QLabel()
        self.endpoint_1_cbx = QtGui.QComboBox()
        self.endpoint_2_cbx = QtGui.QComboBox()

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.dim_lbl, 0, 0)
        self.layout.addWidget(self.endpoint_1_cbx, 0, 1, 1, 2)
        self.layout.addWidget(self.endpoint_2_cbx, 0, 3, 1, 2)

        self.endpoint_1_cbx.currentIndexChanged.connect(
            lambda: parent.update_roi(self.dim)
        )
        self.endpoint_2_cbx.currentIndexChanged.connect(
            lambda: parent.update_roi(self.dim)
        )

    # ------------------------------------------------------------------------------

    def set_dimension(self, dim, coords=None, indices=None):
        self.dim = dim

        self.data_array = self.main_controller.data_array
        self.dim_lbl.setText(self.data_array.dims[dim])
        raw_coords = self.data_array.coords[self.data_array.dims[dim]].values
        if coords is not None:
            raw_coords = coords

        if not type(raw_coords[0]) == str:
            raw_coords = [round(i, 5) for i in raw_coords]
        dim_coords = list(map(str, raw_coords))

        self.endpoint_1_cbx.clear()
        self.endpoint_2_cbx.clear()
        self.endpoint_1_cbx.addItems(dim_coords)
        self.endpoint_2_cbx.addItems(dim_coords)
        if indices is None:
            self.endpoint_2_cbx.setCurrentIndex(len(dim_coords) - 1)
            self.used_coords = dim_coords
        else:
            self.endpoint_1_cbx.setCurrentIndex(indices[0])
            self.endpoint_2_cbx.setCurrentIndex(indices[-1])

            self.used_coords = [dim_coords[i] for i in indices]

# ----------------------------------------------------------------------------------