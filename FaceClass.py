import cv2
import numpy as np
import face_recognition
import pickle
from imutils import paths

# 决定在图中找脸的精细度(数值越大,能找到的最小脸最小)
Degree_Of_Find_Small_Face = 2

# 人脸识别的类
class Face(object):
    # 将输入图像(输入也可以是路径)存储到self.image
    def __init__(self, path_or_image):
        if isinstance(path_or_image, np.ndarray):
            self.image = path_or_image
        elif isinstance(path_or_image, str):
            self.image = cv2.imread(path_or_image)
        if self.image is not None:
            height, width, depth = self.image.shape
            self.ratio = 200/max(height, width)
            self.image = cv2.resize(
                self.image, (int(width*self.ratio), int(height*self.ratio)))

    # 找到人脸的区域并编码人脸,分别存在boxes encodings
    def face_encode(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.boxes = face_recognition.face_locations(
            rgb_image, Degree_Of_Find_Small_Face, model='cnn')
        # 找到所有脸中最大的一个,区域和编码分别存在box encoding,在人脸登记时,登记的是最大脸
        max_area = 0
        if not self.boxes:
            print('boxes empty')
            self.boxes = face_recognition.face_locations(
                rgb_image, Degree_Of_Find_Small_Face+1, model='cnn')
            if not self.boxes:
                print('boxes empty')
        for each in self.boxes:
            top, right, bottom, left = each
            area = (bottom-top)*(right-left)
            if area > max_area:
                max_area = area
                box = each
        top, right, bottom, left = box
        box = [box]
        self.face_image = rgb_image[top:bottom, left:right]
        self.encoding = face_recognition.face_encodings(rgb_image, box)
        self.encodings = face_recognition.face_encodings(rgb_image, self.boxes)
        self.box = box

    # 登记人脸到数据库
    def regist_face(self, face_encoding, face_name):
        record_list = list(paths.list_files('.\\database\\'))
        # 登记数据到pickle文件
        self.data = [{'name': face_name, 'encoding': face_encoding}]
        f = open('.\\database\\'+face_name, 'wb')
        f.write(pickle.dumps(self.data))
        f.close()
        # 检查是否与database内已经存在的重名
        name_list = [x[11:] for x in record_list]
        print(str(name_list))
        print(face_name)
        if face_name in name_list:
            return 'name has existed, overwrite success'
        else:
            return 'regist success'

    # 根据数据库识别人脸,将识别结果存到self.name
    def detect_face(self, face_encoding):
        record_list = list(paths.list_files('.\\database\\'))
        distance = []
        name = []
        for record in record_list:
            record = pickle.loads(open(record, 'rb').read())
            record = np.array(record)
            name.append(record[0]['name'])
            encoding = record[0]['encoding']
            distance.append(face_recognition.face_distance(
                encoding, face_encoding[0]))
        min_dis = min(distance)
        min_pos = distance.index(min_dis)
        # print('min_dis %f '%min_dis)
        # print('min_pos %f'%min_pos)
        if min_dis < 0.52:
            self.name = name[min_pos]
        else:
            self.name = 'unknow'
        # print('self.name %s'%self.name)
