import cv2
# from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle
from .KNN import K_Nearest_Neighbors_Classifier

class RecognizeFaces:

    facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def __init__(self) -> None:
        pass

    def recognize_faces(self):
        with open('data/faces.pkl', 'rb') as w:
            faces = pickle.load(w)

        with open('data/names.pkl', 'rb') as file:
            labels = pickle.load(file)

        camera = cv2.VideoCapture(0)


        knn = K_Nearest_Neighbors_Classifier(4)
        knn.fit(faces,labels)

        while True:
            ret, frame = camera.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                face_coordinates = self.facecascade.detectMultiScale(gray, 1.3, 5)

                for (a, b, w, h) in face_coordinates:
                    fc = frame[b:b + h, a:a + w, :]
                    r = cv2.resize(fc, (50, 50)).flatten().reshape(1,-1)
                    text = knn.predict(r)
                    cv2.putText(frame, text[0], (a, b-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    cv2.rectangle(frame, (a, b), (a + w, b + w), (255, 255, 0), 2)

                cv2.imshow('livetime face recognition', frame)

                if cv2.waitKey(1) == 27:
                    break
                 
            else:
                print("error")
                break

        cv2.destroyAllWindows()
        camera.release()