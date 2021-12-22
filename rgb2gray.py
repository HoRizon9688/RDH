from PIL import Image

img = Image.open('1.bmp').convert('L')
img = img.resize((8, 8))
img.save('test4.bmp')
