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
    
    def __init__(
        self, 
        parent=None, 
        view=pg.PlotWidget(), 
        imageItem=None, 
        levelMode='mono'
    ) -> None:
        super(DataArrayImageView).__init__(parent, view, imageItem, levelMode)


    def setImage(data_array: xr.DataArray):
        ...

# ----------------------------------------------------------------------------------

class DataArrayPlot(pg.PlotWidget):
    """
    A custom PyQtGraph PlotWidget.
    """
    
    def __init__(
        self, 
        parent=None, 
        background='default', 
        plotItem=None
    ) -> None:
        super(DataArrayPlot).__init__(parent, background, plotItem)
