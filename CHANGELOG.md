# Change Log

All notable image-analysis-util changes will be stored here.

## [0.1.1] - 2022-02-17

To update to Version 0.1.1, run  `pip install image-analysis-util==0.1.1`

### Changed

* DataArray dimension controls changed to "drag-and-drop".

## [0.1.0] - 2022-01-23

To update to Version 0.1.0, run  `pip install image-analysis-util==0.1.0`

### Added

* I/O function `create_iau_file` that converts VTI (VTK Image Data) file(s) into an IAU file.
* I/O function `load_iau_file` that creates an xarray DataArray from an IAU file.
* `ImageTool` widget that displays 2D, 3D, and 4D xarray DataArrays.
