from img_process import bit_img2img
import numpy as np


# 嵌入随机生成的信息
def random_msg_embed(block_size, block_num, bit_img, bit_msg, embed_key):
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
    h0 = bit_img.copy()
    h1 = bit_img.copy()
    recover_np_img = np.zeros((block_num * block_size, block_num * block_size), dtype=int)
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

    h0 = bit_img2img(h0)  # 将每个块中的S0集合翻转，S1不变
    h1 = bit_img2img(h1)  # 将每个块中的S1集合翻转，S0不变

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


# 将恢复的像素重新填入解密后的图片（用于恢复非正方形的图片）
def merge_recover_img(block_size, block_num, decrypt_np_img, recover_np_img):
    merge_np_img = decrypt_np_img.copy()
    for i in range(block_num):
        for j in range(block_num):
            for h in range(i * block_size, (i + 1) * block_size):
                for w in range(j * block_size, (j + 1) * block_size):
                    merge_np_img[h, w] = recover_np_img[h, w]
    return merge_np_img

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
