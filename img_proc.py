from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
from img_process import *
from test import *

# 打开图片并返回图片的np数组
# def open_img(img_name):
#     img = Image.open(img_name)
#     np_img = np.array(img)
#     width = np_img.shape[1]
#     height = np_img.shape[0]
#     print("width:" + str(width))
#     print("height:" + str(height) + "\n")
#     # print(np_img)  # 二维数组
#     return width, height, np_img
#
#
# # 将十进制np数组表示的图片转换为二进制
# def img2bit_img(np_img):
#     width = np_img.shape[1]
#     height = np_img.shape[0]
#     bit_img = np.zeros((height, width, 8), dtype=int)
#     for i in range(height):
#         for j in range(width):
#             temp = np_img[i, j]
#             for k in range(0, 8):
#                 bit_img[i, j, k] = math.floor(temp / 2 ** k) % 2
#     return bit_img
#
#
# # 将二进制表示的图片转为十进制
# def bit_img2img(bit_img):
#     width = bit_img.shape[1]
#     height = bit_img.shape[0]
#     np_img = np.zeros((height, width), dtype=int)
#     for i in range(height):
#         for j in range(width):
#             decimal_sum = 0
#             for k in range(0, 8):
#                 decimal_sum += bit_img[i, j, k] * 2 ** k
#             np_img[i, j] = decimal_sum
#     return np_img


# # 异或加密（解密）
# def xor_encrypt(encrypt_key, bit_img):
#     width = bit_img.shape[1]
#     height = bit_img.shape[0]
#     for i in range(height):
#         for j in range(width):
#             for k in range(0, 8):
#                 bit_img[i, j, k] = bit_img[i, j, k] ^ encrypt_key[i, j, k]
#     return bit_img


def encrypt_key_gen(np_img):
    width = np_img.shape[1]
    height = np_img.shape[0]
    encrypt_key = np.random.randint(0, 2, (height, width, 8))
    return encrypt_key


def embed_key_gen(np_img):
    width = np_img.shape[1]
    height = np_img.shape[0]
    embed_key = np.random.randint(0, 2, (height, width))
    return embed_key


def random_msg_embed(block_size, block_num, bit_img, bit_msg, embed_key):
    count = 0
    msg_len = bit_msg.shape[0] * bit_msg.shape[1]
    print("msg_len:", msg_len)
    for i in range(block_num):
        for j in range(block_num):
            if bit_msg[i, j] == 0:
                for k1 in range(i * block_size, (i + 1) * block_size):
                    for k2 in range(j * block_size, (j + 1) * block_size):
                        if embed_key[k1, k2] == 0:
                            for k3 in range(3):  # 翻转后三位
                                if bit_img[k1, k2, k3] == 0:
                                    bit_img[k1, k2, k3] = 1
                                else:
                                    bit_img[k1, k2, k3] = 0
            else:
                for k1 in range(i * block_size, (i + 1) * block_size):
                    for k2 in range(j * block_size, (j + 1) * block_size):
                        if embed_key[k1, k2] == 1:
                            for k3 in range(3):  # 翻转后三位
                                if bit_img[k1, k2, k3] == 0:
                                    bit_img[k1, k2, k3] = 1
                                else:
                                    bit_img[k1, k2, k3] = 0
    return bit_img


