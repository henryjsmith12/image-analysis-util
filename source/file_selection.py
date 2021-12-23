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
import vtk
from vtk.util import numpy_support as npSup # type: ignore

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
        self.select_file_btn.clicked.connect(self.selectFile)
        self.create_file_btn.clicked.connect(self.createFile)
        self.load_file_btn.clicked.connect(self.loadFile)

    # --------------------------------------------------------------------------

    def selectFile(self):
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

    def createFile(self):
        """
        Opens a file creation dialog.
        """

        cfd = FileCreationWidget()
        cfd.exec_()
        
        self.file_path = cfd.new_file_path
        self.select_file_txt.setText(self.file_path)

        # Enables "Load File" button if file path is valid
        if self.file_path != "":
            self.load_file_btn.setEnabled(True)
        else:
            self.load_file_btn.setEnabled(False)

    # --------------------------------------------------------------------------

    def loadFile(self):
        ...

# ==============================================================================

class FileCreationWidget(QtGui.QDialog):
    """
    A dialog that allows the user to create an .iau file from a data source.
    """
    
    def __init__(self):
        super(FileCreationWidget, self).__init__()

        # Class variables
        self.data_source_file_path = ""
        self.new_file_dim_labels = "H, K, L"
        self.new_file_path = ""
        self.new_file_data = None
        self.new_file_axes = None
        self.new_file_metadata = None

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
        self.new_file_dim_labels_lbl = QtGui.QLabel("Dimension Labels: ")
        self.new_file_dim_labels_txt = QtGui.QLineEdit()
        self.new_file_dim_labels_txt.setText(self.new_file_dim_labels)
        self.create_file_btn = QtGui.QPushButton("Save and Create File")
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
        self.layout.addWidget(self.new_file_dim_labels_lbl, 2, 0, 1, 2)
        self.layout.addWidget(self.new_file_dim_labels_txt, 2, 2, 1, 4)
        self.layout.addWidget(self.create_file_btn, 3, 4, 1, 2)

        # Connections
        self.data_source_btn.clicked.connect(self.selectDataSource)
        self.create_file_btn.clicked.connect(self.accept)
    
    # --------------------------------------------------------------------------

    def selectDataSource(self):
        """
        Gets data source file path and displays path in textbox.
        """

        self.data_source_file_path = QtGui.QFileDialog.getOpenFileName(self, "Open File", \
            "", f"(*{self.source_type_cbx.currentText()})")[0]

        self.data_source_txt.setText(self.data_source_file_path)

        # Enables "Load File" button if data source is valid
        if self.data_source_file_path != "":
            self.create_file_btn.setEnabled(True)
        else:
            self.create_file_btn.setEnabled(False)

    # --------------------------------------------------------------------------

    def accept(self):
        """
        Calls functions to save and create new file.
        """

        self.selectNewFileLocation()
        self.loadDataSource()
        self.createNewFile()
        self.close()
        
    # --------------------------------------------------------------------------
    
    def selectNewFileLocation(self):
        """
        Gets file path for new file.
        """

        self.new_file_path = QtGui.QFileDialog.getSaveFileName(self, "Save As", "", "*.iau")[0]

    # --------------------------------------------------------------------------

    def loadDataSource(self):
        """
        Loads data and axes from data source.
        """

        # .vti
        if self.data_source_file_path.endswith(".vti"):
            self.new_file_data, self.new_file_axes = DataSource.loadVTIDataSource(self.data_source_file_path)

    # --------------------------------------------------------------------------

    def createNewFile(self):
        """
        Creates .iau file with data, axes, and labels.
        """

        # Utilizes HDF5 file formatting
        new_file = h5py.File(self.new_file_path, 'a')
        new_file.create_dataset("data", data=self.new_file_data)
        new_file.create_group("coords")

        # Adds scale for each axis
        for i in range(len(self.new_file_axes)):
            axis = np.array(self.new_file_axes[i])
            new_file.create_dataset(f"coords/axis_{i}", data=axis)
            new_file["data"].dims[i].label = self.new_file_dim_labels[i]
            new_file[f"coords/axis_{i}"].make_scale(self.new_file_dim_labels[i])
            new_file["data"].dims[i].attach_scale(new_file[f"coords/axis_{i}"])

# ==============================================================================

class DataSource:
    """
    Functions for loading data from particular data sources.
    """
    
    def loadVTIDataSource(file_path):
        """
        Reads data and axes from 
        """

        # Reads the VTK XML ImageData file format
        data_reader = vtk.vtkXMLImageDataReader()
        data_reader.SetFileName(file_path)
        data_reader.Update()

        raw_data = data_reader.GetOutput()
        dimensions = list(raw_data.GetDimensions())
        
        data = npSup.vtk_to_numpy(raw_data.GetPointData().GetArray('Scalars_'))
        data = data.reshape(dimensions)
        
        origin = raw_data.GetOrigin() # First point for each axis
        spacing = raw_data.GetSpacing() # Space between points for each axis
        extent = raw_data.GetExtent() # First and last index of each axis

        axis_0, axis_1, axis_2 = [], [], []

        # Adds values to each axis accordingly
        for point in range(extent[0], extent[1] + 1):
            axis_0.append(origin[0] + point * spacing[0])
        for point in range(extent[2], extent[3] + 1):
            axis_1.append(origin[1] + point * spacing[1])
        for point in range(extent[4], extent[5] + 1):
            axis_2.append(origin[2] + point * spacing[2])

        # A list of lists of varying lengths
        axes = [axis_0, axis_1, axis_2]

        return data, axes