from img_process import *
from msg_key_gen import *
from embed_extract import *


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


# width, height, np_img = open_img("test1.bmp")
# encrypt_key = encrypt_key_gen(np_img)

# encrypt_key = key_load("encrypt_key.npy")
# print(encrypt_key)

# 判断客户端提取的信息服务器嵌入的信息是否相等
server_msg = msg_read("test.npy")
client_msg = msg_read("server_test.npy")

print((server_msg == client_msg).all())
