"""
Widget that controls the DataArray loaded into an ImageTool instance.
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "DataArrayController"
)

# ----------------------------------------------------------------------------------

DIMENSION_LOCATIONS = [
    "x-axis",
    "y-axis",
    ""
]

# ----------------------------------------------------------------------------------

class DataArrayController(QtGui.QWidget):
    """
    
    """

    def __init__(self, data_array: xr.DataArray) -> None:
        super(DataArrayController, self).__init__()

        self.data_array = data_array
        self.updated = False

        self.layout = DataArrayControllerLayout(data_array, parent=self)
        self.setLayout(self.layout)

        self.dim_lbl_list = self.layout.dim_lbl_list
        self.dim_location_cbx_list = self.layout.dim_location_cbx_list
        self.dim_slider_list = self.layout.dim_slider_list
        self.dim_currval_cbx_list = self.layout.dim_currval_cbx_list

    # ------------------------------------------------------------------------------

    def _update_currval(self) -> None:
        """
        
        """
        
        if isinstance(self.sender(), QtGui.QSlider) and not self.updated:
            dim = self.dim_slider_list.index(self.sender())
            index = self.sender().value()
            self.dim_currval_cbx_list[dim].setCurrentIndex(index)
            #self.updated = True
        if isinstance(self.sender(), QtGui.QComboBox) and not self.updated:
            dim = self.dim_currval_cbx_list.index(self.sender())
            index = self.sender().currentIndex()
            self.dim_slider_list[dim].setValue(index)
            #self.updated = True

    # ------------------------------------------------------------------------------

    def _update_location(self) -> None:
        """
        
        """

# ----------------------------------------------------------------------------------

class DataArrayControllerLayout(QtGui.QGridLayout):
    """
    
    """

    def __init__(self, data_array: xr.DataArray, parent=None) -> None:
        super(DataArrayControllerLayout, self).__init__(parent)

        self.dim_lbl_list = []
        self.dim_location_cbx_list = []
        self.dim_slider_list = []
        self.dim_currval_cbx_list = []

        for i in range(data_array.ndim):
            dim_lbl = data_array.dims[i]
            dim_coords = map(str, data_array.coords[dim_lbl].values)

            self.dim_lbl_list.append(QtGui.QLabel(dim_lbl))
            self.dim_location_cbx_list.append(QtGui.QComboBox())
            self.dim_slider_list.append(QtGui.QSlider(QtCore.Qt.Horizontal))
            self.dim_currval_cbx_list.append(QtGui.QComboBox())

            self.dim_location_cbx_list[i].addItems(DIMENSION_LOCATIONS)
            self.dim_location_cbx_list[i].setCurrentIndex(i)
            self.dim_slider_list[i].setMaximum(data_array.shape[i] - 1)
            self.dim_currval_cbx_list[i].addItems(dim_coords)

            self.addWidget(self.dim_lbl_list[i], i, 0)
            self.addWidget(self.dim_location_cbx_list[i], i, 1)
            self.addWidget(self.dim_slider_list[i], i, 2, 1, 3)
            self.addWidget(self.dim_currval_cbx_list[i], i, 5)

            self.dim_slider_list[i].valueChanged.connect(
                parent._update_currval
            )
            self.dim_currval_cbx_list[i].valueChanged.connect(
                parent._update_currval
            )

# ----------------------------------------------------------------------------------

app = pg.mkQApp()
ctrl = DataArrayController(
    xr.DataArray(
        data=np.random.rand(3, 4, 5),
        coords=[
            ("DIM_ONE", ["a", "b", "c"]),
            ("DIM_TWO", [1, 2, 3, 4]),
            ("DIM_THREE", ["q", "w", "e", "r", "t"])
        ]
    )
)
ctrl.show()
app.exec_()

