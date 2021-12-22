"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ==============================================================================

import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

# ==============================================================================

class FileSelectionWidget(QtGui.QDialog):

    """ 
    A dialog that allows the user to select or create, and then load a file.

    "Select File" opens a QFileDialog (pyqt5) widget, restricted to accept only .iau files.
    "Create File" opens a FileCreationWidget, where the user can create an .iau file.
    "Load File" loads the selected file into a new analysis window.
    """
    
    def __init__(self):
        super(FileSelectionWidget, self).__init__()

        # Class variables
        self.file_path = ""

        # Subwidgets
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

        # Connections
        self.select_file_btn.clicked.connect(self.SelectFile)
        self.create_file_btn.clicked.connect(self.CreateFile)
        self.load_file_btn.clicked.connect(self.LoadFile)

    # --------------------------------------------------------------------------

    def SelectFile(self):
        """
        Gets file path and displays path in textbox.
        """

        self.file_path = QtGui.QFileDialog.getOpenFileName(self, "Select File", "", "(*.iau)")[0]
        self.select_file_txt.setText(self.file_path)

        # Enables "Load File" button if file path is valid
        if self.file_path != "":
            self.load_file_btn.setEnabled(True)
        else:
            self.load_file_btn.setEnabled(False)

    # --------------------------------------------------------------------------

    def CreateFile(self):
        """
        Opens a file creation dialog.
        """

        cfd = FileCreationWidget()
        cfd.exec_()

    # --------------------------------------------------------------------------

    def LoadFile(self):
        ...

# ==============================================================================

class FileCreationWidget(QtGui.QDialog):
    """
    A dialog that allows the user to create an .iau file from a data source.
    """
    
    def __init__(self):
        super(FileCreationWidget, self).__init__()

        # Class variables
        self.file_path = ""
        self.data_source_file_path = ""
        self.dim_labels = "H, K, L"

        # Window attributes
        self.setWindowTitle("New File")

        # Subwidgets
        self.source_type_lbl = QtGui.QLabel("Source Type: ")
        self.source_type_cbx = QtGui.QComboBox()
        self.source_type_cbx.addItems([".vti"])
        self.data_source_lbl = QtGui.QLabel("Data Source: ")
        self.data_source_txt = QtGui.QLineEdit()
        self.data_source_txt.setReadOnly(True)
        self.data_source_btn = QtGui.QPushButton("Browse")
        self.dim_labels_lbl = QtGui.QLabel("Dimension Labels: ")
        self.dim_labels_txt = QtGui.QLineEdit()
        self.dim_labels_txt.setText(self.dim_labels)
        self.save_as_lbl = QtGui.QLabel("Save File As: ")
        self.save_as_txt = QtGui.QLineEdit()
        self.save_as_txt.setReadOnly(True)
        self.save_as_btn = QtGui.QPushButton("Browse")
        self.cancel_btn = QtGui.QPushButton("Cancel")
        self.create_file_btn = QtGui.QPushButton("Create File")
        self.create_file_btn.setDefault(True)
        self.create_file_btn.setEnabled(False)

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.source_type_lbl, 0, 0, 1, 2)
        self.layout.addWidget(self.source_type_cbx, 0, 2, 1, 4)
        self.layout.addWidget(self.data_source_lbl, 1, 0, 1, 2)
        self.layout.addWidget(self.data_source_txt, 1, 2, 1, 2)
        self.layout.addWidget(self.data_source_btn, 1, 4, 1, 2)
        self.layout.addWidget(self.dim_labels_lbl, 2, 0, 1, 2)
        self.layout.addWidget(self.dim_labels_txt, 2, 2, 1, 4)
        self.layout.addWidget(self.save_as_lbl, 3, 0, 1, 2)
        self.layout.addWidget(self.save_as_txt, 3, 2, 1, 2)
        self.layout.addWidget(self.save_as_btn, 3, 4, 1, 2)
        self.layout.addWidget(self.cancel_btn, 4, 0, 1, 2)
        self.layout.addWidget(self.create_file_btn, 4, 4, 1, 2)

        # Connections
        self.data_source_btn.clicked.connect(self.SelectDataSource)
    
    # --------------------------------------------------------------------------

    def SelectDataSource(self):
        """
        Gets data source file path and displays path in textbox.
        """

        self.data_source_file_path = QtGui.QFileDialog.getOpenFileName(self, \
            "Select Data Source", "", f"(*{self.source_type_cbx.currentText})")[0]
        self.data_source_txt.setText(self.data_source_file_path)

    # --------------------------------------------------------------------------