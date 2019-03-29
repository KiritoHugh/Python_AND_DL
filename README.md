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

* **基本本地功能:** 第一步是打开一张图片,然后可以直接按对应的按键执行登记,识别人脸,识别文字等操作

* **登录微信:** 按 *connect wechat* 按键,然后扫二维码登录即可. (如果距离上次登录时间不长,可以直接在手机上确认登录,不必再扫码) .按 *logout wechat* 登出.

* **微信命令:** 当向服务器发送非命令的文字消息时,会收到打招呼+提示功能的消息,服务器需要用户提供信息时都会有自然语言提示.

  ***更加详细的使用方法示例可以观看视频.***

  [---> 视频链接 <---](https://www.bilibili.com/video/av47487768)

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

### 3.收获与感受与心路与坑

#### i.关于"连接微信后本地GUI就崩了!"

一开始,我将实现连接微信自动回复的函数与相应按钮的slot连接后,开始测试.然后在按下按钮之后,虽然成功进入连接微信的流程,不过在执行微信自动回复的任务时,本地的GUI就会一直"程序没有响应".我意识到是我的程序一条线串行执行导致的.于是我就开始寻找解决方法.

我先使用的是win32里面的api,将按按键之后的微信登录回复程序放到一个新的进程中跑.不过在测试之后,我又发现新的进程在GUI关闭之后并不会随之关闭,而是继续留在后台运行,于是我决定用多线程.

于是google,最后使用PyQt5的QThread类满意地解决了这个问题.

#### ii.关于"图片太大了,屏幕都放不下了!"与"图片太大了,CNN提feature unacceptable 地慢了!"

在测试时,我在本地打开某一张人脸的照片并按下按键开始识别人脸时,过了相当长的时间还没有给出结果,于是我意识到是照片的质量太高了,人脸区域的像素点太多,给CNN提取feature带来了没有必要的多余的计算量,导致特别慢.所以我在检测图片之前都将其imsize为合适的大小,不对识别结果造成任何影响,同时提升了很多速度.

#### iii.关于"图片里有多个人,登记的是谁啊?"与"图片里有多个人,怎么只标注了一个脸啊!"

登记人脸时,我碰巧选择了一张含有多个人脸的图片,还没有按下登记按钮,我就把程序关了开始改了,同时我也考虑了检测人脸时有多个脸的问题.最终结果是,登记人脸时,选择图片中所占区域最大的人脸,检测人脸时,标出所有检测到的人脸.