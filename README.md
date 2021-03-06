# image-analysis-util

Copyright (c) UChicago Argonne, LLC. All rights reserved.

Scientific image exploration software for 2D, 3D, and 4D datasets. A continuation of the Image_Analysis repository.

## About

The image-analysis-util repository focuses on providing tools for users to explore and analyze their datasets. The ultimate goal of image-analysis-util is to provide a generalized set of analysis features.

### Built With

* [`h5py`](https://docs.h5py.org/en/stable/)
* [`PyQt5`](https://doc.qt.io/qtforpython/)
* [`pyqtgraph`](https://pyqtgraph.readthedocs.io/en/latest/)
* [`xarray`](https://xarray.pydata.org/en/stable/)

## Getting Started

### Prerequisites

* [Python 3.7+](https://www.python.org/downloads/)
* [Anaconda 3](https://www.anaconda.com/products/individual)

### Installation

#### PyPI Installation

```
pip install image-analysis-util
```

#### Conda Installation

1. Clone the repositiory.

   ```
   git clone https://github.com/henryjsmith12/image-analysis-util.git
   ```
   
2. Create an Anaconda virtual environment using `environment.yml`. The environment name can be altered in that file. By default, the virtual environment is named `ia-util-venv`.

   ```
   conda env create -f environment.yml
   ```
3. Activate the virtual environment.

   ```
   conda activate ia-util-venv
   ```

## Screenshots

<img src="https://github.com/henryjsmith12/image-analysis-util/blob/main/examples/screenshots/v0_1_2_image_tool_3d.png" width="500"/>

<img src="https://github.com/henryjsmith12/image-analysis-util/blob/main/examples/screenshots/v0_1_2_image_tool_4d.png" width="500"/>

## Roadmap

* [X] Tutorial files for file creation/ImageTool
* [ ] File Exportation - The ideal goal will be to have exporting options for xarray DataArray objects, .iau files, and matplotlib plots.
* [ ] Performance improvements for slicing
* [ ] Extensive testing
* [ ] Pixel averaging (ROIs/Binning)

## License

See [`LICENSE.txt`](https://github.com/henryjsmith12/image-analysis-util/blob/main/LICENSE) for more information.

## Author

[Henry Smith](https://www.linkedin.com/in/henry-smith-5956a0189/) - Co-op Student Technical at Argonne National Laboratory

## Support

* [Report bugs here](https://github.com/henryjsmith12/image-analysis-util/issues)
* Email author at [smithh@anl.gov](smithh@anl.gov)
