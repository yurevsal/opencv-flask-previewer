from imutils.video import VideoStream
from imutils.video.pivideostream import PiVideoStream
import imutils
import cv2
import time
import threading
import numpy as np

class MyAlgoritm(threading.Thread):
    def __init__(self, src=0, resolution=(640, 480)):
        try:
            if src == 'picamera': # Picamera
                print('picamera')
                #self.cap = VideoStream(usePiCamera=True, resolution=resolution, framerate=32)
                self.cap = PiVideoStream(resolution=resolution, framerate=32)
                self.picameraCtrls(self.cap)
            else:                   # Webcam comum
                self.cap = VideoStream(src=src,resolution=resolution)
        except:
            print('camera offline')
            exit(0)
        self.stopLoop = False
        self.mutex = threading.Lock()
        threading.Thread.__init__(self)     
    
    def read(self):
        return self.img_result
    
    def stop(self):
        self.stopLoop = True
            
    def imageShow(self, _img):
        with self.mutex:
            self.img_result = _img.copy() 

    def run(self):
        self.cap.start()
        time.sleep(2)
        while not self.stopLoop:
            frame = self.cap.read()
            results = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            self.imageShow(results)

            if cv2.waitKey(1) == 27:
                self.stop()

            time.sleep(0.01)
        self.cap.stop()
