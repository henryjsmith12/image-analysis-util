"""
Tests for io.py
"""

# ----------------------------------------------------------------------------------

from curses import meta
import numpy as np
import os
import unittest

from iautil import io

# ----------------------------------------------------------------------------------

class TestIO(unittest.TestCase):

    def setUp(self):
        self.scan40_iau_path = os.path.abspath("tests/test_files/scan40.iau")
        self.scans_vti_path = os.path.abspath("tests/test_files")
        self.scan40_vti_path = os.path.abspath("tests/test_files/scan40.vti")
        if os.path.exists(self.scan40_iau_path):
            os.remove(self.scan40_iau_path)

    def test_create_iau_success(self):
        io.create_iau(
            iau_path=self.scan40_iau_path,
            data=np.array([[1, 2, 3], [4, 5, 6]]),
            coords=[[-10, -5], [5, 10, 15]],
            dims=["a", "b"],
            metadata={"name" : "scan40"}
        )

    def test_create_iau_no_iau_path(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(iau_path=None, data=None)
        self.assertEqual(str(context.exception), "IAU path not given.")
    
    def test_create_iau_non_string_iau_path(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(42, None)
        self.assertEqual(str(context.exception), "IAU path must be a string.")

    def test_create_iau_no_data(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(iau_path=self.scan40_iau_path, data=None)
        self.assertEqual(str(context.exception), "data not given.")

    def test_create_iau_non_ndarray_data(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(iau_path=self.scan40_iau_path, data=42)
        self.assertEqual(str(context.exception), "data must be a numpy ndarray.")

    def test_create_iau_non_list_coords(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(
                iau_path=self.scan40_iau_path, 
                data=np.array([[1, 2, 3], [4, 5, 6]]),
                coords=42
            )
        self.assertEqual(str(context.exception), "coords must be a list.")

    def test_create_iau_non_list_dims(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(
                iau_path=self.scan40_iau_path, 
                data=np.array([[1, 2, 3], [4, 5, 6]]),
                dims=42
            )
        self.assertEqual(str(context.exception), "dims must be a list.")

    def test_create_iau_non_dict_metadata(self):
        with self.assertRaises(ValueError) as context:
            io.create_iau(
                iau_path=self.scan40_iau_path, 
                data=np.array([[1, 2, 3], [4, 5, 6]]),
                metadata=42
            )
        self.assertEqual(str(context.exception), "metadata must be a dictionary.")

    def test_create_iau_coords_dims_mismatched_ndims(self):
        with self.assertRaises(RuntimeError) as context:
            io.create_iau(
                iau_path=self.scan40_iau_path,
                data=np.array([[1, 2, 3], [4, 5, 6]]),
                coords=[[-10, -5]],
                dims=["a", "b"]
            )
        self.assertEqual(str(context.exception), "Dimension sizes for coords and dims do not match.")

    def test_vti_to_iau_3d_successful(self):

        io.vti_to_iau(
            vti_path=self.scan40_vti_path,
            iau_path=self.scan40_iau_path
        )
    
    def test_vti_to_iau_4d_successful(self):

        io.vti_to_iau(
            vti_path=self.scans_vti_path,
            iau_path=self.scan40_iau_path
        )

    def tearDown(self):
        if os.path.exists(self.scan40_iau_path):
            os.remove(self.scan40_iau_path)
