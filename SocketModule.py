# # -*- coding: utf8 -*-
#
# from PyQt4 import QtCore
# import struct
# import socket
#
#
# class Service(QtCore.QThread):
#     trigger = QtCore.pyqtSignal(str)
#
#     def __init__(self, parent):
#         super(Service, self).__init__()
#
#         self.parent = parent
#         self.address = ('127.0.0.1', 6000)
#
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.bind(self.address)
#
#     def run(self):
#         while True:
#             received_message, address = self.socket.recvfrom(1024)
#             self.trigger.emit(received_message)
#
#
# class Client:
#     def __init__(self):
#         self.address = ('127.0.0.1', 6001)
#         self.buff_size = 1024
#
#     def send_json(self, json):
#         send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         send_sock.connect(self.address)
#
#         command_length = len(json)
#         package_size = (command_length + self.buff_size - 1) / self.buff_size
#         data_head = struct.pack("i", command_length)
#
#         print "开始传送数据:"
#         send_sock.send(data_head)
#         for i in xrange(package_size):
#             index = self.buff_size * i
#             send_sock.send(json[index:index + self.buff_size])
#         print "文件传送完毕，正在断开连接..."
#         send_sock.close()
#         print "连接已关闭..."


# -*- coding: utf8 -*-

from PyQt4 import QtCore
import struct
import socket


class Server(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Server, self).__init__()

        self.parent = parent
        self.address = ('127.0.0.1', 6000)

        self.buff_size = 1024

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)

    def received_data(self, conn):
        command_length = struct.unpack('i', conn.recv(struct.calcsize('i')))[0]
        rest_length = command_length
        json = []

        print "正在接收json文件..."

        while True:
            if rest_length > self.buff_size:
                json.append(conn.recv(self.buff_size))
                rest_length -= self.buff_size
            else:
                json.append(conn.recv(rest_length))
                break

        print "json文件接收完毕"
        self.trigger.emit("".join(json))
        print "文件接收完毕,正在关闭连接"
        conn.close()
        # self.receive_Sock.close()
        print "连接已关闭..."

        self.start_listen()

    def start_listen(self):
        self.socket.listen(True)
        print "等待连接..."

        conn, address = self.socket.accept()
        print "客户端已连接—> ", address

        self.received_data(conn)

    def run(self):
        self.start_listen()


class Client:
    def __init__(self):
        self.address = ('127.0.0.1', 6001)
        self.buff_size = 1024

    def send_json(self, json):
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_sock.connect(self.address)

        command_length = len(json)
        package_size = (command_length + self.buff_size - 1) / self.buff_size
        data_head = struct.pack("i", command_length)

        print "开始传送数据:"
        send_sock.send(data_head)
        for i in xrange(package_size):
            index = self.buff_size * i
            send_sock.send(json[index:index + self.buff_size])
        print "文件传送完毕，正在断开连接..."
        send_sock.close()
        print "连接已关闭..."