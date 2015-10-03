#!image/bin/python

__author__ = 'laixintao'

import unittest
import os
# from Binaryzation import Binaryzation
from BMPImage import BMPImage

class BMPImageTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = "LENA.bmp"
        self.bmp = BMPImage()
        self.bmp.open(filename=self.filename)
        # self.new_file = "temp_test.bmp"

    def test_bmp_exists(self):
        self.assertTrue(self.bmp is not None)

    def test_is_bmp_file(self):
        self.assertTrue(self.bmp.is_bmp_file(
            self.filename))

    def test_get_image_info(self):
        self.assertTrue(isinstance(
            self.bmp.data,list ))

    def test_binaryzation_by_mean(self):
        self.assertTrue(isinstance(
            self.bmp.binaryzation(),list))
        self.assertTrue(self.bmp.write_to_new_file("test.bmp"))

    def test_binaryzation_by_PTile(self):
        self.assertTrue(isinstance(
            self.bmp.binaryzation(method="P-Tile"),list
        ))
        self.assertTrue(self.bmp.write_to_new_file("test.bmp"))

    def tearDown(self):
        for filename in os.listdir("."):
            print filename
        pass

if __name__ == "__main__":
    unittest.main()