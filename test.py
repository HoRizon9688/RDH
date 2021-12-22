from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt


# img = Image.open('test.bmp')
# img_PIL = np.array(img)
# width = img.size[0]
# height = img.size[1]
# print("width:" + str(width))
# print("height:" + str(height) + "\n")
# print(img_PIL)
#


width = 512
height = 1024

result = min(width//8, height//8)
print(result)
string = "Python"
text = ''
binary_converted = ' '.join(map(bin, bytearray(string, "utf-8"))).replace('0b', '')
print("The Binary Represntation is:", binary_converted)
print(len(binary_converted))
asc2 = binary_converted.split(' ')
for i in asc2:
    text += chr(int(i, 2))
print(text)
