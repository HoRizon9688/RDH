import PySimpleGUI as sg
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

layout = [[sg.Text('Choose the img')],
          [sg.Text('Source for Folders', size=(15, 1)), sg.InputText(key='img_src'), sg.FileBrowse()],
          [sg.Submit(), sg.Cancel()]]
window = sg.Window('Rename Files or Folders', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    if values['img_src']:
        img = Image.open(values['img_src'])
        width = img.size[0]
        height = img.size[1]
        print("width:" + str(width))
        print("height:" + str(height) + "\n")
        np_img = np.array(img)
        plt.imshow(np_img)
        plt.axis('off')
        plt.show()
