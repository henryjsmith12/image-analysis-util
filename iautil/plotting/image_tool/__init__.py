"""
A general tool for plotting, slicing, and analyzing xarray DataArrays.
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from pyqtgraph import dockarea, QtGui
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "ImageTool",
    "ImageToolWidget"
)

# ----------------------------------------------------------------------------------

class ImageTool:
    """
    Creates an instance of a QApplication and displays an ImageToolWidget object.
    """

    app = pg.mkQApp("ImageTool")

    def __init__(self, data_array: xr.DataArray) -> None:
        self.image_tool_widget = ImageToolWidget(data_array)

    # ------------------------------------------------------------------------------

    def show(self) -> None:
        """
        Displays ImageTool and executes app.
        """

        self.image_tool_widget.show()
        self.app.exec_()

# ----------------------------------------------------------------------------------

class ImageToolWidget(QtGui.QWidget):
    """
    ImageTool window and widget.
    """

    def __init__(self, data_array: xr.DataArray) -> None:
        super(ImageToolWidget, self).__init__()

        self.setWindowTitle("ImageTool")
        self.setMinimumSize(900, 675)

        self.data_array = data_array

        # Subwidgets
        self.data_array_image_view = None
        self.data_array_controller = None

        # Docks
        self.dock_area = dockarea.DockArea()
        self.data_array_image_view_dock = None
        self.controller_widget_dock = None
        
        # Creation functions
        self._create_widgets()
        self._create_docks()

        # Layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.dock_area)
        self.setLayout(self.layout)

    # ------------------------------------------------------------------------------

    def _create_widgets(self) -> None:
        """
        Instantiates widgets for ImageTool

        DataArrayImageView - Custom PyQtGraph ImageView widget
        DataArrayController - Controls slice direction and position
        """

        from iautil.plotting.image_tool.controller import DataArrayController
        from iautil.plotting.image_tool.slicing import SlicingTab
        from iautil.utilities.ui import DataArrayImageView
        
        self.data_array_image_view = DataArrayImageView()
        self.data_array_controller = DataArrayController(self.data_array, self)
        self.slicing_tab = SlicingTab(self.data_array, self)
        
    # ------------------------------------------------------------------------------
    
    def _create_docks(self) -> None:
        """
        Creates resizeable docks for each widget.
        """

        self.data_array_image_view_dock = dockarea.Dock(
            name="DataArray ImageView",
            size=(200, 300),
            widget=self.data_array_image_view,
            hideTitle=True
        )

        self.controller_widget_dock = dockarea.Dock(
            name="DataArray Controller",
            size=(200, 100),
            widget=self.data_array_controller
        )
        
        self.info_widget_dock = dockarea.Dock(
            name="DataArray Info",
            size=(200, 100),
            widget=None
        )

        self.slicing_tab_dock = dockarea.Dock(
            name="Slicing",
            size=(200, 400),
            widget=self.slicing_tab
        )

        self.dock_area.addDock(self.data_array_image_view_dock)
        self.dock_area.addDock(self.slicing_tab_dock, "right", 
            self.data_array_image_view_dock)
        self.dock_area.addDock(self.controller_widget_dock, "bottom", 
            self.data_array_image_view_dock)
        #self.dock_area.addDock(self.info_widget_dock, "below", 
            #self.controller_widget_dock)

# ----------------------------------------------------------------------------------
