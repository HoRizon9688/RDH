import copy
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


def bit_img2img(bit_img):
    height = bit_img.shape[0]
    width = bit_img.shape[1]
    np_img = np.zeros((height, width), dtype=int)
    for i in range(height):
        for j in range(width):
            decimal_sum = 0
            for k in range(0, 8):
                decimal_sum += bit_img[i, j, k] * 2 ** k
            np_img[i, j] = decimal_sum
    return np_img


img = Image.open('test.bmp')
img_PIL = np.array(img)
width = img_PIL.shape[1]
height = img_PIL.shape[0]
print("width:" + str(width))
print("height:" + str(height))

# 打印原图片
plt.imshow(img_PIL, cmap="gray")
plt.axis('off')
plt.show()

# print(img_PIL)  # 二维数组


encrypt_key = np.random.randint(0, 2, (height, width, 8))
# print(encrypt_key)

bit_img = np.zeros((height, width, 8), dtype=int)

# bit_img为异或加密后的二进制图片
for i in range(height):
    for j in range(width):
        temp = img_PIL[i, j]
        for k in range(0, 8):
            bit_img[i, j, k] = math.floor(temp / 2 ** k) % 2
            bit_img[i, j, k] = bit_img[i, j, k] ^ encrypt_key[i, j, k]

# print("加密后二进制数据")
# print(bit_img)

# 将二进制图片转换为十进制，方便打印
# encrypted_img = bit_img2img(bit_img)
# plt.imshow(encrypted_img, cmap="gray")
# plt.axis('off')
# plt.show()

# 加密部分
#########################################################################
# 嵌入部分


block_size = 8
block_num = min(height//block_size, width//block_size)
print("block_num:", block_num)

embed_key = np.random.randint(0, 2, (block_num * block_size, block_num * block_size))

random_msg = np.random.randint(0, 2, (block_num, block_num))

# print("原图像二进制数据")
# print(bit_img)

# print("隐藏密钥")
# print(embed_key)
# print("嵌入信息")
# print(random_msg)

# 嵌入信息
for i in range(block_num):
    for j in range(block_num):
        if random_msg[i, j] == 0:  # 嵌入信息为0则翻转S0集合的后三位
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
# print("嵌入后图片二进制数据")
# print(bit_img)

# 打印嵌入信息后图片
np_img = bit_img2img(bit_img)
plt.imshow(np_img, cmap="gray")
plt.axis('off')
plt.show()

# 加密后的图片再次异或完成解密
for i in range(height):
    for j in range(width):
        for k in range(0, 8):
            bit_img[i, j, k] = bit_img[i, j, k] ^ encrypt_key[i, j, k]

# 打印解密后图片
np_img = bit_img2img(bit_img)
plt.imshow(np_img, cmap="gray")
plt.axis('off')
plt.show()

# print("解密后")
# print(np_img)


# 块恢复和嵌入信息提取
H0 = bit_img.copy()  # 将每个块中的S0集合翻转，S1不变
H1 = bit_img.copy()  # 将每个块中的S1集合翻转，S0不变

for i in range(block_num):
    for j in range(block_num):
        for k1 in range(i * block_size, (i + 1) * block_size):
            for k2 in range(j * block_size, (j + 1) * block_size):
                if embed_key[k1, k2] == 0:  # 翻转S0
                    for k3 in range(3):
                        if bit_img[k1, k2, k3] == 0:
                            H0[k1, k2, k3] = 1
                        else:
                            H0[k1, k2, k3] = 0
for i in range(block_num):
    for j in range(block_num):
        for k1 in range(i * block_size, (i + 1) * block_size):
            for k2 in range(j * block_size, (j + 1) * block_size):
                if embed_key[k1, k2] == 1:
                    for k3 in range(3):
                        if bit_img[k1, k2, k3] == 0:
                            H1[k1, k2, k3] = 1
                        else:
                            H1[k1, k2, k3] = 0

H0 = bit_img2img(H0)
H1 = bit_img2img(H1)
# print("H0\n", H0)
# print("H1\n", H1)

recover_img = np.zeros((height, width), dtype=int)

for i in range(block_num):
    for j in range(block_num):
        f0 = 0
        f1 = 0
        for k1 in range(i * block_size + 2, (i + 1) * block_size - 1):
            for k2 in range(j * block_size + 2, (j + 1) * block_size - 1):
                f0 += abs(H0[k1, k2] - (H0[k1-1, k2] + H0[k1, k2-1] + H0[k1+1, k2] + H0[k1, k2+1]) / 4)
                f1 += abs(H1[k1, k2] - (H1[k1 - 1, k2] + H1[k1, k2 - 1] + H1[k1 + 1, k2] + H1[k1, k2 + 1]) / 4)
        if f0 < f1:
            for h in range(i * block_size, (i + 1) * block_size):
                for w in range(j * block_size, (j + 1) * block_size):
                    recover_img[h, w] = H0[h, w]
        else:
            for h in range(i * block_size, (i + 1) * block_size):
                for w in range(j * block_size, (j + 1) * block_size):
                    recover_img[h, w] = H1[h, w]
# print(recover_img)

# 打印块恢复后图片
plt.imshow(recover_img, cmap="gray")
plt.axis('off')
plt.show()

# for i in range(block_num * block_size + 2, (block_num + 1) * block_size - 1):
#     for j in range(block_num * block_size + 2, (block_num + 1) * block_size - 1):
#         f0 += abs(H0[i, j] - (H0[i-1, j] + H0[i, j-1] + H0[i+1, j] + H0[i, j+1]) / 4)
#         f1 += abs(H1[i, j] - (H1[i-1, j] + H1[i, j-1] + H1[i+1, j] + H1[i, j+1]) / 4)
