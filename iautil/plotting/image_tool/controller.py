"""
Controls DataArray slice in ImageView.
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

AXES = ["x", "y", "z", "t"]

AXES_DICT = {
    "x" : 0,
    "y" : 1,
    "z" : 2,
    "t" : 3
}

# ----------------------------------------------------------------------------------

class DataArrayController(QtGui.QWidget):
    """
    Controls DataArray slice in ImageView.
    """

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(DataArrayController, self).__init__(parent)

        self.parent = parent
        self.data_array = data_array
        
        # Custom layout
        self.layout = DataArrayControllerLayout(data_array, parent=self)
        self.setLayout(self.layout)

        # Component lists from layout
        self.lbl_list = self.layout.lbl_list
        self.axis_cbx_list = self.layout.axis_cbx_list
        self.value_slider_list = self.layout.value_slider_list
        self.value_cbx_list = self.layout.value_cbx_list

        self._update_value()
        self._update_axes()

    # ------------------------------------------------------------------------------

    def _update_value(self) -> None:
        """
        Updates value for axis when changed by a slider or combobox.
        """
        
        if isinstance(self.sender(), QtGui.QSlider):
            dim = self.value_slider_list.index(self.sender())
            value_index = self.sender().value()
            self.value_cbx_list[dim].setCurrentIndex(value_index)

        if isinstance(self.sender(), QtGui.QComboBox):
            dim = self.value_cbx_list.index(self.sender())
            value_index = self.sender().currentIndex()
            self.value_slider_list[dim].setValue(value_index)

        self._update_image_view()

    # ------------------------------------------------------------------------------

    def _update_axes(self) -> None:
        """
        Updates axis order to determine which slice is in view
        """

        # After initial update (after controller is created)
        if not self.sender() is None:
            # Changed axis
            new_axis = self.sender().currentIndex()

            # All axes
            axes = [i for i in range(self.data_array.ndim)]

            # Axes after initial change
            curr_axes = [cbx.currentIndex() for cbx in self.axis_cbx_list]
            
            # Axis that is not in curr_axes
            try:
                axis_to_add = list(set(axes) - set(curr_axes))[0]
            except:
                pass

        # Loops through axes
        for i in range(self.data_array.ndim):
            cbx = self.axis_cbx_list[i]

            # After initial update (after controller is created)
            if not self.sender() is None:
                if cbx.currentIndex() == new_axis and not cbx == self.sender():
                    cbx.setCurrentIndex(axis_to_add)

            # Enables/disables value-changing components based on axis
            if cbx.currentIndex() <= 1:
                self.value_slider_list[i].setEnabled(False)
                self.value_cbx_list[i].setEnabled(False)
            else:
                self.value_slider_list[i].setEnabled(True)
                self.value_cbx_list[i].setEnabled(True)

        self._update_image_view()

    # ------------------------------------------------------------------------------

    def _update_image_view(self) -> None:
        """
        Determines slice to display in ImageView.
        """

        str_numpy_args = ""
        axis_order = []
        transpose = False
        x_index, y_index = 0, 0
        z, t = 0, 0

        # Loops through axes
        for i in range(self.data_array.ndim):
            axis_order.append(
                self.data_array.dims[AXES_DICT[self.axis_cbx_list[i].currentText()]]
            )
            if self.axis_cbx_list[i].currentIndex() == 0:
                x_index = i
            elif self.axis_cbx_list[i].currentIndex() == 1:
                y_index = i
            elif self.axis_cbx_list[i].currentIndex() == 2:
                z = self.value_slider_list[i].value()
            else:
                t = self.value_slider_list[i].value()

        # Transposes DataArray to match axis order
        # Creates DataArray Slice to be displayed
        axis_order = tuple(axis_order)
        if self.data_array.ndim == 2:
            ax_0, ax_1 = axis_order
            data_array_T = self.data_array.transpose(ax_0, ax_1)
            data_array_slice = data_array_T
        if self.data_array.ndim == 3:
            ax_0, ax_1, ax_2 = axis_order
            data_array_T = self.data_array.transpose(ax_0, ax_1, ax_2)
            data_array_slice = data_array_T[:, :, z]
        if self.data_array.ndim == 4:
            ax_0, ax_1, ax_2, ax_3 = axis_order
            data_array_T = self.data_array.transpose(ax_0, ax_1, ax_2, ax_3)
            data_array_slice = data_array_T[:, :, z, t]
        
        # Checks for possible x-y transposition condition
        if x_index > y_index:
            data_array_slice = data_array_slice.T

        # Checks for empty slice
        if data_array_slice.values.ndim != 0:
            self.parent.data_array_image_view.set_data_array_slice(
                data_array_T,
                data_array_slice
            )
            
        
# ----------------------------------------------------------------------------------

class DataArrayControllerLayout(QtGui.QGridLayout):
    """
    Custom dynamic grid layout for controller
    """

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(DataArrayControllerLayout, self).__init__(parent)

        # Lists for components
        self.lbl_list = []
        self.axis_cbx_list = []
        self.value_slider_list = []
        self.value_cbx_list = []

        # Axis labels (depends on number of dimensions in DataArray)
        axes = AXES[:data_array.ndim]

        # Loops through axes
        for i in range(data_array.ndim):
            dim_lbl = data_array.dims[i]

            # Rounds numeric labels and converts them to strings
            raw_coords = data_array.coords[dim_lbl].values
            if not type(raw_coords[0]) == str:
                raw_coords = [round(i, 5) for i in raw_coords]
            dim_coords = list(map(str, raw_coords))

            # Adds new component to respective list
            self.lbl_list.append(QtGui.QLabel(dim_lbl))
            self.axis_cbx_list.append(QtGui.QComboBox())
            self.value_slider_list.append(QtGui.QSlider(QtCore.Qt.Horizontal))
            self.value_cbx_list.append(QtGui.QComboBox())

            # Adds axes and sets current axis
            self.axis_cbx_list[i].addItems(axes)
            self.axis_cbx_list[i].setCurrentIndex(i)

            # Sets max value index 
            self.value_slider_list[i].setMaximum(data_array.shape[i] - 1)

            # Adds values
            self.value_cbx_list[i].addItems(dim_coords)

            # Adds components to layout
            self.addWidget(self.lbl_list[i], i, 0)
            self.addWidget(self.axis_cbx_list[i], i, 1)
            self.addWidget(self.value_slider_list[i], i, 2, 1, 3)
            self.addWidget(self.value_cbx_list[i], i, 5)

            # Connections
            self.axis_cbx_list[i].currentIndexChanged.connect(
                parent._update_axes
            )
            self.value_slider_list[i].valueChanged.connect(
                parent._update_value
            )
            self.value_cbx_list[i].currentIndexChanged.connect(
                parent._update_value
            )

# ----------------------------------------------------------------------------------