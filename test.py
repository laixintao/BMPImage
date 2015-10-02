#!image/bin/python

__author__ = 'laixintao'

import unittest
import os

from main import BMPImage

class BMPImageTestCase(unittest.TestCase):
    def setUp(self):
        self.bmp = BMPImage("test.bmp")
        self.new_file = "temp_test.bmp"

    def test_bmp_exists(self):
        self.assertTrue(self.bmp is not None)

    def test_write_to_new_file(self):
        self.assertTrue(self.bmp.write_to_new_file(self.new_file,
                                          108))
    def tearDown(self):
        # os.remove(self.new_file)
        pass

if __name__ == "__main__":
    unittest.main()