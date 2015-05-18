# -*- coding: utf8 -*-

from PyQt4 import QtGui
from Base64 import encode_image
from SocketModule import UDPService, TCPClient
from Modify import render_faces, modify_model
from core import G


class SocketWindow(QtGui.QWidget):
    def __init__(self):
        super(SocketWindow, self).__init__()

        self.setWindowTitle("TCP Window")

        # remote server and client
        self.receive_server = None
        self.tcp_client = None

        G.app.setFaceCamera()

        self.init_ui()
        self.init_remote_module()

    def init_ui(self):
        v_box = QtGui.QVBoxLayout(self)

        image = QtGui.QLabel(self)
        v_box.addWidget(image)

        switch = QtGui.QPushButton(self)
        switch.setText("Turn off TCP Server")
        switch.clicked.connect(self.switch_click)
        v_box.addWidget(switch)

        self.setLayout(v_box)

    def init_remote_module(self):
        # UDP Server
        self.receive_server = UDPService(self)
        self.receive_server.trigger.connect(self.received)
        self.receive_server.start()
        # TCP Client
        self.tcp_client = TCPClient()

    def switch_click(self):
        text = self.switch.text()
        if "Off" in text:
            self.switch.setText("Turn On TCP Server")
        else:
            self.switch.setText("Turn Off TCP Server")

    def received(self, received_qt_message):
        received_message = str(received_qt_message)

        # method_name and continue

        command = eval(received_message)
        human = G.app.selectedHuman

        method = getattr(self, command["Method"])
        method(human, command)

    def modify_and_get_images(self, human, command):
        count = 0
        image_size = []
        image_data =[]

        for face in render_faces(human, command["Individuals"]):
            base64_string = encode_image(face)

            count += 1
            image_size.append(len(base64_string))
            image_data.append(base64_string)

        command["ReturnData"] = image_data

        self.tcp_client.send_json(str(command))

    def modify_and_get_points(self, human, command):
        points_data = {}

        individual = command["Individuals"][0]
        indices = command["Parameters"]

        modify_model(human, individual)

        for index in indices:
            point = human.mesh.__dict__["coord"][index]
            points_data[str(index)] = str(point.tolist())

        command["ReturnData"] = points_data

        self.tcp_client.send_json(str(command))

    def modify_and_get_models(self, human, command):
        models_data = []

        for individual in command["Individuals"]:
            modify_model(human, individual)

            models_data.append(human.mesh.__dict__["coord"].tolist())

        command["ReturnData"] = models_data

        self.tcp_client.send_json(str(command))

    def modify(self, human, command):
        pass