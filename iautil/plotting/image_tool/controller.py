"""
Controls DataArray slice in ImageView.
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

class DataArrayController(QtGui.QWidget):
    """
    Controls DataArray slice in ImageView.
    """

    updated = QtCore.pyqtSignal()

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(DataArrayController, self).__init__(parent)

        self.parent = parent
        self.data_array = data_array

        self.setAcceptDrops(True)

        self.dim_list = list(data_array.dims)
        self.dim_ctrl_list = []
        self.value_slider_list = []
        self.value_cbx_list = []
        
        # Custom layout
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        # Loops through axes
        for i in range(data_array.ndim):
            self.dim_ctrl_list.append(DimensionController(data_array, i, parent=self))
            self.value_slider_list.append(self.dim_ctrl_list[i].value_slider)
            self.value_cbx_list.append(self.dim_ctrl_list[i].value_cbx)

            self.layout.addWidget(self.dim_ctrl_list[i])

            self.dim_ctrl_list[i].updated.connect(self._update_image_view)

        self._update_axis_order()

    # ------------------------------------------------------------------------------

    def _update_axis_order(self) -> None:
        """
        Updates axis order to determine which slice is in view
        """

        axis_order = []
        for i in range(self.layout.count()):
            dim_ctrl = self.layout.itemAt(i).widget()

            axis_order.append(dim_ctrl.dim_lbl.text())
            # Enables/disables value-changing components based on axis
            if i <= 1:
                dim_ctrl.value_slider.setEnabled(False)
                dim_ctrl.value_cbx.setEnabled(False)
            else:
                dim_ctrl.value_slider.setEnabled(True)
                dim_ctrl.value_cbx.setEnabled(True)
        axis_order = tuple(axis_order)

        if self.data_array.ndim == 2:
            dim_0, dim_1 = axis_order
            self.data_array = self.data_array.transpose(dim_0, dim_1)
        if self.data_array.ndim == 3:
            dim_0, dim_1, dim_2 = axis_order
            self.data_array = self.data_array.transpose(dim_0, dim_1, dim_2)
        if self.data_array.ndim == 4:
            dim_0, dim_1, dim_2, dim_3 = axis_order
            self.data_array = self.data_array.transpose(dim_0, dim_1, dim_2, dim_3)

        self.updated.emit()

        self._update_image_view()

    # ------------------------------------------------------------------------------

    def _update_image_view(self) -> None:

        """
        Determines slice to display in ImageView.
        """

        if self.data_array.ndim == 2:
            data_array_slice = self.data_array[:, :]
        
        if self.data_array.ndim == 3:
            z = self.layout.itemAt(2).widget().value_slider.value()
            data_array_slice = self.data_array[:, :, z]

        if self.data_array.ndim == 4:
            z = self.layout.itemAt(2).widget().value_slider.value()
            t = self.layout.itemAt(3).widget().value_slider.value()
            data_array_slice = self.data_array[:, :, z, t]
        
        self.parent.data_array_image_view.set_data_array_slice(
            self.data_array,
            data_array_slice
        )

    # ------------------------------------------------------------------------------
    # Functions for dragging/dropping dimension controllers

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        drop_pos = e.pos()
        widget = e.source()

        for i in range(self.layout.count()):
            w = self.layout.itemAt(i).widget()

            if drop_pos.y() < w.y():
                    self.layout.insertWidget(i - 1, widget)
                    break
            else:
                if i == self.layout.count() - 1:
                    self.layout.insertWidget(i, widget)
                    break

        self._update_axis_order()
        e.accept()

# ----------------------------------------------------------------------------------

class DimensionController(QtGui.QGroupBox):

    updated = QtCore.pyqtSignal()
        
    def __init__(
        self, 
        data_array: xr.DataArray, 
        dim: int, 
        parent=None
    ) -> None:
        super(DimensionController, self).__init__(parent)

        self.parent = parent
        self.data_array = data_array

        self.dim_lbl = QtGui.QLabel()
        self.value_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.value_cbx = QtGui.QComboBox()

        if data_array is not None:
            self.dim_lbl.setText(data_array.dims[dim])
            raw_coords = data_array.coords[data_array.dims[dim]].values
            if not type(raw_coords[0]) == str:
                raw_coords = [round(i, 5) for i in raw_coords]
            dim_coords = list(map(str, raw_coords))

            self.value_slider.setMaximum(data_array.shape[dim] - 1)
            self.value_cbx.addItems(dim_coords)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.dim_lbl, 0, 0)
        self.layout.addWidget(self.value_slider, 0, 1, 1, 6)
        self.layout.addWidget(self.value_cbx, 0, 7, 1, 3)

        self.value_slider.valueChanged.connect(self._update_value)
        self.value_cbx.currentIndexChanged.connect(self._update_value)

    # ------------------------------------------------------------------------------

    def set_dimension(self, dim):

        self.data_array = self.parent.data_array
        self.dim_lbl.setText(self.data_array.dims[dim])
        raw_coords = self.data_array.coords[self.data_array.dims[dim]].values
        if not type(raw_coords[0]) == str:
            raw_coords = [round(i, 5) for i in raw_coords]
        dim_coords = list(map(str, raw_coords))

        self.value_slider.setMaximum(self.data_array.shape[dim] - 1)
        self.value_slider.setValue(0)
        self.value_cbx.clear()
        self.value_cbx.addItems(dim_coords)

    # ------------------------------------------------------------------------------
    
    def _update_value(self, e):
        if self.data_array is not None:
            if isinstance(self.sender(), QtGui.QSlider):
                value_index = self.sender().value()
                self.value_cbx.setCurrentIndex(value_index)

            if isinstance(self.sender(), QtGui.QComboBox):
                value_index = self.sender().currentIndex()
                self.value_slider.setValue(value_index)
                self.updated.emit()

    # ------------------------------------------------------------------------------
    # Function for dragging/dropping

    def mouseMoveEvent(self, e):
        if isinstance(self.parent, DataArrayController):
            if e.buttons() == QtCore.Qt.LeftButton:
                drag = QtGui.QDrag(self)
                mime = QtCore.QMimeData()
                drag.setMimeData(mime)
                drag.exec_(QtCore.Qt.MoveAction)

# ----------------------------------------------------------------------------------
