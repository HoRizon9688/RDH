import re
import zlib
import binascii
import numpy as np


def plus(str):
    # Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    return str.zfill(8)


def encode(s):
    return ''.join([bin(ord(c)).replace('0b', '') for c in s])


def get_key2(photo):
    f = open(photo, mode='rb')
    x = np.fromfile(f, dtype=np.ubyte)
    hex_data = ''
    print(x, len(x))
    print(x[len(x)-1])
    for i in range(0, len(x)-1):
        hex_data = hex_data + plus(bin(int(str(x[i]))).replace('0b', ''))
    a = bin(int(str(x[1]))).replace('0b', '')
    print(a, type(a))
    print(hex_data[0:256])
    return hex_data
    #print(x)


def get_key():
    f = open('std_photo3.jpg', 'rb')
    image_data = str(f.read())
    print(image_data)
get_key2("std_photo3.jpg")
