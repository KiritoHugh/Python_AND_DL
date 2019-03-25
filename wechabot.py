import sys
import cv2
import os
import numpy as np
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
                             QGridLayout, QLabel, QPushButton, QLineEdit, QPlainTextEdit)
from PIL import Image, ImageDraw
import itchat
import time
from itchat.content import *
from queue import Queue
from threading import Thread
import random
from FaceClass import Face
from TextClass import Text
# from PyQtClass import *

# from PyQt5 import KeepAspectRatio,FastTransformation
import face_recognition
# from imutils import paths
# import pickle
# from collections import namedtuple
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPixmap

# Degree_Of_Find_Small_Face = 2


# 继承PyQt的QThread类设计的类
# 实现多线程运行(本地pc的gui主程序和微信的自动回复服务器同时运行,互不干扰)
# 下面这个类是开微信回复的线程的
class BigThingThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, rest, parent=None):
        super().__init__(parent)
        self._rest = rest

    # 登录微信并开始后台运行自动回复
    def run(self):
        print('do something big')
        itchat.auto_login(True)
        global helpinfo
        itchat.run()
        self.finished_signal.emit('done')

    # 登出微信
    def logout(self):
        itchat.logout()

# 继承QDialog类,设计最主要的gui窗口类
class win(QDialog):
    def __init__(self):

        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())
        super().__init__()
        self.initUI()
        self.setWindowTitle('WECHAboT')
        self.setWindowIcon(QIcon(QPixmap("robot.png")))

    # 设计界面的外观以及绑定相关组件及函数
    def initUI(self):
        self.resize(400, 300)
        self.lineName = QLineEdit('Name', self)
        self.lineOutput = QPlainTextEdit(self)
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)

        self.btnFindface = QPushButton('Detect face', self)
        self.btnRegist = QPushButton('Regist face', self)        
        self.btnDetectText = QPushButton('Detect text',self)

        self.btnConnect = QPushButton('Connect Wechat', self)
        self.btnLogout = QPushButton('Logout Wechat', self)
 
        self.subtitile_Output = QLabel('Output:')
        self.subtitile_Input = QLabel('Input:')

        self.btnQuit = QPushButton('Quit', self)
        self.label = QLabel()

        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 2, 4)
        layout.addWidget(self.subtitile_Input, 2, 1, 1, 1)
        layout.addWidget(self.lineName, 3, 1, 1, 1)

        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)

        layout.addWidget(self.btnFindface, 5, 1, 1, 1)
        layout.addWidget(self.btnRegist, 5, 2, 1, 1)
        layout.addWidget(self.btnDetectText, 5, 3, 1, 1)

        layout.addWidget(self.btnConnect, 6, 1, 1, 1)
        layout.addWidget(self.btnLogout, 6, 2, 1, 1)

        layout.addWidget(self.btnQuit, 7, 1, 1, 2)

        layout.addWidget(self.subtitile_Output, 8, 1, 1, 1)
        layout.addWidget(self.lineOutput, 9, 1, 2, 4)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)

        self.btnFindface.clicked.connect(self.findfaceSlot)
        self.btnRegist.clicked.connect(self.Local_Regist)
        self.btnDetectText.clicked.connect(self.Local_DetectText)

        self.btnConnect.clicked.connect(self.ConnectWechat)
        self.btnLogout.clicked.connect(self.LogoutWechat)

        self.btnQuit.clicked.connect(self.close)

    # 打开本地图片
    def openSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        # 采用opencv函数读取数据
        self.fname = fileName
        self.img = cv2.imread(fileName)
        height, width, depth = self.img.shape
        self.ratio = 500/max(height, width)
        self.img = cv2.resize(
            self.img, (int(width*self.ratio), int(height*self.ratio)))

        if self.img.size == 1:
            return

        self.refreshShow()

    #保存当前显示的图片到本地
    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './__data', '*.png *.jpg *.bmp', '*.png')

        if fileName is '':
            return
        if self.img.size == 1:
            return

        # 调用opencv写入图像
        cv2.imwrite(fileName, self.img)

    # 在图中找脸,标注脸
    def findfaceSlot(self):
        names = []
        One_object = Face(self.img)

        # cv2 类型的img转换为PIL中的img,以便在其上画出相应标注
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        draw_image = ImageDraw.Draw(self.img)
        # 识别图中的脸,并在图中标注出来
        One_object.face_encode()
        for (top, right, bottom, left), face_encoding in zip(One_object.boxes, One_object.encodings):
            One_object.detect_face([face_encoding])
            name = One_object.name
            names.append(name)
            (top, right, bottom, left) = tuple(
                [int(x/One_object.ratio) for x in (top, right, bottom, left)])
            draw_image.rectangle(
                ((left, top), (right, bottom)), outline=(0, 0, 255))
            text_width, text_height = draw_image.textsize(One_object.name)
            draw_image.rectangle(((left, bottom - text_height - 10),
                                  (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw_image.text((left + 6, bottom - text_height - 5),
                            name, fill=(255, 255, 255, 255))
        self.img = np.array(self.img)
        # Convert RGB to BGR
        self.img = self.img[:, :, ::-1].copy()
        # 输出人名
        nameOutput = ''
        for mem in names:
            nameOutput = nameOutput+'    '+str(mem)
        self.lineOutput.setPlainText(nameOutput)
        self.refreshShow()

    # 显示图片
    def refreshShow(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        pixmap = QPixmap.fromImage(self.qImg)
        self.label.setPixmap(pixmap)

    @staticmethod
    def _show_message(message):
        print('{}'.format(message))
        print('i dont understand')

    # 开启新线程,运行微信自动回复
    def ConnectWechat(self):
        self.big_thread = BigThingThread(1)
        self.big_thread.finished_signal.connect(self._show_message)
        self.big_thread.start()

    # 登出
    def LogoutWechat(self):
        self.big_thread.logout()

    # 通过本地gui登记人脸
    def Local_Regist(self):
        One_object = Face(self.img)
        One_object.face_encode()
        hint = One_object.regist_face(
            One_object.encoding, self.lineName.text())
        self.lineOutput.setPlainText(hint)

    # 通过本地gui识别文字
    def Local_DetectText(self):
        Text_object = Text(self.fname)
        Text_object.text_detect()
        self.lineOutput.setPlainText(Text_object.textcontent)


if __name__ == '__main__':

    helpinfo = '\n */I AM WECHAboT/* \n Nice to meet you, I have 4 commands: regist detect text logout'

    init_reply_list = [
        'Please give a LEGAL command, sir.%s' % helpinfo,
        'Master! Beg for a LEGAL command.%s' % helpinfo,
        'I am bored! Please order me.%s' % helpinfo
    ]

    command = 'empty'
    reciever = 'filehelper'
    waitname_flag = False
    name = None
    One_instance = Face(command)

    # 生成装饰器(详见itchat文档),修饰对文字消息做反应的函数(接受文字消息并作处理和回应)
    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
    def text_reply(msg):
        text = msg['Text']
        # 如果是已接收登记人脸的command,则要等待人名输入
        global waitname_flag
        if waitname_flag:
            name = text
            global One_instance
            One_instance.regist_face(One_instance.encoding, name)
            itchat.send('regist success', reciever)
            waitname_flag = False

        # 接受command
        else:
            if text in ['regist', 'detect', 'text']:
                global command
                command = text
                itchat.send('Give me a photo', reciever)
            elif text in ['logout']:
                # itchat.send_image('lena.png',reciever)
                itchat.send('bye~',reciever)
                itchat.logout()
                # global w
                # w.close()
            else:
                itchat.send(random.choice(init_reply_list), reciever)

    # 生成装饰器(详见itchat文档),修饰对图片消息做反应的函数(下载图片,并作处理和回应)
    @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def download_files(msg):
        # 下载图片
        msg.download(msg.fileName)
        typeSymbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg.type, 'fil')

        # 读图,进行人脸识别或文字识别
        fname = cv2.imread(msg.fileName)
        global One_instance
        One_instance = Face(fname)
        Text_inatance = Text(msg.fileName)

        if command == 'regist':
            One_instance.face_encode()
            itchat.send('Please input name.', reciever)
            global waitname_flag
            waitname_flag = True
        elif command == 'detect':
            One_instance.face_encode()
            One_instance.detect_face(One_instance.encoding)
            # print(str(One_instance.encoding))
            itchat.send(One_instance.name, reciever)
        elif command == 'text':
            Text_inatance.text_detect()
            itchat.send(Text_inatance.textcontent, reciever)

    # 运行gui程序
    # a = QApplication(sys.argv)
    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())

