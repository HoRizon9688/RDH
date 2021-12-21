from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


# 打开图片并返回图片的np数组
def open_img(img_name):
    img = Image.open(img_name)
    np_img = np.array(img)
    width = img.size[0]
    height = img.size[1]
    print("width:" + str(width))
    print("height:" + str(height) + "\n")
    # 打印原图片
    plt.imshow(np_img, cmap="gray")
    plt.axis('off')
    plt.show()
    # print(np_img)  # 二维数组
    return np_img


# 将十进制np数组表示的图片转换为二进制
def img2bit_img(np_img):
    width = np_img.shape[0]
    height = np_img.shape[1]
    bit_img = np.zeros((width, height, 8), dtype=int)
    for i in range(width):
        for j in range(height):
            temp = np_img[i, j]
            for k in range(0, 8):
                bit_img[i, j, k] = math.floor(temp / 2 ** k) % 2
    return bit_img


# 将二进制表示的图片转为十进制
def bit_img2img(bit_img):
    width = bit_img.shape[0]
    height = bit_img.shape[1]
    np_img = np.zeros((width, height), dtype=int)
    for i in range(width):
        for j in range(height):
            decimal_sum = 0
            for k in range(0, 8):
                decimal_sum += bit_img[i, j, k] * 2 ** k
            np_img[i, j] = decimal_sum
    return np_img


def encrypt_key_gen(np_img):
    width = np_img.shape[0]
    height = np_img.shape[1]
    encrypt_key = np.random.randint(0, 2, (width, height, 8))
    return encrypt_key


def embed_key_gen(np_img):
    width = np_img.shape[0]
    height = np_img.shape[1]
    embed_key = np.random.randint(0, 2, (width, height))
    return embed_key


def xor_encrypt(encrypt_key, bit_img):
    width = bit_img.shape[0]
    height = bit_img.shape[1]
    for i in range(width):
        for j in range(height):
            for k in range(0, 8):
                bit_img[i, j, k] = bit_img[i, j, k] ^ encrypt_key[i, j, k]
    return bit_img





np_img = open_img("test1.bmp")
bit_img = img2bit_img(np_img)
encrypt_key = encrypt_key_gen(np_img)
encrypted_img = xor_encrypt(encrypt_key, bit_img)
print(encrypt_key)
print(encrypted_img)
