"""

"""

# ----------------------------------------------------------------------------------

from setuptools import setup

# ----------------------------------------------------------------------------------

setup( 
    name="image-analysis-util",
    version="0.0.0",
    description="Scientific image exploration software for multidimensional datasets.",
    author="Henry Smith",
    author_email="smithh@anl.gov",
    url="https://github.com/henryjsmith12/image-analysis-util/iautil",
    install_requires=[
        "h5py",
        "numpy",
        "PyQt5",
        "pyqtgraph",
        "scipy",
        "vtk",
        "xarray",
    ],
    license="See LICENSE file",
    platforms="any",
)

