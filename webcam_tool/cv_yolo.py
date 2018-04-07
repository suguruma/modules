#! /usr/bin/env python

import argparse
import colorsys
import os
import random

import numpy as np
from keras import backend as K
from keras.models import load_model
from PIL import Image, ImageDraw

from yad2k.models.keras_yolo import yolo_eval, yolo_head

import cv2

parser = argparse.ArgumentParser(
    description='Run a YOLO_v2 style detection model on test images..')
parser.add_argument(
    '-m',
    '--model_path',
    help='path to h5 model file containing body of a YOLO_v2 model',
    default='model_data/yolo.h5')
parser.add_argument(
    '-a',
    '--anchors_path',
    help='path to anchors file, defaults to yolo_anchors.txt',
    default='model_data/yolo_anchors.txt')
parser.add_argument(
    '-c',
    '--classes_path',
    help='path to classes file, defaults to coco_classes.txt',
    default='model_data/coco_classes.txt')
parser.add_argument(
    '-t',
    '--test_path',
    help='path to directory of test images, defaults to images/',
    default='images')
parser.add_argument(
    '-o',
    '--output_path',
    help='path to output test images, defaults to images/out',
    default='images/out')
parser.add_argument(
    '-s',
    '--score_threshold',
    type=float,
    help='threshold for bounding box scores, default .3',
    default=.3)
parser.add_argument(
    '-iou',
    '--iou_threshold',
    type=float,
    help='threshold for non max suppression IOU, default .5',
    default=.5)

class YOLOV2:

    sensor = 0
    cap = cv2.VideoCapture(0)
    class_names = None
    is_fixed_size = None
    model_image_size = None
    input_image_shape = None
    sess = None
    boxes = None
    scores = None
    classes = None
    yolo_model = None

    cv_img = None
    resize_on = None
    width = 240
    height = 320

    def init(self):
        args = parser.parse_args()
        model_path = os.path.expanduser(args.model_path)
        assert model_path.endswith('.h5'), 'Keras model must be a .h5 file.'
        anchors_path = os.path.expanduser(args.anchors_path)
        classes_path = os.path.expanduser(args.classes_path)
        test_path = os.path.expanduser(args.test_path)
        output_path = os.path.expanduser(args.output_path)
        self.sess = K.get_session()  # TODO: Remove dependence on Tensorflow session.

        with open(classes_path) as f:
            self.class_names = f.readlines()
        self.class_names = [c.strip() for c in self.class_names]

        with open(anchors_path) as f:
            anchors = f.readline()
            anchors = [float(x) for x in anchors.split(',')]
            anchors = np.array(anchors).reshape(-1, 2)

        self.yolo_model = load_model(model_path)

        # Verify model, anchors, and classes are compatible
        num_classes = len(self.class_names)
        num_anchors = len(anchors)
        # TODO: Assumes dim ordering is channel last
        model_output_channels = self.yolo_model.layers[-1].output_shape[-1]
        assert model_output_channels == num_anchors * (num_classes + 5), \
            'Mismatch between model and given anchor and class sizes. ' \
            'Specify matching anchors and classes with --anchors_path and ' \
            '--classes_path flags.'
        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Check if model is fully convolutional, assuming channel last order.
        self.model_image_size = self.yolo_model.layers[0].input_shape[1:3]
        self.is_fixed_size = self.model_image_size != (None, None)

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        random.seed(10101)  # Fixed seed for consistent colors across runs.
        random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        # TODO: Wrap these backend operations with Keras layers.
        yolo_outputs = yolo_head(self.yolo_model.output, anchors, len(self.class_names))
        self.input_image_shape = K.placeholder(shape=(2, ))
        self.boxes, self.scores, self.classes = yolo_eval(
            yolo_outputs,
            self.input_image_shape,
            score_threshold=args.score_threshold,
            iou_threshold=args.iou_threshold)

        self.cap = cv2.VideoCapture(self.sensor)

    def set_sensor(self, _sensor):
        self.sensor = _sensor

    def set_size(self, _width=320, _height=240):
        self.width = _width
        self.height = _height

    def detection(self):
        ret, img = self.cap.read()
        if ret == False:
            self.cap.release()
            return -1

        if self.resize_on:
            img = cv2.resize(img, (self.width, self.height))

        image = Image.fromarray(img)
        if self.is_fixed_size:  # TODO: When resizing we can use minibatch input.
            resized_image = image.resize(
                tuple(reversed(self.model_image_size)), Image.BICUBIC)
            image_data = np.array(resized_image, dtype='float32')
        else:
            # Due to skip connection + max pooling in YOLO_v2, inputs must have width and height as multiples of 32.
            new_image_size = (image.width - (image.width % 32), image.height - (image.height % 32))
            resized_image = image.resize(new_image_size, Image.BICUBIC)
            image_data = np.array(resized_image, dtype='float32')
            print(image_data.shape)

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        #print('Found {} boxes for {}'.format(len(out_boxes), image_file))
        thickness = (image.size[0] + image.size[1]) // 300

        for i, c in reversed(list(enumerate(out_classes))):

            if not self.class_names[c] == "person":
                continue

            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)

            draw = ImageDraw.Draw(image)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            #print(label, (left, top), (right, bottom))

            for i in range(thickness):
                draw.rectangle([left + i, top + i, right - i, bottom - i], outline=(50, 200, 50))
            del draw

        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)

        return img

    def proc_end(self):
        self.sess.close()


if __name__ == '__main__':

    run = YOLOV2()
    run.init()
    run.detection()
    run.proc_end()
