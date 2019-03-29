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

<img src="data:image/png;base64,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"/>

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