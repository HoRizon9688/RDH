from img_process import *
from msg_key_gen import *
from embed_extract import *


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


width, height, np_img = open_img("test3.bmp")
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
# print(bit_msg)
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

recover_np_img, extract_msg = recover_extract_rand(block_size, block_num, decrypt_bit_img, embed_key)
merge_np_img = merge_recover_img(block_size, block_num, decrypt_np_img, recover_np_img)

# print(recover_np_img)
# print(merge_np_img)
# print((recover_np_img == merge_np_img).all())

# 提取的嵌入信息
# print(extract_msg)

# 打印恢复后图片
plt.imshow(merge_np_img, cmap="gray")
plt.axis('off')
plt.show()
