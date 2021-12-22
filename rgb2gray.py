from PIL import Image

img = Image.open('sample_1280×853.bmp').convert('L')
img.save('test3.bmp')
