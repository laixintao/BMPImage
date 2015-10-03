#!image/bin/python

__author__ = 'laixintao'

import unittest
import os

from BMPImage import BMPImage

class BMPImageTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = "test.bmp"
        self.bmp = BMPImage()
        self.bmp.open(filename=self.filename)
        self.new_file = "temp_test.bmp"

    def test_bmp_exists(self):
        self.assertTrue(self.bmp is not None)

    def test_is_bmp_file(self):
        self.assertTrue(self.bmp.is_bmp_file(
            self.filename
        ))

    def test_get_image_info(self):
        self.assertTrue(isinstance(
            self.bmp.data,list
        ))

    def test_binaryzation(self):
        self.assertTrue(isinstance(
            self.bmp.binaryzation(),list
        ))
    def test_write_to_new_file(self):
        self.assertTrue(self.bmp.write_to_new_file(self.new_file,
                                          108))
    def tearDown(self):
        if os.path.isfile(self.new_file):
            os.remove(self.new_file)
        pass

if __name__ == "__main__":
    unittest.main()