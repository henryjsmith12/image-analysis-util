"""
Basic I/O functions for:
- Creating IAU file from manual arguments
- Creating IAU file from a .vti (VTK Image Data) file/directory
- Creating an xarray DataArray from a IAU file
"""

# ----------------------------------------------------------------------------------

import ast
import h5py
import numpy as np
import os
from typing import List
import vtk
from vtk.util import numpy_support as npSup # type: ignore
import xarray as xr

# ----------------------------------------------------------------------------------

__all__ = (
    "create_iau",
    "vti_to_iau",
    "iau_to_data_array"
)

# ----------------------------------------------------------------------------------

def create_iau(
    iau_path: str,
    data: np.ndarray,
    coords: list = None,
    dims: list = None,
    metadata: dict = None
):
    """
    Creates IAU file.

    Parameters:
    iau_path (str): Path to save file in.
    data (np.ndarray): A numpy array of data points to be stored in file.
    coords (list): A list of lists of coordinates for each dimension of dataset.
    dims (list): A list of labels for each dimension of dataset.
    metadata (dict): Metadata for file.
    """

    if iau_path is None:
        raise ValueError("IAU path not given.")
    if type(iau_path) != str:
        raise ValueError("IAU path must be a string.")

    if data is None:
        raise ValueError("data not given.")
    if type(data) != np.ndarray:
        raise ValueError("data must be a numpy ndarray.")

    if coords is not None:
        if type(coords) != list:
            raise ValueError("coords must be a list.")

    if dims is not None:
        if type(dims) != list:
            raise ValueError("dims must be a list.")

    if metadata is not None:
        if type(metadata) != dict:
            raise ValueError("metadata must be a dictionary.")

    if None not in [coords, dims] and len(coords) != len(dims):
        raise RuntimeError("Dimension sizes for coords and dims do not match.")

    with h5py.File(iau_path, "a") as new_file:
        new_file.create_dataset("data", data=data)
        new_file.attrs["metadata"] = str(metadata)
        new_file.create_group("axes")

        if dims is None:
            dims = [f"dim_{i}" for i in range(data.ndim)]

        for i in range(len(coords)):
            new_file["data"].dims[i].label = dims[i]

            if coords is not None:
                axis = np.array(coords[i])
                new_file.create_dataset(f"axes/axis_{i}", data=axis)
                new_file[f"axes/axis_{i}"].make_scale(dims[i])
                new_file["data"].dims[i].attach_scale(new_file[f"axes/axis_{i}"])

# ----------------------------------------------------------------------------------

def vti_to_iau(
    vti_path: str,
    iau_path: str,
    new_dim_coords: list = None,
    dims: list = None,
    metadata: dict = None
):
    """
    Creates IAU file from VTI file(s).

    Parameters:
    iau_path (str): Path to save file in.
    data (np.ndarray): A numpy array of data points to be stored in file.
    coords (list): A list of lists of coordinates for each dimension of dataset.
    dims (list): A list of labels for each dimension of dataset.
    metadata (dict): Metadata for file.
    """

    if vti_path is None:
        raise ValueError("VTI path not given.")
    if type(vti_path) != str:
        raise ValueError("VTI path must be a string.")

    # Data source as directory
    if os.path.isdir(vti_path):
        file_list = os.listdir(vti_path) # directory contents, sorted
        file_list.sort()
        data_list, coords_list = [], []

        for file in file_list:
            if file.endswith(".vti"):
                data, coords = _load_vti(str(os.path.join(vti_path, file)))
                data_list.append(data)
                coords_list.append(coords)
        data, coords = _stitch(data_list, coords_list)

        # Handles new axis values 
        if new_dim_coords is None:
            new_dim_coords = [i for i in range(data.shape[-1])]
        coords.append(new_dim_coords)

    # Data source as file
    elif os.path.isfile(vti_path):
        data, coords = _load_vti(vti_path)

    else:
        raise RuntimeError("Invalid VTI path.")

    create_iau(
        iau_path=iau_path,
        data=data,
        coords=coords,
        dims=dims,
        metadata=metadata
    )

# ----------------------------------------------------------------------------------

def iau_to_data_array(iau_path: str):
    """
    Retrieves data, axis info, and metadata from .iau file in an xarray dataset.

    Parameters:
        file (str): .iau file to load.

    Returns:
        data_array (xr.DataArray): Dataset containing data, axis info, and metadata.
    """
    
    # Reads info from .iau file
    with h5py.File(iau_path, 'r') as iau_file:
        data = iau_file["data"][...]
        coords = [iau_file["data"].dims[i][0][...] for i in range(data.ndim)]
        dims = [iau_file["data"].dims[i].label for i in range(data.ndim)]
        metadata = ast.literal_eval(iau_file.attrs["metadata"])

    # Creates xarray DataArray from .iau info
    # Internal data structure for everything in image-analysis-util
    data_array = xr.DataArray(
        data=data, 
        coords=coords, 
        dims=dims, 
        attrs=metadata
    )

    return data_array

# ----------------------------------------------------------------------------------

def _load_vti(vti_path: str):

    data_reader = vtk.vtkXMLImageDataReader()
    data_reader.SetFileName(vti_path)
    data_reader.Update()

    raw_data = data_reader.GetOutput()
    dimensions = list(raw_data.GetDimensions())

    data = npSup.vtk_to_numpy(raw_data.GetPointData().GetArray('Scalars_'))
    data = data.reshape(dimensions)

    origin = raw_data.GetOrigin() # First point for each axis
    spacing = raw_data.GetSpacing() # Space between points for each axis
    extent = raw_data.GetExtent() # First and last index of each axis

    axis_0, axis_1, axis_2 = [], [], []

    for point in range(extent[0], extent[1] + 1):
        axis_0.append(origin[0] + point * spacing[0])
    for point in range(extent[2], extent[3] + 1):
        axis_1.append(origin[1] + point * spacing[1])
    for point in range(extent[4], extent[5] + 1):
        axis_2.append(origin[2] + point * spacing[2])

    # A list of lists of varying lengths
    coords = [axis_0, axis_1, axis_2]

    return data, coords

# ----------------------------------------------------------------------------------

def _stitch(
    data_list: List[np.ndarray],
    coords_list: List[list]
):
    data, coords = None, None

    # Checks if coords stay consistent throughout data source files
    consistent_coords = coords_list.count(coords_list[0]) == len(coords_list)

    if consistent_coords:
        coords = coords_list[0]
    else:
        raise ValueError(
            "Inconsistent coords throughout data source files."
        )

    # Converts list of NumPy arrays (ndim = n) to one NumPy array (ndim = n + 1)
    data = np.stack(data_list, axis=-1)
    
    return data, coords

# ----------------------------------------------------------------------------------