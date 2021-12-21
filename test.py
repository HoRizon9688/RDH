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

result = max(width//8, height//8)
print(result)