from Utils.msg_key_gen import *
from Utils.embed_extract import *
import os

def np_img_save(np_img, img_name):
    rgb_img = Image.fromarray(np_img).convert('RGB')
    rgb_img.save(img_name)
    gray_img = Image.open(img_name).convert('L')
    gray_img.save(img_name)


def encrypt_key_gen(np_img):
    width = np_img.shape[1]
    height = np_img.shape[0]
    encrypt_key = np.random.randint(0, 2, (height, width, 8))
    np.save("encrypt_key.npy", encrypt_key)
    return encrypt_key


def key_load(key_type):
    key = np.load(key_type)
    return key


def msg_read(extract_msg_name):
    msg = np.load(extract_msg_name)
    return msg


def get_bmp_file(file_path):
    dir_file = os.listdir(file_path)
    bmp_file = []
    for file in dir_file:
        if file.endswith(".bmp"):
            bmp_file.append(file)
    return bmp_file

# 判断客户端提取的信息服务器嵌入的信息是否相等
# server_msg = msg_read("test.npy")
# client_msg = msg_read("server_test.npy")
# print((server_msg == client_msg).all())


# dir_file = os.listdir('./')
# bmp_file = []
# print(dir_file)
# for file in dir_file:
#     if file.endswith(".bmp"):
#         # print(os.path.join(file))
#         bmp_file.append(file)
# print(bmp_file)

print(get_bmp_file("C:/Users/HoRizon/PycharmProjects/RDH/Server/"))