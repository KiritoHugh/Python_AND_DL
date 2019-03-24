import cv2
from aip import AipOcr


class Text(object):
    def __init__(self, fname):
        self.fname = fname

    def get_file_content(self):
        with open(self.fname, 'rb') as fp:
            self.image = fp.read()

    def text_detect(self):
        f = open('password.txt', 'r')
        # 用于api登录的 APPID AK SK
        line = f.readline()
        APP_ID = line[:-1]
        line = f.readline()
        API_KEY = line[:-1]
        line = f.readline()
        SECRET_KEY = line
        f.close()
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

# a = Text('text2.png')
# a.text_detect()
# print(a.textcontent)
