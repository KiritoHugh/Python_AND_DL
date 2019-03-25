# WECHAboT

[TOC]



### 1. 功能及使用说明

#### - 本地端

* 打开本地图片显示于GUI
* 存储GUI当前显示图片
* 识别图片中的文字
* 登记人脸信息及其对应的姓名到数据库
* 根据数据库识别人脸,并在原图中标记出每张脸的位置和姓名
* 登录微信,使微信账号连接至本地服务器
* 登出微信

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

```python
#继承PyQt的 QThread类设计的类
#实现多线程运行(本地pc的gui主程序和微信的自动回复服务器同时运行,互不干扰)
#下面这个类是开微信回复的线程的
class BigThing Thread (QThread):
    finished signal= pyqtsignal(str)
    
    def init(self, rest, parent=None)
    
    #登录微信并开始后台运行自动回复
    def run(self)
    
    #登出微信
    def logout(self)
```



##### win 类

```python

```



#### - 其他的'技巧'

##### 装饰器



##### 多线程