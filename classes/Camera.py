import cv2


class Camera(object):
    def __init__(self, pipeline):
        self.camera = cv2.VideoCapture(pipeline)

    def get_frame(self):
        frame = self.camera.read()[1]
        return cv2.flip(frame, 1)



