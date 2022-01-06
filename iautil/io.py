"""
Houses basic I/O functions for creating and loading .iau files.
"""

import h5py
import numpy as np
from typing import List
import vtk
import xarray as xr

__all__ = (
    "create_iau_file",
    "load_iau_file"
)

def create_iau_file (
    data_source: str, 
    save_location: str = None, 
    axis_labels: List[str] = None, 
    new_axis_values: List = None,
    metadata: dict = None
) -> None:

    """
    Creates .iau file from data source.

    Parameters:
    data_source (str): Data source file/directory used to create .iau file.
    save_location (str): Path to save .iau file in.
    axis_labels (list[str]): Labels for each axis.
    new_axis_values (list): For .iau files created from multiple data source files
        stitched together. Defines values for new axis.
    metadata (dict): Metadata for .iau file.
    """

    ...

def load_iau_file(file) -> xr.Dataset:
    """
    
    """
    ...