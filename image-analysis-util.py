"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ==============================================================================

import pyqtgraph as pg
from pyqtgraph import QtGui

from source.file_selection import FileSelectionWidget

# ==============================================================================

app = pg.mkQApp("image-analysis-util")
file_selector = FileSelectionWidget() # Allows user to select/create file to use
file_selector.show()
app.exec_()

