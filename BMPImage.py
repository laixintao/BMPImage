#coding:utf-8
__author__ = 'laixintao'

import struct

class NotBMPFileError(Exception):
    pass

class BMPImage(object):

    @staticmethod
    def is_bmp_file(file):
        "Check if the file is a bmpfile"
        #todo:could be called by object without *file*
        try:
            f = open(file)
            signature = [struct.unpack("c",f.read(1))[0],
                         struct.unpack("c",f.read(1))[0]]
        except IOError,e:
            print e
        finally:
            f.close()
        if signature[0]=="B" and signature[1]=="M":
            return True
        else:
            raise NotBMPFileError

    def open(self,filename):
        "open a bmp file"
        # todo :should be a static method
        BMPImage.is_bmp_file(filename)
        try:
            self.__file = open(filename)
            self.filename=filename
            self.signature = [struct.unpack("c",self.__file.read(1))[0],
                              struct.unpack("c",self.__file.read(1))[0]]

            self.size = struct.unpack("i",self.__file.read(4))[0]
            self.reserved = struct.unpack("i",self.__file.read(4))[0]
            self.offset = struct.unpack("i",self.__file.read(4))[0]
            self.hdr_size = struct.unpack("i",self.__file.read(4))[0]
            self.width = struct.unpack("i",self.__file.read(4))[0]
            self.height = struct.unpack("i",self.__file.read(4))[0]
            self.nr_planes = struct.unpack("h",self.__file.read(2))[0]
            self.bit_per_pixel = struct.unpack("h",self.__file.read(2))[0]
            self.compress_type = struct.unpack("i",self.__file.read(4))[0]
            self.data_size = struct.unpack("i",self.__file.read(4))[0]
            self.resol_hori = struct.unpack("i",self.__file.read(4))[0]
            self.resol_vert = struct.unpack("i",self.__file.read(4))[0]
            self.nr_colors = struct.unpack("i",self.__file.read(4))[0]
            self.important_colors = struct.unpack("i",self.__file.read(4))[0]
            self.info = []
            self.data = []
            self.hist = {}.fromkeys([i for i in range(256)],0)
            for i in range(1024):
                self.info.append(struct.unpack('B',self.__file.read(1))[0])
            self.__file.seek(self.offset)
            for i in range(self.width):
                for j in range(self.height):
                    value = struct.unpack("B",self.__file.read(1))[0]
                    self.data.append(value)
                    self.hist[value]+=1
        except IOError,e:
            print e
        finally:
            self.__file.close()

    def __init__(self,filename="__None"):
        self.is_binaryzation = False
        self.binaryzation_data = []
        self.binaryzation_method = None
        if filename != "__None":
            self.open(filename)
        else:
            pass

    def get_image_info(self):
        return self.data

    def write_to_new_file(self,filename,filedata="bzdata"):
        if filedata == "bzdata":
            data = self.binaryzation_data
            filename = "binary_"+\
                       self.binaryzation_method+"_"+filename
        f = open(filename,"wb")
        f.write(struct.pack("c",self.signature[0]))
        f.write(struct.pack("c",self.signature[1]))
        f.write(struct.pack("i",self.size))
        f.write(struct.pack("i",self.reserved))
        f.write(struct.pack("i",self.offset))
        f.write(struct.pack("i",self.hdr_size))
        f.write(struct.pack("i",self.width))
        f.write(struct.pack("i",self.height))
        f.write(struct.pack("h",self.nr_planes))
        f.write(struct.pack("h",self.bit_per_pixel))
        f.write(struct.pack("i",self.compress_type))
        f.write(struct.pack("i",self.data_size))
        f.write(struct.pack("i",self.resol_hori))
        f.write(struct.pack("i",self.resol_vert))
        f.write(struct.pack("i",self.nr_colors))
        f.write(struct.pack("i",self.important_colors))
        for i in range(1024):
            f.write(struct.pack("B",self.info[i]))
        for j in data:
            f.write(struct.pack("B",j))
        f.close()
        return True

    def binaryzation(self,method="mean",threshold=None):
        "binaryzation for a bmp image"
        # choose a method,default is mean
        self.is_binaryzation = True
        self.binaryzation_method = method
        if threshold is not None:
            self.binaryzation_method = "threshold"+str(threshold)
        elif method == "mean":
            threshold = self.threshold_by_mean()
        elif method == "P-Tile":
            pass
        tempdata = []
        for i in self.data:
            if i>threshold: i=255
            else: i=0
            tempdata.append(i)
        self.binaryzation_data = tempdata
        return self.binaryzation_data


    def threshold_by_mean(self):
        hist = self.hist
        Sum = 0
        Amount = 0
        for i in range(256):
            Amount += hist[i]
            Sum += hist[i] * i
        return Sum/Amount

    def threshold_by_PTile(self):
        pass


if __name__=="__main__":
    file = BMPImage("test.bmp")
    # print file.get_image_info()
    file.binaryzation(threshold=50)
    print "---"
    # print file.get_image_info()
    # print file.hist
    file.write_to_new_file("new_test.bmp")