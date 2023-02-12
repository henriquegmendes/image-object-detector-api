import os
from typing import Any, List

import cv2
import numpy as np

from settings import settings
from utils import create_dir_if_not_exists

config = settings()


yolo_opencv_singleton = None

def get_yolo_opencv():
    global yolo_opencv_singleton

    if not yolo_opencv_singleton:
        labels_path = os.path.sep.join(['yolo', config.yolo_labels_filename])
        config_path = os.path.sep.join(['yolo', config.yolo_config_filename])
        weights_path = os.path.sep.join(['yolo', config.yolo_weights_filename])
        yolo_opencv_singleton = YoloOpenCV(labels_path, config_path, weights_path)

    return yolo_opencv_singleton

class YoloOpenCV:
    _labels_path: str
    _config_path: str
    _weights_path: str

    labels: List[str]
    colors: Any

    net: Any
    net_out_layer_names: List[str]


    def __init__(self, labels_path, config_path, weights_path):
        self._labels_path = labels_path
        self._config_path = config_path
        self._weights_path = weights_path

        self.labels = open(self._labels_path).read().strip().split('\n')
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype=np.uint8)

        self.net = cv2.dnn.readNet(self._config_path, self._weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        net_layer_names = self.net.getLayerNames()
        net_out_layers = self.net.getUnconnectedOutLayers()
        self.net_out_layer_names = [net_layer_names[i - 1] for i in net_out_layers]


    def process_image_and_get_dnn_layer_outputs(self, img_path):
        img = cv2.imread(img_path)

        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)

        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.net_out_layer_names)

        return img, layer_outputs

    @classmethod
    def create_np_array(cls, data: List[Any]):
        return np.array(data)

    @classmethod
    def get_arg_max(cls, data: List[Any]):
        return np.argmax(data)


    @classmethod
    def get_boxes_without_suppression(cls, boxes, confidences, threshold, threshold_nms):
        return cv2.dnn.NMSBoxes(boxes, confidences, threshold, threshold_nms)

    @classmethod
    def mark_object_boxes(cls, img, class_color, class_name, confidence, x, y, width, height):
        text = f'{class_name}: {str(confidence)}'
        text_background = np.full((img.shape), (0, 0, 0), dtype=np.uint8)

        text_box_y = y - 5 if y - 5 >= 0 else y + 12
        cv2.putText(text_background, text, (x, text_box_y), 0, 0.5, (255, 255, 255), 2)
        fx, fy, fw, fh = cv2.boundingRect(text_background[:, :, 2])

        cv2.rectangle(img, (x, y), (x + width, y + height), class_color, 2)

        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), class_color, -1)
        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), class_color, 3)

        cv2.putText(img, text, (x, text_box_y), 0, 0.5, (0, 0, 0), 2)

    @classmethod
    def save_image(cls, path, file_name, image):
        create_dir_if_not_exists(path)
        full_path = os.path.sep.join([path, file_name])
        cv2.imwrite(full_path, image)
