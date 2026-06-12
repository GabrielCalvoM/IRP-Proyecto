from ultralytics import YOLO
from ultralytics.engine.results import Results, Boxes
import torch
import cv2

model = YOLO("modelos/yolo26l.pt")
vehicle_classes = [1, 2, 3, 5, 7]

def yolo_detector(normalized_img: cv2.Mat) -> Results :
    global model

    results = model.predict(normalized_img)

    return results[0]

def filter_classes(result: Results, filter_list: list[int] = vehicle_classes) -> Results :
    mask = torch.isin(result.boxes.cls, torch.tensor(filter_list))

    result.boxes = result.boxes[mask]

    return result

def filter_conf(result: Results, filter_threshold: float = 0.5) -> Results :
    mask = result.boxes.conf > filter_threshold

    result.boxes = result.boxes[mask]

    return result

def identify_img(normalized_img: cv2.Mat, filter_list: list[int] = vehicle_classes, filter_threshold: int = 0.5) -> Results:
    result = yolo_detector(normalized_img)
    result = filter_classes(result, filter_list)
    result = filter_conf(result, filter_threshold)

    return result

def set_boxes(img: cv2.Mat, result: Results, resize_info: dict[str, float | int]) -> cv2.Mat :
    boxes = result.boxes

    new_img = img

    for box in boxes:
        clase = int(box.cls)
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        x1, x2 = x1 - resize_info["left"], x2 - resize_info["left"]
        y1, y2 = y1 - resize_info["top"], y2 - resize_info["top"]
        x1, y1, x2, y2 = int(x1 // resize_info["scale"]), int(y1 // resize_info["scale"]), int(x2 // resize_info["scale"]), int(y2 // resize_info["scale"])

        box_color = (0, 255, 0)
        
        cv2.rectangle(new_img, (x1, y1), (x2, y2), box_color, 2)
        height, width = img.shape[:2]

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = min((height, width)) / 1000
        (text_width, text_height), baseline = cv2.getTextSize(result.names[clase], font, font_scale, 1)

        cv2.rectangle(new_img, (x1, y1 - text_height - 10), (x1 + text_width, y1), box_color, -1)
        cv2.putText(new_img, result.names[clase], (x1, y1 - 5), font, font_scale, (255, 255, 255), 1, cv2.LINE_AA)

    return new_img
