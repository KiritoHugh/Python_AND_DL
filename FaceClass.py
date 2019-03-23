import cv2
import numpy as np
import face_recognition
import pickle
from imutils import paths

Degree_Of_Find_Small_Face = 2
class Face(object):
    def __init__(self, path_or_image):
        # to save the input image(path or imagedata) in the self.image
        if isinstance(path_or_image, np.ndarray):
            self.image = path_or_image
        elif isinstance(path_or_image, str):
            self.image = cv2.imread(path_or_image)
        if self.image is not None:
            height, width, depth = self.image.shape
            self.ratio = 200/max(height,width)
            self.image = cv2.resize(self.image,(int(width*self.ratio),int(height*self.ratio)))
    
    def face_encode(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.boxes = face_recognition.face_locations(rgb_image,Degree_Of_Find_Small_Face,model='cnn')
        max_area = 0
        if not self.boxes:
            print('boxes empty')
            self.boxes = face_recognition.face_locations(rgb_image,Degree_Of_Find_Small_Face+1,model='cnn')
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
        self.face_image = rgb_image[top:bottom,left:right]
        self.encoding = face_recognition.face_encodings(rgb_image,box)
        self.encodings = face_recognition.face_encodings(rgb_image,self.boxes)
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
