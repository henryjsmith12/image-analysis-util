"""
A general tool for plotting, slicing, and analyzing xarray DataArrays.
"""

# ----------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

# ----------------------------------------------------------------------------------

__all__ = (
    "ImageTool",
    "image_tool"
)

# ----------------------------------------------------------------------------------

class ImageTool(QtGui.QApplication):
    """
    
    """
    
    def __init__(self, data_array) -> None:
        super(ImageTool).__init__()

        self.data_array = data_array

# ----------------------------------------------------------------------------------

class ImageToolWidget(QtGui.QWidget):
    ...

# ----------------------------------------------------------------------------------

class ImageToolLayout(QtGui.QGridLayout):
    ...

# ----------------------------------------------------------------------------------