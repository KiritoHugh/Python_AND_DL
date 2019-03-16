import sys
import cv2
import os
import numpy as np
from imutils import paths
import pickle
from collections import namedtuple
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,QLabel, QPushButton)
from PIL import Image
import itchat, time
from itchat.content import *
import face_recognition
from queue import Queue
from threading import Thread
import random

def tsetfun():
    print('test')

class Face(object):
    def __init__(self, path_or_image):
        # to save the input image(path or imagedata) in the self.image
        if isinstance(path_or_image, np.ndarray):
            self.image = path_or_image
        elif isinstance(path_or_image, str):
            self.image = cv2.imread(path_or_image)
        if self.image is not None:
            height, width, depth = self.image.shape
            ratio = 200/max(height,width)
            self.image = cv2.resize(self.image,(int(width*ratio),int(height*ratio)))
    
    def face_encode(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb_image,model='cnn')
        max_area = 0
        if not boxes:
            print('boxes empty')
        for each in boxes:
            top, right, bottom, left = each
            area = (bottom-top)*(right-left)
            if area > max_area:
                max_area = area
                box = each
        top, right, bottom, left = box
        box = [box]
        self.face_image = rgb_image[top:bottom,left:right]
        self.encoding = face_recognition.face_encodings(rgb_image,box)
        self.box = box

    def regist_face(self, face_encoding, face_name):
        # check if it's been registed already
        # list = open('.\\database\\ListOfAll','wb')
        
        # regist to pickle file 
        self.data = [{'name':face_name, 'encoding':face_encoding}]
        f = open('.\\database\\'+face_name,'wb')
        f.write(pickle.dumps(self.data))
        f.close()

    def detect_face(self, face_encoding):
        record_list = list(paths.list_files('.\\database\\'))
        distance = []
        name = []
        for record in record_list:
            record = pickle.loads(open(record,'rb').read())
            record = np.array(record)
            name.append(record[0]['name'])
            encoding = record[0]['encoding']
            distance.append(face_recognition.face_distance(encoding,face_encoding[0]))
        min_dis = min(distance)
        min_pos = distance.index(min_dis)
        # print('min_dis %f '%min_dis)
        # print('min_pos %f'%min_pos)
        if min_dis < 0.5:
            self.name = name[min_pos]
        else:
            self.name = 'unknow'        
        # print('self.name %s'%self.name)

class BigThingThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, rest, parent=None):
        super().__init__(parent)
        self._rest = rest

    def run(self):
        print('do something big')
        itchat.auto_login(True)
        global helpinfo
        itchat.run()
        self.finished_signal.emit('done')

class win(QDialog):
    def __init__(self):

        # 初始化一个img的ndarray, 用于存储图像
        self.img = np.ndarray(())

        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 300)
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)
        self.label = QLabel()
        # my
        self.btnConnect = QPushButton('Connect Wechat',self)

        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnProcess, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)
        # my
        layout.addWidget(self.btnConnect,5,1,1,1)

        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)
        # my
        self.btnConnect.clicked.connect(self.ConnectWechat)

    def openSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        # 采用opencv函数读取数据
        self.img = cv.imread(fileName, -1)

        if self.img.size == 1:
            return

        self.refreshShow()

    def saveSlot(self):
        # 调用存储文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './__data', '*.png *.jpg *.bmp', '*.png')

        if fileName is '':
            return
        if self.img.size == 1:
            return

        # 调用opencv写入图像
        cv.imwrite(fileName, self.img)

    def processSlot(self):
        if self.img.size == 1:
            return

        # 对图像做模糊处理, 窗口设定为5x5
        self.img = cv.blur(self.img, (5, 5))

        self.refreshShow()

    def refreshShow(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(self.qImg))

    @staticmethod
    def _show_message(message):
        print('{}'.format(message))

    def ConnectWechat(self):
        # win32api.ShellExecute(0,'open','nude.py','','',1)
        # global wechat_handle
        # wechat_handle = win32process.CreateProcess('D:\Anaconda3\python.exe','D:\my_workspace\little_program\pyqt-hw\nude.py',None,None,0,win32process.CREATE_NO_WINDOW,None,None,win32process.STARTUPINFO())
        # itchat.auto_login(True)
        # itchat.run()
        self.big_thread = BigThingThread(1)
        self.big_thread.finished_signal.connect(self._show_message)
        self.big_thread.start()

    def test(self):
        tsetfun()

if __name__ == '__main__':

    helpinfo = 'regist detect text'

    init_reply_list = [
        'Please give a LEGAL command */%s/*, sir.'%helpinfo,
        'Master! Beg for a LEGAL command */%s/*.'%helpinfo,
        'I am bored! Please order me */%s/*.'%helpinfo
    ]
    command = 'empty'
    reciever = 'filehelper'
    waitname_flag = False
    name = None
    # global One_instance
    One_instance = Face(command)
    

    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
    def text_reply(msg):
        text = msg['Text']
        global waitname_flag
        if waitname_flag:
            name = text
            global One_instance
            One_instance.regist_face(One_instance.encoding,name)
            itchat.send('regist success',reciever)
            waitname_flag = False

        else:
            if text in ['regist','detect','text']:
                global command
                command = text
                itchat.send('Give me a photo',reciever)
            elif text in ['bye']:
                pass
                # global w
                # w.close()
            else:
                itchat.send(random.choice(init_reply_list),reciever)



    @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def download_files(msg):
        msg.download(msg.fileName)
        typeSymbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg.type, 'fil')
        
        fname=cv2.imread(msg.fileName)
        global One_instance
        One_instance = Face(fname)

        if command == 'regist':
            One_instance.face_encode()
            itchat.send('Please input name.',reciever)
            global waitname_flag
            waitname_flag = True
        elif command == 'detect':
            One_instance.face_encode()
            print('after encode')
            One_instance.detect_face(One_instance.encoding)
            print('after detect')
            itchat.send(One_instance.name,reciever)
            print('after send')



        # n.resize(maxheight=800, maxwidth=600)
        # n.parse()#分析函数
        # n.showSkinRegions()
        
        # #print(n.result, n.inspect())
        # #itchat.send_image(msg.fileName,'filehelper') # 发送图片
        # # itchat.send('经专业鉴定，此图%s' % ('涉黄，请跟我们走一趟' if n.result== True else '清清白白，组织相信你了'), msg['FromUserName'])
        # itchat.send('经专业鉴定，此图%s' % ('涉黄，请跟我们走一趟' if n.result== True else '清清白白，组织相信你了'), 'filehelper')

    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())
    # win32process.TerminateProcess(wechat_handle[0],0)


# improvement waitlist:
#     - in the Face.face_encode, if no face in photo
