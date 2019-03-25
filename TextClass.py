import cv2
from aip import AipOcr

# 识别文字的类
class Text(object):

    # 将图片的文件名存到self.fname
    def __init__(self, fname):
        self.fname = fname

    # 获得读取状态的图片,为调用API做准备工作
    def get_file_content(self):
        with open(self.fname, 'rb') as fp:
            self.image = fp.read()

    # 调用API识别文字获得结果
    def text_detect(self):
        f = open('password.txt', 'r')
        # 从本地txt文件读取用于api登录的 APPID AK SK
        line = f.readline()
        APP_ID = line[:-1]
        line = f.readline()
        API_KEY = line[:-1]
        line = f.readline()
        SECRET_KEY = line
        f.close()
        # 调用API,获得文字识别结果,并在原图中框出文字,保存修改的图片到本地
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        self.get_file_content()
        results = client.general(self.image)['words_result']
        img = cv2.imread(self.fname)
        self.textcontent = ''
        for result in results:
            self.textcontent = self.textcontent + result['words']
            location = result['location']
            cv2.rectangle(img, (location["left"], location["top"]), (
                location["left"]+location["width"], location["top"]+location["height"]), (0, 255, 0), 2)

        cv2.imwrite(self.fname[:-4]+"_result.jpg", img)

# 测试
# a = Text('text2.png')
# a.text_detect()
# print(a.textcontent)
