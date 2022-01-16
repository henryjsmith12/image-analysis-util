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
            view=pg.PlotItem(),
            imageItem=pg.ImageItem()
        )

    # ------------------------------------------------------------------------------

    def setDataArray(self, data_array_slice: xr.DataArray):
        """
        
        """

        image = data_array_slice.values
        self.setImage(image)

# ----------------------------------------------------------------------------------

class DataArrayPlot(pg.PlotWidget):
    """
    A custom PyQtGraph PlotWidget.
    """
    
    def __init__(self, parent=None, plotItem=None) -> None:
        super(DataArrayPlot, self).__init__(parent, plotItem)

# ----------------------------------------------------------------------------------

