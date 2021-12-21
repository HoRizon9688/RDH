from PIL import Image


def mod(x, y):
    return x % y


def func(le, str1):
    b = ""  # 提取出来的信息
    im = Image.open(str1)
    lenth = le * 8
    width = im.size[0]
    height = im.size[1]
    count = 0
    for h in range(0, height):
        for w in range(0, width):
            # 获得(w,h)点像素的值
            pixel = im.getpixel((w, h))
            # 此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
            if count % 3 == 0:
                count += 1
                b = b + str((mod(int(pixel[0]), 2)))
                if count == lenth:
                    break
            if count % 3 == 1:
                count += 1
                b = b + str((mod(int(pixel[1]), 2)))
                if count == lenth:
                    break
            if count % 3 == 2:
                count += 1
                b = b + str((mod(int(pixel[2]), 2)))
                if count == lenth:
                    break
        if count == lenth:
            break
    # 隐藏的图片的二进制信息输出在msg.txt中，用010editor新建一个新的十六进制文件将此二进制信息粘贴进去然后保存为对应格式即可还原
    f = open('msg.txt', 'a')
    f.write(b)

# 信息长度（字节数）需补充 需补充 需补充 需补充
le = 10644
# 含有隐藏信息的图片 需补充 需补充 需补充 需补充
new = "LSB.png"

func(le, new)
