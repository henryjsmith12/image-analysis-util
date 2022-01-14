"""
Widget that controls the DataArray loaded into an ImageTool instance.
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "DataArrayController"
)

# ----------------------------------------------------------------------------------

class DataArrayController(QtGui.QWidget):
    """
    
    """

    def __init__(self) -> None:
        super(DataArrayController).__init__()

