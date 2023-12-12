import os
import cv2
import pickle
import numpy as np


class AddFace:

    def __init__(self, name) -> None:
        self.name = name
        
    # Face recognition using Knn
    def capture_face(self):
        success = True

        face_data = []
        i = 0

        camera = cv2.VideoCapture(0)

        facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        ret = True
        while(ret):
            ret, frame = camera.read()
            if ret == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                face_coordinates = facecascade.detectMultiScale(gray, 1.3, 4)

                for (a, b, w, h) in face_coordinates:
                    faces = frame[b:b+h, a:a+w, :]
                    resized_faces = cv2.resize(faces, (50, 50))
                    
                    if i % 10 == 0 and len(face_data) < 10:
                        face_data.append(resized_faces)
                    cv2.rectangle(frame, (a, b), (a+w, b+h), (255, 0, 0), 2)
                i += 1

                cv2.imshow('frames', frame)

                if cv2.waitKey(1) == 27 or len(face_data) >= 10:
                    break
            else:
                print('error')
                success = False
                break
            

        cv2.destroyAllWindows()
        camera.release()


        face_data = np.asarray(face_data)
        if face_data.size > 0:
            face_data = face_data.reshape(10, -1)  # Ensure consistent reshaping


            if not os.path.isdir("data"):
                os.mkdir("data")
            
            if 'faces.pkl' not in os.listdir('data/'):
                with open('data/faces.pkl', 'wb') as w:
                    pickle.dump(face_data, w)
            else:
                with open('data/faces.pkl', 'rb') as w:
                    faces = pickle.load(w)
                    # Check if shapes are compatible for concatenation
                    if faces.shape[1] == face_data.shape[1]:
                        faces = np.append(faces, face_data, axis=0)
                        with open('data/faces.pkl', 'wb') as w:
                            pickle.dump(faces, w)
                    else:
                        print('Shape mismatch, cannot append face data.')
                        success = False
        else:
            print('No face data captured.')
            success = False

        if 'names.pkl' not in os.listdir('data/'):
            names = [self.name]*10
            with open('data/names.pkl', 'wb') as file:
                pickle.dump(names, file)
        else:
            with open('data/names.pkl', 'rb') as file:
                names = pickle.load(file)

            names = names + [self.name]*10
            with open('data/names.pkl', 'wb') as file:
                pickle.dump(names, file)
        
        return success