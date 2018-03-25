import numpy as np
import cv2

class ImageProcessing:
    def __init__(self, parent = None):
        pass

    def open_img(self, file):
        img = cv2.imread(file)
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #R<->B
        return img, img_color

    def save_img(self, file, _img):
        cv2.imwrite(file, _img)

    # Grayscale
    def grayscale(self, src):
        if len(src.shape) == 3:
            return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        else:
            return src
    # Flip
    def flip(self, src):
        return cv2.flip(src, 1)

    # Affine
    def translation(self, src):
        mat = np.float32([[1, 0, -100], [0, 1, 50]])
        dst = cv2.warpAffine(src, mat, (src.shape[1], src.shape[0]))
        return dst

    # Edge Detection
    def sobelX(self, src):
        return cv2.Sobel(src, cv2.CV_8U, 1, 0, ksize=3)
    def sobelY(self, src):
        return cv2.Sobel(src, cv2.CV_8U, 0, 1, ksize=3)
    def laplacian(self, src):
        return cv2.Laplacian(src, cv2.CV_8U, ksize=3)

    # Canny Edge Detection
    def canny(self, src):
        if len(src.shape) == 3:
            img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(img, 100, 200)
            edges2 = np.zeros_like(src)
            for i in (0,1,2):
                edges2[:,:,i] = edges
            dst = cv2.addWeighted(src, 1, edges2, 0.4,0)
            return dst

        else:
            edges = cv2.Canny(src, 100, 200)
            dst = cv2.addWeighted(src, 1, edges, 0.4,0)
            return dst

if __name__ == '__main__':
    file = "../lena.jpg"
    a = opencv_ip()
    b,c = a.open_img(file)
    d = a.canny(b)
    cv2.imshow("",d)
    cv2.waitKey(0)
    cv2.destroyAllWindows()