"""
UI widget classes.
"""

# ----------------------------------------------------------------------------------

from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "DataArrayImageView",
    "DataArrayPlot",
    "set_data_array"
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

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        
        self.view.setAspectLocked(lock=False)
        self.view.enableAutoRange()

    # ------------------------------------------------------------------------------

    def set_data_array(self, data_array: xr.DataArray) -> None:
        """
        
        """

        image = self._set_color_map(data_array.values)
        self.view.setLabels(
            bottom = data_array.dims[0],
            left = data_array.dims[1]
        )

        self.setImage(image)

    # ------------------------------------------------------------------------------

    def _set_color_map(image: np.ndarray) -> np.ndarray:
        """
        
        """

        image_max = np.amax(image)
        norm = colors.LogNorm(vmax=image_max)

        normalized_image = norm(image)
        color_image = plt.cm.jet(normalized_image)

        return color_image

# ----------------------------------------------------------------------------------

class DataArrayPlot(pg.PlotWidget):
    """
    A custom PyQtGraph PlotWidget.
    """
    
    def __init__(self, parent=None, plotItem=None) -> None:
        super(DataArrayPlot, self).__init__(parent, plotItem)

# ----------------------------------------------------------------------------------