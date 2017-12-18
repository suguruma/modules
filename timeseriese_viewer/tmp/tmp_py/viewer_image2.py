#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import skimage.io
from PyQt5.QtGui import *

skimg = skimage.io.imread('lena.png')

# convert to QImage (skimg can be grayscale or rgb)
h, w = skimg.shape[:2]
qimg_format = QImage.Format_RGB888 if len(skimg.shape) == 3 else QImage.Format_Indexed8
qimg = QImage(skimg.flatten(), w, h, qimg_format)

# if you can assure that skimg has 3 channels, this conversion can be just like:
# qimg = QImage(skimg.flatten(), skimg.shape[1], skimg.shape[0], QImage.Format_RGB888)


# re-convert to ndarray
skimg_ret = numpy.array(qimg.constBits()).reshape(skimg.shape)

assert (skimg == skimg_ret).all()