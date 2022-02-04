"""
Contains overridden UI widget classes from PyQtGraph.
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
    A custom PyQtGraph ImageView widget. Only displays 2D images, so all slice 
    controls (switching slice/direction) are handled externally.
    """
    
    def __init__(self, parent=None) -> None:
        super(DataArrayImageView, self).__init__(
            parent, 
            view=pg.PlotItem(),
            imageItem=pg.ImageItem()
        )

        self.parent = parent

        self.data_array = None
        self.data_array_slice = None
        self.image_item = None
        self.axis_order = None

        # Removes out default ImageView features
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        # Aspect/range settings
        self.view.setAspectLocked(lock=False)
        self.view.enableAutoRange()

    # ------------------------------------------------------------------------------

    def set_data_array_slice(
        self, 
        data_array: xr.DataArray, 
        data_array_slice: xr.DataArray, 
        axis_order
    ) -> None:

        """
        Sets image, axis labels, axis coordinates for ImageView.

        Parameters:
            data_array (xr.DataArray): 2D DataArray with data, coords, and dims
        """

        self.data_array = data_array
        self.axis_order = axis_order

        # Adds matplotlib colormap to image
        self.data_array_slice = self._set_color_map(data_array_slice.values)
        self.image_item = pg.ImageItem(self.data_array_slice)

        # Sets plot labels
        self.view.setLabels(
            bottom = data_array_slice.dims[0],
            left = data_array_slice.dims[1]
        )

        # Retrieves axis starting positions and scaling
        pos, scale = self._get_axis_coords(data_array_slice)

        # Adds image to ImageView with proper axes
        self.setImage(self.data_array_slice, pos=pos, scale=scale)

    # ------------------------------------------------------------------------------

    def _set_color_map(self, image: np.ndarray) -> np.ndarray:
        """
        Adds colormap to an image. Currently only supports matplotlib "jet" in
        logarithmic scale.

        Parameters:
            image (np.ndarray): NumPy array to map

        Returns:
            color_image (np.ndarray): NumPy array with color mapping
        """

        # Max pixel value in image
        image_max = np.amax(image)

        # Normalizer
        norm = colors.LogNorm(vmax=image_max)

        # Normalized image
        normalized_image = norm(image)

        # Normalized image with colormap
        color_image = plt.cm.jet(normalized_image)

        return color_image

    # ------------------------------------------------------------------------------

    def _get_axis_coords(self, data_array: xr.DataArray):
        """
        Retrieves axis starting points and scaling for image.

        Parameters:
            data_array (xr.DataArray): 2D DataArray with data, coords, and dims

        Returns:
            x (float): starting x point
            y (float): starting y point
            x_scale (float): space between x points
            y_scale (float): space between y points
        """

        def _is_monotonic(values: list) -> bool:
            """
            Checks list for monoticity.
            """
            # Differentiated list
            dx = np.diff(values)

            return np.all(dx <= 0) or np.all(dx >= 0)

        def _set_rect_values(values: list):
            """
            Selects starting point and scale based on list item type and monoticity.
            """

            if type(values[0]) == str or not _is_monotonic(values):
                start = 0
                scale = 1
            else:
                start = values[0]
                scale = values[1] - values[0]

            return start, scale
        
        # NumPy arrays of values from DataArray
        x_values = data_array.coords[data_array.dims[0]].values
        y_values = data_array.coords[data_array.dims[1]].values

        x, x_scale = _set_rect_values(x_values)
        y, y_scale = _set_rect_values(y_values)

        return (x, y), (x_scale, y_scale)

# ----------------------------------------------------------------------------------

class DataArrayPlot(pg.PlotWidget):
    """
    A custom PyQtGraph PlotWidget.
    """
    
    def __init__(self, parent=None, plotItem=None) -> None:
        super(DataArrayPlot, self).__init__(parent, plotItem)

        self.setBackground("default")

    # ------------------------------------------------------------------------------

    def set_data_array_slice(
        self, 
        data_array: xr.DataArray, 
        data_array_slice: xr.DataArray, 
        axis_order
    ) -> None:
        """

        """

        self.data_array = data_array
        self.axis_order = axis_order

        # Adds matplotlib colormap to image
        self.data_array_slice = data_array_slice.values

        # Sets plot labels
        self.setLabels(
            bottom = data_array_slice.dims[0]
        )

        # Adds image to ImageView with proper axes
        self.plot(self.data_array_slice, clear=True)


# ----------------------------------------------------------------------------------

class SlicingROI(pg.LineSegmentROI):
    """
    
    """

    def __init__(self, position=(0,0), parent=None, child=None) -> None:
        super(SlicingROI, self).__init__(position)

        self.parent = parent
        self.child = child

        self.parent.addItem(self)

        self.sigRegionChanged.connect(self.slice_data_array)

    # ------------------------------------------------------------------------------

    def slice_data_array(self):
        p_data_array = self.parent.data_array
        p_data_array_slice = self.parent.data_array_slice
        p_axis_order = self.parent.axis_order[:p_data_array.ndim]

        data, coords = self.getArrayRegion(
            data=p_data_array_slice,
            img=self.parent.getImageItem(),
            returnMappedCoords=True
        )
        x_coords, y_coords = coords.astype(int)
        
        if p_data_array.ndim == 2:
            ax_0, ax_1 = p_axis_order
            p_data_array.transpose(ax_0, ax_1)
        if p_data_array.ndim == 3:
            ax_0, ax_1, ax_2 = p_axis_order
            p_data_array.transpose(ax_0, ax_1, ax_2)
        if p_data_array.ndim == 4:
            ax_0, ax_1, ax_2, ax_3 = p_axis_order
            p_data_array.transpose(ax_0, ax_1, ax_2, ax_3)

        for i in range(len(x_coords)):
            if x_coords[i] < 0:
                x_coords[i] = 0
            if x_coords[i] >= p_data_array.values.shape[0]:
                x_coords[i] = p_data_array.values.shape[0] - 1

        for i in range(len(y_coords)):
            if y_coords[i] < 0:
                y_coords[i] = 0
            if y_coords[i] >= p_data_array.values.shape[1]:
                y_coords[i] = p_data_array.values.shape[1] - 1

        c_data_array = xr.concat(
            [p_data_array[x, y] for x, y in zip(x_coords, y_coords)],
            f"{p_data_array.dims[0]}, {p_data_array.dims[1]}"
        )

        if c_data_array.ndim == 3:
            c_data_array_slice = c_data_array[:, :, c_data_array.values.shape[2] - 1]
        else:
            c_data_array_slice = c_data_array
        
        c_axis_order = tuple([c_data_array.dims[i] for i in range(c_data_array.ndim)])

        self.child.set_data_array_slice(
            c_data_array,
            c_data_array_slice,
            c_axis_order
        )
        