# 块恢复和嵌入信息提取
def recover_extract_rand(block_size, block_num, bit_img, embed_key):
    h0 = bit_img.copy()  # 将每个块中的S0集合翻转，S1不变
    h1 = bit_img.copy()  # 将每个块中的S1集合翻转，S0不变
    recover_np_img = np.zeros((height, width), dtype=int)
    extract_msg = np.zeros((block_num, block_num), dtype=int)

    for i in range(block_num):
        for j in range(block_num):
            for k1 in range(i * block_size, (i + 1) * block_size):
                for k2 in range(j * block_size, (j + 1) * block_size):
                    if embed_key[k1, k2] == 0:  # 翻转S0
                        for k3 in range(3):
                            if bit_img[k1, k2, k3] == 0:
                                h0[k1, k2, k3] = 1
                            else:
                                h0[k1, k2, k3] = 0
    for i in range(block_num):
        for j in range(block_num):
            for k1 in range(i * block_size, (i + 1) * block_size):
                for k2 in range(j * block_size, (j + 1) * block_size):
                    if embed_key[k1, k2] == 1:
                        for k3 in range(3):
                            if bit_img[k1, k2, k3] == 0:
                                h1[k1, k2, k3] = 1
                            else:
                                h1[k1, k2, k3] = 0

    h0 = bit_img2img(h0)
    h1 = bit_img2img(h1)

    for i in range(block_num):
        for j in range(block_num):
            f0 = 0
            f1 = 0
            for k1 in range(i * block_size + 2, (i + 1) * block_size - 1):
                for k2 in range(j * block_size + 2, (j + 1) * block_size - 1):
                    f0 += abs(h0[k1, k2] - (h0[k1 - 1, k2] + h0[k1, k2 - 1] + h0[k1 + 1, k2] + h0[k1, k2 + 1]) / 4)
                    f1 += abs(h1[k1, k2] - (h1[k1 - 1, k2] + h1[k1, k2 - 1] + h1[k1 + 1, k2] + h1[k1, k2 + 1]) / 4)
            if f0 < f1:
                for h in range(i * block_size, (i + 1) * block_size):
                    for w in range(j * block_size, (j + 1) * block_size):
                        recover_np_img[h, w] = h0[h, w]
                extract_msg[i, j] = 0
            else:
                for h in range(i * block_size, (i + 1) * block_size):
                    for w in range(j * block_size, (j + 1) * block_size):
                        recover_np_img[h, w] = h1[h, w]
                extract_msg[i, j] = 1

    return recover_np_img, extract_msg


# def msg_embed(block_size, block_num, bit_img, bit_msg, embed_key):
#     count = 0
#     msg_len = len(bit_msg)
#     print("msg_len:", msg_len)
#     while count < msg_len:
#         for i in range(block_num):
#             for j in range(block_num):
#                 if bit_msg[count] == '0':
#                     for k1 in range(i * block_size, (i + 1) * block_size):
#                         for k2 in range(j * block_size, (j + 1) * block_size):
#                             if embed_key[k1, k2] == 0:
#                                 for k3 in range(3):  # 翻转后三位
#                                     if bit_img[k1, k2, k3] == 0:
#                                         bit_img[k1, k2, k3] = 1
#                                     else:
#                                         bit_img[k1, k2, k3] = 0
#                 else:
#                     for k1 in range(i * block_size, (i + 1) * block_size):
#                         for k2 in range(j * block_size, (j + 1) * block_size):
#                             if embed_key[k1, k2] == 1:
#                                 for k3 in range(3):  # 翻转后三位
#                                     if bit_img[k1, k2, k3] == 0:
#                                         bit_img[k1, k2, k3] = 1
#                                     else:
#                                         bit_img[k1, k2, k3] = 0
#         count += 1
#     return bit_img


width, height, np_img = open_img("test2.bmp")
block_size = 8
block_num = min(height//block_size, width//block_size)
msg_capacity = block_num * block_num

print("width:" + str(width))
print("height:" + str(height))
print("block_size:", block_size)
print("block_num:", block_num)
print("msg_capacity:", msg_capacity)

# 打印原图片
plt.imshow(np_img, cmap="gray")
plt.axis('off')
plt.show()

bit_img = img2bit_img(np_img)
encrypt_key = encrypt_key_gen(np_img)
encrypted_bit_img = xor_encrypt(encrypt_key, bit_img)


# 打印异或加密后图片
encrypted_np_img = bit_img2img(encrypted_bit_img)
plt.imshow(encrypted_np_img, cmap="gray")
plt.axis('off')
plt.show()

embed_key = embed_key_gen(np_img)

bit_msg = random_msg_gen(block_num)
print(bit_msg)
# bit_msg = msg_gen("A")

embed_bit_img = random_msg_embed(block_size, block_num, encrypted_bit_img, bit_msg, embed_key)

# 打印嵌入信息后图片
embed_np_img = bit_img2img(embed_bit_img)
plt.imshow(embed_np_img, cmap="gray")
plt.axis('off')
plt.show()

decrypt_bit_img = xor_encrypt(encrypt_key, embed_bit_img)

# 打印解密后图片
decrypt_np_img = bit_img2img(decrypt_bit_img)
plt.imshow(decrypt_np_img, cmap="gray")
plt.axis('off')
plt.show()

# 打印恢复后图片
recover_np_img, extract_msg = recover_extract_rand(block_size, block_num, decrypt_bit_img, embed_key)
print(extract_msg)
plt.imshow(recover_np_img, cmap="gray")
plt.axis('off')
plt.show()
