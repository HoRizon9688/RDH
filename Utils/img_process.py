from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


# 打开图片并返回图片的np数组
def open_img(img_name):
    img = Image.open(img_name)
    np_img = np.array(img)
    width = np_img.shape[1]
    height = np_img.shape[0]
    # print("width:" + str(width))
    # print("height:" + str(height) + "\n")
    # print(np_img)  # 二维数组
    return width, height, np_img


# 将np数组表示的灰度值转换为图片保存
def np_img_save(np_img, img_name):
    rgb_img = Image.fromarray(np_img).convert('RGB')
    rgb_img.save(img_name)
    gray_img = Image.open(img_name).convert('L')
    gray_img.save(img_name)


# 将十进制np数组表示的图片转换为二进制
def img2bit_img(np_img):
    width = np_img.shape[1]
    height = np_img.shape[0]
    bit_img = np.zeros((height, width, 8), dtype=int)
    for i in range(height):
        for j in range(width):
            temp = np_img[i, j]
            for k in range(0, 8):
                bit_img[i, j, k] = math.floor(temp / 2 ** k) % 2
    return bit_img


# 将二进制表示的图片转为十进制
def bit_img2img(bit_img):
    width = bit_img.shape[1]
    height = bit_img.shape[0]
    np_img = np.zeros((height, width), dtype=int)
    for i in range(height):
        for j in range(width):
            decimal_sum = 0
            for k in range(0, 8):
                decimal_sum += bit_img[i, j, k] * 2 ** k
            np_img[i, j] = decimal_sum
    return np_img


# 二进制图片异或加密解密
def xor_encrypt(encrypt_key, bit_img):
    width = bit_img.shape[1]
    height = bit_img.shape[0]
    for i in range(height):
        for j in range(width):
            for k in range(0, 8):
                bit_img[i, j, k] = bit_img[i, j, k] ^ encrypt_key[i, j, k]
    return bit_img