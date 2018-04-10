import cv2, numpy, os
size = 2
fn_haar = '/Users/mehdi/Work/smart-camera/haarcascade_frontalface_default.xml'
fn_dir = '/Users/mehdi/Work/smart-camera/att_faces'

class FaceRecognizer(object):
    def __init__(self):
        (self.images, self.lables, self.names, self.id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(fn_dir):
            for subdir in dirs:
                self.names[self.id] = subdir
                subjectpath = os.path.join(fn_dir, subdir)
                for filename in os.listdir(subjectpath):
                    f_name, f_extension = os.path.splitext(filename)
                    path = subjectpath + '/' + filename
                    self.lable = self.id
                    self.images.append(cv2.imread(path, 0))
                    self.lables.append(int(self.lable))
                self.id += 1
        (self.im_width, self.im_height) = (112, 92)
        (self.images, self.lables) = [numpy.array(lis) for lis in [self.images, self.lables]]
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.train(self.images, self.lables)
        self.haar_cascade = cv2.CascadeClassifier(fn_haar)

    def predict(self, frame, db):
        person = None
        db.open()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        faces = self.haar_cascade.detectMultiScale(mini)
        for i in range(len(faces)):
            face_i = faces[i]
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (self.im_width, self.im_height))
            prediction = self.model.predict(face_resize)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            id = self.names[prediction[0]]
            print(id)
            person = db.query_person(id)
            cv2.putText(frame,
                        '%s' % (person[1] + ' ' + person [2]),
                        (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        db.close()
        return frame, person

    def save_face(self, name, webcam):
        path = os.path.join(fn_dir, name)
        if not os.path.isdir(path):
            os.mkdir(path)
        im_width, im_height = (112, 92)
        pin = sorted([int(n[:n.find('.')]) for n in os.listdir(path)
                      if n[0] != '.'] + [0])[-1] + 1
        count = 0
        pause = 0
        count_max = 20
        while count < count_max:
            frame = webcam.get_frame()
            height, width, channels = frame.shape
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
            faces = self.haar_cascade.detectMultiScale(mini)
            faces = sorted(faces, key=lambda x: x[3])
            if faces:
                face_i = faces[0]
                (x, y, w, h) = [v * size for v in face_i]

                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (im_width, im_height))

                # Draw rectangle and write name
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
                    1,(0, 255, 0))
                # Remove false positives
                if(w * 6 < width or h * 6 < height):
                    print("Face too small")
                else:
                    # To create diversity, only save every fith detected image
                    if(pause == 0):
                        print("Saving training sample "+str(count+1)+"/"+str(count_max))
                        # Save image file
                        cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
                        pin += 1
                        count += 1
                        pause = 1
            if (pause > 0):
                pause = (pause + 1) % 5
        self.retrain()
        return True

    def retrain(self):
        (self.images, self.lables, self.names, self.id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(fn_dir):
            for subdir in dirs:
                self.names[self.id] = subdir
                subjectpath = os.path.join(fn_dir, subdir)
                for filename in os.listdir(subjectpath):
                    f_name, f_extension = os.path.splitext(filename)
                    path = subjectpath + '/' + filename
                    self.lable = self.id
                    self.images.append(cv2.imread(path, 0))
                    self.lables.append(int(self.lable))
                self.id += 1
        (self.im_width, self.im_height) = (112, 92)
        (self.images, self.lables) = [numpy.array(lis) for lis in [self.images, self.lables]]
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.model.train(self.images, self.lables)
        return True



