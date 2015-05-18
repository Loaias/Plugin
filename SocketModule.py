# -*- coding: utf8 -*-

from PyQt4 import QtCore
import struct
import socket


class UDPService(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(UDPService, self).__init__()

        self.parent = parent
        self.address = ('127.0.0.1', 6000)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)

    def run(self):
        while True:
            received_message, address = self.socket.recvfrom(1024)
            self.trigger.emit(received_message)


class TCPClient():
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