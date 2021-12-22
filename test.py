from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
import re


def random_msg_gen(block_num):
    random_msg = np.random.randint(0, 2, (block_num, block_num))
    return random_msg


def msg_gen(msg):
    bit_msg = ' '.join(map(bin, bytearray(msg, "utf-8"))).replace('0b', '').replace(' ', '')
    return bit_msg


def msg_recover(bit_msg):
    msg = ''
    asc2 = re.findall('.{7}', bit_msg)
    # print(asc2)
    # asc2 = bit_msg.split(' ')
    for i in asc2:
        msg += chr(int(i, 2))
    return msg


# random_msg = random_msg_gen(2)
# print(random_msg)

# bit_msg = msg_gen("Python")
# print(bit_msg, len(bit_msg))
# text = msg_recover(bit_msg)
# print(text)
