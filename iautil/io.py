"""
Houses basic I/O functions for creating/loading .iau files and reading
from various file types.
"""

# ----------------------------------------------------------------------------------

import h5py
import numpy as np
import os
from typing import List, Tuple
import vtk
import warnings
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "create_iau_file",
    "load_iau_file"
)

# ----------------------------------------------------------------------------------

def create_iau_file (
    data_source: str, 
    location: str = None, 
    axis_labels: List[str] = None, 
    new_axis_values: List = None,
    metadata: dict = None
) -> None:

    """
    Creates .iau file from data source. Data source can either be a single file
    or a directory of multiple data source files.

    Parameters:
    data_source (str): File/directory path used to create .iau file from.
    location (str): Directory (not file) path to save .iau file in.
    axis_labels (list[str]): Labels for each axis.
    new_axis_values (list): For .iau files created from multiple data source files
        stitched together. Defines values for new axis.
    metadata (dict): Metadata for .iau file.
    """

    # Data source validation
    if not os.path.exists(data_source):
        raise OSError(
            f"{data_source} is an invalid path."
        )

    # Save location validation
    if location is None:
        location = os.getcwd()
        warnings.warn(
            f"\n\nUsing {location} as save location...\n"
        )
    elif not os.path.exists(location) or not os.path.isdir(location):
        raise OSError(
            f"{location} is an invalid path."
        )

    if os.path.isdir(data_source):
        file_list = os.listdir(data_source).sort() # directory contents, sorted
        data_list, axes_list = [], []

        for file in file_list:
            data, axes = load_data_source(file)
            data_list.append(data)
            axes_list.append(axes)
        data, axes = stitch(data_list, axes_list)

        if new_axis_values is None:
            new_axis_values = [i for i in range(data.shape[-1])]
            print(new_axis_values)

        axes.append(new_axis_values)

    elif os.path.isfile(data_source):
        data, axes = load_data_source(data_source)

# ----------------------------------------------------------------------------------

def load_iau_file(file: str) -> xr.Dataset:
    """
    Retrieves data, axis info, and metadata from .iau file in an xarray dataset.

    Parameters:
        file (str): .iau file to load.

    Returns:
        dataset (xr.Dataset): Dataset containing data, axis info, and metadata.
    """
    ...

# ----------------------------------------------------------------------------------

def stitch(
    data_list: List[np.ndarray],
    axes_list: List[list]
) -> Tuple[np.ndarray, List[list]]:
    """
    Stitches data from multiple data source files. Also checks for inconsistencies 
    in axis values.

    Parameters:
        data_list (list[np.ndarray]): List of data from each data source file.
        axes_list (list[list]): List of axis values from each data source file.

    Returns:
        data (np.ndarray): Stacked data arrays; n + 1 dimensions.
        axes (list[list]): Axis values from each axis.
    """
    ...

# ----------------------------------------------------------------------------------

def load_data_source(file: str) -> Tuple[np.ndarray, List]:
    """
    Retrieves data and axis values from data source file.

    Parameters:
        file (str): Data source file to load.

    Returns:
        data (np.ndarray): Multi-dimensional NumPy array holding data.
        axes (list[list]): List of values for each axis.
    """
    ...

# ----------------------------------------------------------------------------------

create_iau_file(".")
