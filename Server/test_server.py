import PySimpleGUI as sg
import socket
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
file_path = "C:/Users/HoRizon/PycharmProjects/RDH/Server/"

server = socket.socket()  # 创建 socket 对象
server.bind(ip_port)                # 绑定服务地址
server.listen(5)                    # 监听连接请求
print('启动socket服务，等待客户端连接...')

# quit_flag = 0

# layout = [[sg.Button('查看服务器文件')]]
#
# window = sg.Window('Server', layout)
#
# while True:
#     event, values = window.read()
#     if event == sg.WINDOW_CLOSED:
#         print("退出系统")
#         server.close()
#         break

while True:
    client_sock, address = server.accept()
    print("connected with ", end="")
    print(address[0] + ":" + str(address[1]))

    while True:
        fun_select = client_sock.recv(buffer_size).decode("utf-8")

        if fun_select == 'upload':
            print("Start " + fun_select)
            header_struct = client_sock.recv(4)
            header_len = struct.unpack('i', header_struct)[0]

            data = client_sock.recv(header_len)
            dict_header = json.loads(data.decode("utf-8"))
            filesize_bytes = dict_header["file_size"]
            file_name = dict_header["file_name"]

            recv_len = 0
            recv_msg = b''

            file_src = file_path + file_name
            f = open(file_src, "wb")

            while recv_len < filesize_bytes:
                if filesize_bytes - recv_len > buffer_size:
                    recv_msg = client_sock.recv(buffer_size)
                    f.write(recv_msg)
                    recv_len += len(recv_msg)
                else:
                    recv_msg = client_sock.recv(filesize_bytes - recv_len)
                    f.write(recv_msg)
                    f.close()
                    print("文件接受完毕")
                    break

            finish_flag = "1"
            client_sock.send(bytes(finish_flag, "utf-8"))

        elif fun_select == "download":
            print("Start " + fun_select)
            file_name = client_sock.recv(buffer_size).decode("utf-8")
            file_src = file_path + file_name

            filesize_bytes = os.path.getsize(file_src)
            file_name = "new_" + file_name
            dict_header = {"file_name": file_name, "file_size": filesize_bytes}

            header = json.dumps(dict_header)
            len_header = struct.pack('i', len(header))

            client_sock.send(len_header)
            client_sock.send(header.encode("utf-8"))

            with open(file_src, "rb") as f:
                data = f.read()
                client_sock.sendall(data)
                f.close()

            finish_flag = client_sock.recv(buffer_size).decode("utf-8")
            if finish_flag == "1":
                print("用户下载完毕")
        else:
            print(address[0] + ":" + str(address[1]) + " 用户退出")
            client_sock.close()
            break
