#!/bin/bash

rm -rf yolo \
&& mkdir yolo \
&& git clone https://github.com/AlexeyAB/darknet \
&& cp darknet/cfg/yolov4.cfg yolo/ \
&& cp darknet/data/coco.names yolo/ \
&& rm -rf darknet \
&& cd yolo \
&& wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights \
&& cd ..
