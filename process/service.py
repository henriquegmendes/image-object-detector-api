import os
import uuid

from fastapi import HTTPException

import utils
from pkg import get_yolo_opencv as yolo, YoloOpenCV
from process import request

image_mime_type = 'image/jpeg'
result_files_path = 'tmp/results'
downloaded_files_path = 'tmp/downloads'


def process_layers_by_threshold(image, layers, threshold):
    boxes = []
    confidences = []
    classes = []
    (H, W) = image.shape[:2]

    for output in layers:
        for detection in output:
            scores = detection[5:]
            class_idx = YoloOpenCV.get_arg_max(scores)
            class_confidence = scores[class_idx]

            if class_confidence > threshold:
                box = detection[0:4] * YoloOpenCV.create_np_array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype('int')
                x = int(center_x - (width / 2))
                x = x if x >= 0 else 0
                y = int(center_y - (height / 2))
                y = y if y >= 0 else 0

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(class_confidence))
                classes.append(class_idx)

    return boxes, confidences, classes


def generate_results(img, boxes_without_suppression, boxes, confidences, classes):
    result = []
    for box_idx in boxes_without_suppression:
        box_data = {
            "class": yolo().labels[classes[box_idx]],
            "confidence": confidences[box_idx],
            "bounding_box": {
                "x_center": boxes[box_idx][0],
                "y_center": boxes[box_idx][1],
                "width": boxes[box_idx][2],
                "height": boxes[box_idx][3],
            },
        }

        result.append(box_data)

        bounding_box = box_data['bounding_box']
        class_color = [int(c) for c in yolo().colors[classes[box_idx]]]
        YoloOpenCV.mark_object_boxes(img,
                                     class_color,
                                     box_data['class'],
                                     box_data['confidence'],
                                     bounding_box['x_center'],
                                     bounding_box['y_center'],
                                     bounding_box['width'],
                                     bounding_box['height'])

    return result


async def process_image(req: request.ProcessImageRequest, threshold_nms: float) -> dict:
    process_id = uuid.uuid4()

    file_to_process = utils.download_file(downloaded_files_path, req.image_url, f'{process_id}.{req.file_extension}')

    img, layer_outputs = yolo().process_image_and_get_dnn_layer_outputs(file_to_process)

    boxes, confidences, classes = process_layers_by_threshold(img, layer_outputs, req.threshold)

    boxes_without_suppression = YoloOpenCV.get_boxes_without_suppression(boxes, confidences, req.threshold,
                                                                         threshold_nms)

    result = []
    if len(boxes_without_suppression) > 0:
        result = generate_results(img, boxes_without_suppression, boxes, confidences, classes)

    YoloOpenCV.save_image(result_files_path, f'/{process_id}.jpg', img)

    utils.delete_file(file_to_process)

    return {
        'id': process_id,
        'external_id': req.external_id,
        'status': 'success',
        'output': result,
    }


def static_file_by_path(process_id: str):
    file_path = os.path.sep.join([result_files_path, f'{process_id}.jpg'])
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f'File {file_path} does not exist')

    return file_path, image_mime_type
