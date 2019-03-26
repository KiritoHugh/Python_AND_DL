# WECHAboT

[TOC]

### 0. 部署方式

* 保证已安装所依赖的包

  ```python
  sys
  cv2
  os
  numpy
  PyQt5
  PIL
  itchat
  time
  queue
  threading
  random
  face_recognition
  imutils
  pickle
  baidu-aip (pip install baidu-aip)
  ```

* clone 所有文件到本地

* 转到clone到本地的仓库目录内

* `python wechabot.py` 运行程序

### 1. 功能及使用说明

#### - 本地端

* Open ,打开本地图片显示于GUI
* Save ,存储GUI当前显示图片
* Detect text ,识别图片中的文字
* Regist face ,登记人脸信息及其对应的姓名到数据库
* Detect face ,根据数据库识别人脸,并在原图中标记出每张脸的位置和姓名
* Connect Wechat ,登录微信,使微信账号连接至本地服务器
* Logout Wetchat ,登出微信
* Quit ,退出程序

#### - 微信端

* regist 命令,发送照片和人名登记到数据库
* detec 命令,发送照片,识别出照片中的人脸
* text 命令,发送图片,识别其中的所有文字
* logout 命令,退出登录,中断账号与服务器连接

#### - 关于使用方式

![1553516938966](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\1553516938966.png)

* **基本本地功能:** 第一步是打开一张图片,然后可以直接按对应的按键执行登记,识别人脸等操作

* **登录微信:** 按 *connect wechat* 按键,然后扫二维码登录即可. (如果距离上次登录时间不长,可以直接在手机上确认登录,不必再扫码) .按 *logout wechat* 登出.

* **微信命令:** 当向服务器发送非命令的文字消息时,会收到打招呼+提示功能的消息,服务器需要用户提供信息时都会有自然语言提示.

  ***更加详细的使用方法示例可以观看视频.***

**注**: 人脸登记和识别是本地实现的,没有使用API,不需要联网.

### 2. 代码阐释

#### - 设计的类

##### Face 类

* 成员函数及其功能

```python
#人脸识别的类
class Face (object):
    #将输入图像(输入也可以是路径)存储到se1f. image
    def init(self, path_or_image)
    
    #找到人脸的区域并编码人脸,分别存在 boxes encodings
    def face encode(self)
    
    #登记人脸到数据库
    def regist face(self, face encoding, face name)
    
    #根据数据库识别人脸,将识别结果存到se1f.name
    def detect face (self, face encoding)
```



##### Text 类

* 成员函数及其功能

```python
#识别文字的类
class Text(object):
    #将图片的文件名存到se1f. fname
    def init (self, fname )
    
    #获得读取状态的图片,为调用API做准备工作
    def get file content(self)
    
    #调用AP识别文字获得结果
    def text detect(self)
```



##### BigThing 类

* 成员函数及其功能

```python
#继承PyQt的 QThread类设计的类
#实现多线程运行(本地pc的gui主程序和微信的自动回复服务器同时运行,互不干扰)
#下面这个类是开微信回复的线程的
class BigThing Thread (QThread):
    finished_signal= pyqtsignal(str)
    
    def init(self, rest, parent=None)
    
    #登录微信并开始后台运行自动回复
    def run(self)
    
    #登出微信
    def logout(self)
```



##### win 类

* 成员函数及其功能

```python
#继承 DIalog类,设计最主要的gui窗口类
class win(DIalog):
    
    __init__(self)
    
    #设计界面的外观以及绑定相关组件及函数
    def initUI(self)
    
    #打开本地图片
    def open Slot(self)
    
    #保存当前显示的图片到本地
    def save Slot(self)
    
    #在图中找脸,标注脸
    def findfaceSlot(self)
    
    #显示图片
    def refreshShow(self)
    
    @staticmethod
    def show message(message)
    
    #开启新线程,运行微信自动回复
    def ConnectWechat (self)
    
    #登出
    def LogoutWechat(self)
    
    #通过本地gu登记人脸
    def Local Regist(self)
    
    # 通过本地gui识别文字
    def Local DetectText(self)
```



#### - 其他的'技巧'

##### 装饰器

```python
#生成装饰器(详见 ichat文档),修饰息做反应的函数(接受文字消息并作处理和回应)
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING1])
def text_reply(msg)
	...
#生成装饰器(详见 ichat文档),修饰对图片消息做反应的函数(下载图片,并作处理和回应)
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg)
	...
```

这里设涉及到了python中的装饰器技术.`itchat.msg_regist()` 函数是一个装饰器构造函数,其参数是从微信收到的消息类型. 这里的 `@` 是一个语法糖,相当于把`itchat.msg_regist()` 修饰后的`text_reply(),download_files()` 所返回的函数再赋值给原来的函数名.

装饰器可以非常方便的给函数增加额外功能.避免了写很多的重复代码.

##### 多线程

```python
#继承PyQt的 QThread类设计的类
#实现多线程运行(本地pc的gui主程序和微信的自动回复服务器同时运行,互不干扰)
#下面这个类是开微信回复的线程的
class BigThing Thread (QThread):
    finished_signal= pyqtsignal(str)
    
    def init(self, rest, parent=None)
    
    #登录微信并开始后台运行自动回复
    def run(self)
    
    #登出微信
    def logout(self)
```

`PyQt5` 提供了`QThread` 用来实现多线程. 这里在继承`QThread` 类的基础上设计一个类. 实现了在运行等待微信消息并实现自动回复的这个循环的同时,不会影响本地的GUI及其相关的功能的实现.  *(如果只有一个线程,那么连接微信后,本地GUI就会卡住,程序一直处在自动回复的循环中)*

### 3.经历与感受

