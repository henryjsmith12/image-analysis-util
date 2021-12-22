"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ==============================================================================

import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

# ==============================================================================

class FileSelectionWidget(QtGui.QWidget):

    """ 
    A dialog that allows the user to select or create, and then load a file.

    "Select File" opens a QFileDialog (pyqt5) widget, restricted to accept only .iau files.
    "Create File" opens a FileCreationWidget, where the user can create an .iau file.
    "Load File" loads the selected file into a new analysis window.
    """
    
    def __init__(self):
        super(FileSelectionWidget, self).__init__()

        # Subwidget creation
        self.prompt_lbl = QtGui.QLabel("Select or create an .iau file to begin.")
        self.prompt_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.select_file_txt = QtGui.QLineEdit()
        self.select_file_txt.setReadOnly(True)
        self.select_file_btn = QtGui.QPushButton("Select File")
        self.select_file_btn.setDefault(True)
        self.create_file_btn = QtGui.QPushButton("Create File")
        self.load_file_btn = QtGui.QPushButton("Load File")
        self.load_file_btn.setEnabled(False)

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.prompt_lbl, 0, 0, 1, 4)
        self.layout.addWidget(self.select_file_txt, 1, 0, 1, 2)
        self.layout.addWidget(self.select_file_btn, 1, 2, 1, 2)
        self.layout.addWidget(self.create_file_btn, 2, 0, 1, 2)
        self.layout.addWidget(self.load_file_btn, 2, 2, 1, 2)

        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(3, 1)

# ==============================================================================

class FileCreationWidget(QtGui.QWidget):
    ...