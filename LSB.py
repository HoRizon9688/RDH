import numpy as np
from PIL import Image


def mod(x, y):
    return x % y


def plus(str):
    return str.zfill(8)


def get_key2(photo):
    f = open(photo, mode='rb')
    x = np.fromfile(f, dtype=np.ubyte)
    hex_data = ''
    print("图片信息长度:", len(x))
    for i in range(0, len(x)):
        hex_data = hex_data + plus(bin(int(str(x[i]))).replace('0b', ''))
    # f = open("data.txt", 'a')
    # f.write(hex_data)
    return hex_data


def func(str1, str2, str3):
    im = Image.open(str1)
    width = im.size[0]
    print("width:" + str(width) + "\n")
    height = im.size[1]
    print("height:" + str(height) + "\n")
    count = 0
    # 获取需要隐藏的信息
    key = get_key2(str2)
    keylen = len(key)
    for h in range(0, height):
        for w in range(0, width):
            pixel = im.getpixel((w, h))
            a = pixel[0]
            b = pixel[1]
            c = pixel[2]
            if count == keylen:
                break

            a = a - mod(a, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            b = b - mod(b, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            c = c - mod(c, 2) + int(key[count])
            count += 1
            if count == keylen:
                im.putpixel((w, h), (a, b, c))
                break
            if count % 3 == 0:
                im.putpixel((w, h), (a, b, c))
    im.save(str3)


old = "1.png"  #载体图片
enc = "std_photo3.jpg"  #隐藏的内容
new = "LSB.png"  #输出图片

func(old, enc, new)
