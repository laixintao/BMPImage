#coding:utf-8
__author__ = 'laixintao'
import struct

class BMPImage(object):
    def __init__(self,filename):
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
        # self.info = struct.unpack("p",self.__file.read(1024))
        self.info = []
        for i in range(1024):
            self.info.append(struct.unpack('B',self.__file.read(1))[0])
        self.__file.close()
        if self.signature[0]!="B" or self.signature[1]!="M":
            raise IOError("Not a bmp file!")

    def show_info(self):
        d = self.__dict__
        for key in d:
            if key.startswith("_"):
                pass
            else:
                print key,"----",d[key]

    def print_byte(self):
        f = open(self.filename)
        for i in range(1000):
            for j in range(1000):
                print struct.unpack("b",f.read(1))[0],
            print ""

    def write_to_new_file(self,filename,threshold=108):
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
        oldfile=open(self.filename)
        oldfile.seek(self.offset)
        for i in range(self.width):
            for j in range(self.height):
                value = struct.unpack("B",oldfile.read(1))[0]
                print value,
                if value>threshold:value = 255
                else :value=0
                f.write(struct.pack("B",value))
            print ""
        oldfile.close()
        f.close()

if __name__=="__main__":
    image = BMPImage("test.bmp")
    image.show_info()
    image.write_to_new_file("new2.bmp")