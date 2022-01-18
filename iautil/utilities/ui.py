"""
UI widget classes.
"""

# ----------------------------------------------------------------------------------

import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "DataArrayImageView",
    "DataArrayPlot"
)

# ----------------------------------------------------------------------------------

class DataArrayImageView(pg.ImageView):
    """
    A custom PyQtGraph ImageView.
    """
    
    def __init__(self, parent=None) -> None:
        super(DataArrayImageView, self).__init__(
            parent, 
            view=pg.PlotItem()
        )

    # ------------------------------------------------------------------------------

    def set_data_array(self, data_array: xr.DataArray):
        """
        
        """

        image = data_array.values
        self.view.setLabels(
            bottom = data_array.dims[0],
            left = data_array.dims[1]
        )
        self.setImage(image)

# ----------------------------------------------------------------------------------

class DataArrayPlot(pg.PlotWidget):
    """
    A custom PyQtGraph PlotWidget.
    """
    
    def __init__(self, parent=None, plotItem=None) -> None:
        super(DataArrayPlot, self).__init__(parent, plotItem)

# ----------------------------------------------------------------------------------