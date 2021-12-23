import socket
import PySimpleGUI as sg
import struct
import json
import os
import sys
import time

ip_port = ('127.0.0.1', 8888)
buffer_size = 1024
file_path = "C:/Users/HoRizon/PycharmProjects/RDH/Client/"

client = socket.socket()  # 创建套接字
client.connect(ip_port)  # 连接服务器

layout = [[sg.Text('Choose the img')],
          [sg.Text('Source for Folders', size=(15, 1)), sg.InputText(key='file_src'), sg.FileBrowse()],
          [sg.Button('上传'), sg.Button('下载')]]
window = sg.Window('Client', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        print("退出系统")
        client.close()
        break
    if event == '上传':
        if values['file_src']:
            file_src = values['file_src']
            # window.perform_long_operation(upload(client, file_src), 'upload_done')
            function = "upload"
            client.send(bytes(function, "utf-8"))

            filesize_bytes = os.path.getsize(file_src)
            file_name = os.path.basename(file_src)

            dict_header = {"file_name": file_name, "file_size": filesize_bytes}

            header = json.dumps(dict_header)
            len_header = struct.pack('i', len(header))

            client.send(len_header)
            client.send(header.encode('utf-8'))

            with open(file_src, 'rb') as f:
                data = f.read()
                client.sendall(data)
                f.close()

            finish_flag = client.recv(buffer_size).decode('utf-8')
            if finish_flag == "1":
                print("文件上传成功")

    if event == "下载":
        if values['file_src']:
            file_name = values['file_src']
            function = "download"
            client.send(bytes(function, "utf-8"))

            client.send(bytes(file_name, "utf-8"))

            header_struct = client.recv(4)
            header_len = struct.unpack('i', header_struct)[0]
            data = client.recv(header_len)

            dict_header = json.loads(data.decode("utf-8"))
            filesize_bytes = dict_header["file_size"]
            file_name = dict_header["file_name"]

            recv_len = 0
            recv_mesg = b''

            file_src = file_path + file_name
            f = open(file_src, "wb")

            while recv_len < filesize_bytes:
                if filesize_bytes - recv_len > buffer_size:
                    recv_mesg = client.recv(buffer_size)
                    f.write(recv_mesg)
                    recv_len += len(recv_mesg)
                else:
                    recv_mesg = client.recv(filesize_bytes - recv_len)
                    f.write(recv_mesg)
                    f.close()
                    print("文件下载完毕")
                    break
            finish_flag = "1"
            client.send(bytes(finish_flag, "utf-8"))

window.close()
