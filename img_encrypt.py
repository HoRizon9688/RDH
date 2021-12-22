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


img = Image.open('test1.bmp')
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

# print(bit_img)
# 将二进制图片转换为十进制，方便打印
encrypted_img = np.zeros((height, width), dtype=int)
for i in range(height):
    for j in range(width):
        decimal_sum = 0
        for k in range(0, 8):
            decimal_sum += bit_img[i, j, k] * 2 ** k
        encrypted_img[i, j] = decimal_sum
# print(encrypted_img)

plt.imshow(encrypted_img, cmap="gray")
plt.axis('off')
plt.show()


embed_key = np.random.randint(0, 2, (height, width))

block_size = 8
block_num = min(height//block_size, width//block_size)
print("block_num:", block_num)
random_msg = np.random.randint(0, 2, (height // block_size, width // block_size))

# print("原图像二进制数据")
# print(bit_img)
# print("隐藏密钥")
# print(embed_key)
# print("嵌入信息")
# print(random_msg)

# 嵌入信息
for i in range(block_num):
    for j in range(block_num):
        if random_msg[i, j] == 0:
            for k1 in range(i * block_size, (i + 1) * block_size):
                for k2 in range(j * block_size, (j + 1) * block_size):
                    if embed_key[k1, k2] == 0:
                        for k3 in range(3):
                            if bit_img[k1, k2, k3] == 0:
                                bit_img[k1, k2, k3] = 1
                            else:
                                bit_img[k1, k2, k3] = 0
        else:
            for k1 in range(i * block_size, (i + 1) * block_size):
                for k2 in range(j * block_size, (j + 1) * block_size):
                    if embed_key[k1, k2] == 1:
                        for k3 in range(3):
                            if bit_img[k1, k2, k3] == 0:
                                bit_img[k1, k2, k3] = 1
                            else:
                                bit_img[k1, k2, k3] = 0
# print("嵌入后图片二进制数据")
# print(bit_img)
np_img = bit_img2img(bit_img)
plt.imshow(np_img, cmap="gray")
plt.axis('off')
plt.show()

# 加密后的图片再次异或完成解密
for i in range(height):
    for j in range(width):
        for k in range(0, 8):
            bit_img[i, j, k] = bit_img[i, j, k] ^ encrypt_key[i, j, k]

np_img = bit_img2img(bit_img)
plt.imshow(np_img, cmap="gray")
plt.axis('off')
plt.show()
