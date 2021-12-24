import socket
import PySimpleGUI as sg
import struct
import json
import os
import sys
import time
from img_process import *
from msg_key_gen import *
from embed_extract import *

ip_port = ('127.0.0.1', 8888)
buffer_size = 1024
file_path = "C:/Users/HoRizon/PycharmProjects/RDH/Client/"

client = socket.socket()  # 创建套接字
client.connect(ip_port)  # 连接服务器
print("连接成功")

layout = [[sg.Text('Choose the img')],
          [sg.Text('Source for Folders', size=(15, 1)), sg.InputText(key='file_src'), sg.FileBrowse()],
          [sg.Button('上传'), sg.Button('下载'), sg.Button('查看服务器文件')]]
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
            function = "upload"
            client.send(bytes(function, "utf-8"))

            # 返回图片加密后的np数组
            width, height, np_img = open_img(file_src)
            bit_img = img2bit_img(np_img)
            encrypt_key = encrypt_key_gen(np_img)
            encrypted_bit_img = xor_encrypt(encrypt_key, bit_img)
            encrypted_np_img = bit_img2img(encrypted_bit_img)

            # 获取原图片名
            file_name = os.path.basename(file_src)
            # 加密后图片名
            encrypted_file_name = "encrypted_" + file_name
            # 加密原图片并保存到client目录下
            np_img_save(encrypted_np_img, encrypted_file_name)
            filesize_bytes = os.path.getsize(file_path + encrypted_file_name)

            # 仍按照原文件名发送
            dict_header = {"file_name": file_name, "file_size": filesize_bytes}

            header = json.dumps(dict_header)
            len_header = struct.pack('i', len(header))

            client.send(len_header)
            client.send(header.encode('utf-8'))

            with open(file_path + encrypted_file_name, 'rb') as f:
                data = f.read()
                client.sendall(data)
                f.close()

            finish_flag = client.recv(buffer_size).decode('utf-8')
            if finish_flag == "1":
                print("文件上传成功")

            # os.remove(file_path + encrypted_file_name)

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

    # if event == "查看服务器文件":
    #     function = "view"
    #     client.send(bytes(function, "utf-8"))


window.close()
