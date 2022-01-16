"""
A general tool for plotting, slicing, and analyzing xarray DataArrays.
"""

# ----------------------------------------------------------------------------------

from iautil.plotting.image_tool import DataArrayController
from iautil.utilities.ui import DataArrayImageView
import numpy as np
import pyqtgraph as pg
from pyqtgraph import dockarea, QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "ImageTool",
    "ImageToolWidget"
)

# ----------------------------------------------------------------------------------

class ImageTool:
    """
    
    """

    def __init__(self, data_array: xr.DataArray) -> None:
        app = pg.mkQApp()
        image_tool_widget = ImageToolWidget(data_array)
        image_tool_widget.show()
        app.exec_()

# ----------------------------------------------------------------------------------

class ImageToolWidget(QtGui.QWidget):
    """

    """

    def __init__(self, data_array: xr.DataArray) -> None:
        super(ImageToolWidget, self).__init__()

        self.data_array = data_array

        self.data_array_image_view = None
        self.controller_widget = None

        self.dock_area = dockarea.DockArea()
        self.data_array_image_view_dock = None
        self.controller_widget_dock = None
        
        self._create_widgets()
        self._create_docks()

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.dock_area)
        self.setLayout(self.layout)

    # ------------------------------------------------------------------------------

    def _create_widgets(self) -> None:
        """
        
        """
        
        # Generic placeholder widgets
        #self.data_array_image_view = pg.ImageView()
        #self.controller_widget = QtGui.QWidget()

        self.data_array_image_view = DataArrayImageView()
        self.controller_widget = DataArrayController()
        
    # ------------------------------------------------------------------------------
    
    def _create_docks(self) -> None:
        """
        
        """

        self.data_array_image_view_dock = dockarea.Dock(
            name="DataArray ImageView",
            size=(200, 200),
            widget=self.data_array_image_view,
            hideTitle=True
        )

        self.controller_widget_dock = dockarea.Dock(
            name="Controller",
            size=(200, 100),
            widget=self.controller_widget,
            hideTitle=True
        )

        self.dock_area.addDock(self.data_array_image_view_dock)
        self.dock_area.addDock(self.controller_widget_dock)

# ----------------------------------------------------------------------------------

ImageTool(
    xr.DataArray(
        data=np.random.rand(3, 4, 5),
        coords=[
            ("DIM_ONE", ["a", "b", "c"]),
            ("DIM_TWO", [1, 2, 3, 4]),
            ("DIM_THREE", ["q", "w", "e", "r", "t"])
        ]
    )
)