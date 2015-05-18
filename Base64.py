from PyQt4 import QtCore
import zlib


def encode_image(image):
    byte_array = QtCore.QByteArray()
    byte_buffer = QtCore.QBuffer(byte_array)
    image.toQImage().save(byte_buffer, 'JPEG')
    base64_string = byte_array.toBase64().data()
    return base64_string