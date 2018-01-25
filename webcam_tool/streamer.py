import os
import numpy as np
import cv2
import datetime
from collections import deque

class ImageProcessing:

    def init(self):
        # background_diff
        self.back_img = None
        self.flag_back_img = False
        self.update_rate = 0.01

        # salt_pepper_noise
        self.s_vs_p = 0.5
        self.amount = 0.01

    def background_diff(self, _img):
        if self.flag_back_img == False:
            self.flag_back_img = True
            self.back_img = np.zeros_like(_img, np.float32)
        f_frame = _img.astype(np.float32)
        diff_frame = cv2.absdiff(f_frame, self.back_img)
        cv2.accumulateWeighted(f_frame, self.back_img, self.update_rate)
        return diff_frame.astype(np.uint8)

    def salt_pepper_noise(self, _img):

        dst = _img.copy()
        #numpy.random.randint(low, high=None, size=None, dtype='l')
        num_salt = np.ceil(self.amount * _img.size * self.s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in _img.shape]
        dst[coords[:-1]] = (255, 255, 255)

        num_pepper = np.ceil(self.amount * _img.size * (1. - self.s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in _img.shape]
        dst[coords[:-1]] = (0, 0, 0)

        return dst


class CameraStreamer:

    ### init
    def init(self):
        self.sensor = 0
        self.width = 640
        self.height = 480
        self.recode_on = -1

        self.flag_prev_img = False

        ##
        self.acm_img_list = deque([])

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
        dst = self.ip.background_diff(_img)
        cv2.imshow("back", self.ip.back_img.astype(np.uint8))
        return dst

    def do_opticalflow(self, _img):

        if self.flag_prev_img == False:
            self.flag_prev_img = True
            self.prevgray = _img
        flow = cv2.calcOpticalFlowFarneback(self.prevgray, _img, None, 0.5, 3, 10, 3, 7, 1.5, 0)
        #(prev, next, flow(None), pyrScale(0.5), levels(3), winsize(15), iterations(3), polyN(5), polySigma, flags)
        self.prevgray = _img

        return flow

    def draw_flow(self, img, flow, step=8):
        h, w = img.shape[:2]
        y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
        fx, fy = flow[y, x].T
        lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
        lines = np.int32(lines + 0.5)
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.polylines(vis, lines, 0, (0, 255, 0))
        for (x1, y1), (_x2, _y2) in lines:
            cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
        return vis

    def draw_hsv(self, flow):
        h, w = flow.shape[:2]
        fx, fy = flow[:, :, 0], flow[:, :, 1]
        ang = np.arctan2(fy, fx) + np.pi
        v = np.sqrt(fx * fx + fy * fy)
        hsv = np.zeros((h, w, 3), np.uint8)
        hsv[..., 0] = ang * (180 / np.pi / 2)
        hsv[..., 1] = 255
        hsv[..., 2] = np.minimum(v * 4, 255)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr

    def accumulateImage(self, _img, accumulate_frame = 10, frame_ratio = 3.5):

        ### init
        if len(self.acm_img_list) < 1:
            self.acm_img = np.zeros_like(_img, np.float32)

        ### list update
        self.acm_img_list.append(_img.astype(np.float32))
        if len(self.acm_img_list) > accumulate_frame:
            self.acm_img_list.popleft()

        ### accumulate motion area
        for i in range(len(self.acm_img_list)):
            ratio = frame_ratio * (i+1) / accumulate_frame
            cv2.accumulate(self.acm_img_list[i] * ratio, self.acm_img)
        self.acm_img = self.acm_img / len(self.acm_img_list)
        coord = self.acm_img > 255
        self.acm_img[coord] = 255

        return self.acm_img.astype(np.uint8)

    def do_imageProcessing(self, _img):
        noise_img = self.ip.salt_pepper_noise(_img)
        g_img = cv2.cvtColor(noise_img, cv2.COLOR_RGB2GRAY)
        flow = self.do_opticalflow(g_img)

        flow_img = self.draw_hsv(flow)
        flow_img = cv2.dilate(flow_img, kernel=np.ones((3, 3), np.uint8), iterations=3)
        flow_img = cv2.GaussianBlur(flow_img, ksize=(5, 5), sigmaX=3.0)

        accumulate_img = self.accumulateImage(flow_img)

        cv2.imshow('Accumulate Motion Image', accumulate_img)

    def set_init_data(self, _img):
        pass

    ### main
    def videoCameraView(self):
        cap = cv2.VideoCapture(self.sensor)
        ret, img = cap.read()

        self.set_init_data(img)
        skip_num = 0

        while True:
            ret, img = cap.read()
            for i in range(skip_num): cap.read()

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



if __name__ == "__main__":

    #VIDEODATA = "http://10.232.163.38/mjpg/1/video.mjpg"
    #VIDEODATA = "http://10.232.163.38/jpg/1/image.jpg"
    #VIDEODATA = "20180124_143122.avi"
    VIDEODATA = 0

    cam = CameraStreamer()
    cam.init()
    cam.set_sensor(VIDEODATA)
    #cam.set_recoding_mode(0) # 0(movie) or 1(frame)

    cam.videoCameraView()
    #cam.frameCameraView()