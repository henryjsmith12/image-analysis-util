"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ==============================================================================

import h5py
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

# ==============================================================================

class MainWindow(QtGui.QWidget):
    """
    
    """

    def __init__(self, file_path) -> None:
        super().__init__()

        self.file_path = file_path
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)