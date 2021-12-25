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
          [sg.Button('上传'), sg.Button('下载'), sg.Button('查看服务器文件'), sg.Button('获取嵌入密钥')]]
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
            window['file_src'].update('')
            function = "upload"
            client.send(bytes(function, "utf-8"))

            # 获取原图片名
            file_name = os.path.basename(file_src)
            # 返回图片加密后的np数组
            width, height, np_img = open_img(file_src)
            bit_img = img2bit_img(np_img)
            # 生成加密密钥并保存
            encrypt_key = encrypt_key_gen(np_img, file_name)

            encrypted_bit_img = xor_encrypt(encrypt_key, bit_img)
            encrypted_np_img = bit_img2img(encrypted_bit_img)

            # 加密后图片名
            encrypted_file_name = "encrypted_" + file_name
            # 加密原图片并保存到client目录下
            np_img_save(encrypted_np_img, encrypted_file_name)
            filesize_bytes = os.path.getsize(file_path + encrypted_file_name)

            # 创建字典用于报头，仍按照原文件名发送
            dict_header = {"file_name": file_name, "file_size": filesize_bytes}
            # 将字典转为JSON字符，再将字符串的长度打包
            header = json.dumps(dict_header)
            len_header = struct.pack('i', len(header))
            # 先发送报头长度，然后发送报头内容
            client.send(len_header)
            client.send(header.encode('utf-8'))
            # 发送真实文件
            with open(file_path + encrypted_file_name, 'rb') as f:
                data = f.read()
                client.sendall(data)
                f.close()
            # 服务器若接受完文件会发送信号，客户端接收
            finish_flag = client.recv(buffer_size).decode('utf-8')
            if finish_flag == "1":
                print("文件上传成功")

            os.remove(file_path + encrypted_file_name)

    if event == "下载":
        if values['file_src']:
            file_name = values['file_src']

            encrypt_key_name = file_name.replace('.bmp', '_encrypt_key.npy')
            embed_key_name = file_name.replace('.bmp', '_embed_key.npy')

            window['file_src'].update('')
            function = "download"
            # 发送下载指令给server同时指定下载的文件名
            client.send(bytes(function, "utf-8"))
            client.send(bytes(file_name, "utf-8"))
            # 接受并解析报头的长度，接受报头的内容
            header_struct = client.recv(4)
            header_len = struct.unpack('i', header_struct)[0]
            data = client.recv(header_len)
            # 解析报头字典
            dict_header = json.loads(data.decode("utf-8"))
            filesize_bytes = dict_header["file_size"]
            file_name = dict_header["file_name"]
            # 接受真实的文件内容
            recv_len = 0
            recv_msg = b''
            file_src = file_path + file_name

            f = open(file_src, "wb")
            while recv_len < filesize_bytes:
                if filesize_bytes - recv_len > buffer_size:
                    recv_msg = client.recv(buffer_size)
                    f.write(recv_msg)
                    recv_len += len(recv_msg)
                else:
                    recv_msg = client.recv(filesize_bytes - recv_len)
                    f.write(recv_msg)
                    f.close()
                    print("文件下载完毕")
                    break
            # 向服务器发送下载完毕信号
            finish_flag = "1"
            client.send(bytes(finish_flag, "utf-8"))

            width, height, np_img = open_img(file_name)
            block_size = 32
            block_num = min(height // block_size, width // block_size)
            msg_capacity = block_num * block_num

            # 加载加密密钥和嵌入密钥
            encrypt_key = key_load(encrypt_key_name)
            embed_key = key_load(embed_key_name)

            embed_bit_img = img2bit_img(np_img)
            decrypt_bit_img = xor_encrypt(encrypt_key, embed_bit_img)
            decrypt_np_img = bit_img2img(decrypt_bit_img)

            recover_np_img, extract_msg = recover_extract_rand(block_size, block_num, decrypt_bit_img, embed_key)
            merge_np_img = merge_recover_img(block_size, block_num, decrypt_np_img, recover_np_img)

            np_img_save(merge_np_img, file_name)
            extract_msg_name = file_name.replace('.bmp', '.npy')
            np.save(extract_msg_name, extract_msg)
            print("完成解密与嵌入信息提取")

    if event == "查看服务器文件":
        function = "view_file"
        client.send(bytes(function, "utf-8"))


    if event == "获取嵌入密钥":
        if values['file_src']:
            function = "get_embed_key"
            client.send(bytes(function, "utf-8"))
            embed_key_name = values['file_src'].replace('.bmp', '')
            client.send(bytes(embed_key_name, "utf-8"))
            header_struct = client.recv(4)
            header_len = struct.unpack('i', header_struct)[0]
            data = client.recv(header_len)
            dict_header = json.loads(data.decode("utf-8"))
            filesize_bytes = dict_header["file_size"]
            file_name = dict_header["file_name"]
            # 接受真实的文件内容
            recv_len = 0
            recv_msg = b''
            file_src = file_path + file_name

            f = open(file_src, "wb")
            while recv_len < filesize_bytes:
                if filesize_bytes - recv_len > buffer_size:
                    recv_msg = client.recv(buffer_size)
                    f.write(recv_msg)
                    recv_len += len(recv_msg)
                else:
                    recv_msg = client.recv(filesize_bytes - recv_len)
                    f.write(recv_msg)
                    f.close()
                    print("成功获取嵌入密钥")
                    break
            # 向服务器发送下载完毕信号
            finish_flag = "1"
            client.send(bytes(finish_flag, "utf-8"))

window.close()
