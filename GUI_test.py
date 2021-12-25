import PySimpleGUI as sg
import matplotlib.pyplot as plt

layout = [[sg.Text('Choose the img')],
          [sg.Text('Source for Folders', size=(15, 1)), sg.InputText(key='file_src'), sg.FileBrowse()],
          [sg.Button('上传'), sg.Button('下载'), sg.Button('查看服务器文件'), sg.Button('获取嵌入密钥')],
          [sg.Output(key="-Output-", size=(80, 20))]]
window = sg.Window('Client', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        print("退出系统")
        break
