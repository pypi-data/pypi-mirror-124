
import cv2 
from PIL import Image, ImageDraw






class FaceDetect:
    __slots__ = ('path','__face_cascade_db')
    def __init__(self, path: str) -> None:
        self.path = path 
        self.__face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    
    def show(self) -> None:
        """Show the image"""
        try:
            img = cv2.imread(self.path) 
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            raise ValueError("File not found!")
        
        faces = self.__face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255, 0), 2)
        cv2.imshow('result', img)
        cv2.waitKey()

    def save(self, filename='result.png'):
        """Save the image"""
        try:
            img = cv2.imread(self.path) 
            imgs = Image.open(self.path)
        except:
            raise ValueError("File not found!")
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.__face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
        draw = ImageDraw.Draw(imgs)
        for (x,y,w,h) in faces:
            

            to_width = w + x
            to_height = h + y

            draw.rectangle(
                (x, y) + (to_width, to_height),
                fill=None,
                outline='RED',
                width=2,
            )
        imgs.save(filename)