#!/usr/bin/python

import os
import numpy as np
import cv2
import datetime


class ImageProcessing:

    def init(self):
        self.img = None
        self.back_img = None
        self.flag_back_img = False
        self.update_rate = 0.01

    def set_background(self, _img):
        if self.flag_back_img == False:
            self.flag_back_img = True
            self.back_img = np.zeros_like(_img, np.float32)

    def run(self, _img):
        f_frame = _img.astype(np.float32)
        diff_frame = cv2.absdiff(f_frame, self.back_img)
        cv2.accumulateWeighted(f_frame, self.back_img, self.update_rate)
        return diff_frame.astype(np.uint8)


class CameraStreamer:

    ### init
    def init(self):
        self.sensor = 0
        self.width = 640
        self.height = 480
        self.recode_on = -1

        self.ip = ImageProcessing()
        self.ip.init()

    ### set param
    def set_sensor(self, _sensor):
        self.sensor = _sensor

    def set_recoding_mode(self, _mode):
        self.recode_on = _mode
        if self.recode_on == 0:
            self.set_video_recoder()
        if self.recode_on == 1:
            self.set_frame_recoder()

    def set_video_recoder(self):
        self.filename = "{0}.avi".format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.fps = 12
        self.out = cv2.VideoWriter(self.filename, self.fourcc, self.fps, (self.width, self.height))

    def set_frame_recoder(self, _save_path = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')):
        self.im_counter = 0
        self.ext = "jpg"
        self.save_path = _save_path
        if(os.path.exists(_save_path)):
            print("{}: Found folder".format(_save_path))
        else:
            os.mkdir(_save_path)

    ### processing
    def recording(self, _img):
        if self.recode_on == 0:
            self.out.write(_img)
        if self.recode_on == 1:
            self.save_frame(_img)

    def recording_close(self):
        if self.recode_on == 0:
            self.out.release()

    def save_frame(self, _img):
        cv2.imwrite(self.save_path + "/{0:06d}.{1}".format(self.im_counter, self.ext), _img)
        self.im_counter = self.im_counter + 1

    ### background image diff
    def do_backgroundDiff(self, _img):
        self.ip.set_background(_img)
        dst = self.ip.run(_img)
        cv2.imshow("back", self.ip.back_img.astype(np.uint8))
        return dst

    def do_imageProcessing(self, _img):
        img = cv2.cvtColor(_img, cv2.COLOR_RGB2GRAY)
        gb_img = cv2.GaussianBlur(img, ksize=(5, 5), sigmaX=3.0)
        diff_img = self.do_backgroundDiff(gb_img)
        ret, th_img = cv2.threshold(diff_img, 50, 255, cv2.THRESH_BINARY)
        dilate_img = cv2.dilate(th_img, kernel=np.ones((6, 6), np.uint8), iterations=3)
        cv2.imshow("GaussianBlur", gb_img)
        cv2.imshow("BackgroundDiff", diff_img)
        cv2.imshow("Binarization", th_img)
        cv2.imshow("Dilation", dilate_img)

    ### main
    def videoCameraView(self):
        cap = cv2.VideoCapture(self.sensor)

        while True:
            ret, img = cap.read()

            if ret == False:
                break
            if len(img.shape) == 3:
                _height, _width, _channels = img.shape[:3]
            else:
                _height, _width = img.shape[:2]
                _channels = 1

            ###
            img = cv2.resize(img, (self.width, self.height))
            self.recording(img)

            ###
            self.do_imageProcessing(img)

            ###
            cv2.imshow("Stream Video", img)
            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                break

        self.recording_close()
        cap.release()
        cv2.destroyAllWindows()

    ### sub
    def frameCameraView(self):

        import urllib
        import requests
        import io
        from PIL import Image

        while True:
            f = io.BytesIO(urllib.request.urlopen(self.sensor).read())
            img = cv2.cvtColor(np.array(Image.open(f)), cv2.COLOR_BGR2RGB)

            if len(img.shape) == 3:
                _height, _width, _channels = img.shape[:3]
            else:
                _height, _width = img.shape[:2]
                _channels = 1
            img = cv2.resize(img, (self.width, self.height))
            self.recording(img)

            cv2.imshow('Camera capture', img)
            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                break

        self.recording_close()
        cv2.destroyAllWindows()

if __name__ == '__main__':

    #URL = "http://10.232.163.38/mjpg/1/video.mjpg"
    #URL = "http://10.232.163.38/jpg/1/image.jpg"
    #URL = "20180124_143122.avi"
    URL = 0

    cam = CameraStreamer()
    cam.init()
    cam.set_sensor(URL)
    #cam.set_recoding_mode(0) # 0(movie) or 1(frame)

    cam.videoCameraView()
    #cam.frameCameraView()



