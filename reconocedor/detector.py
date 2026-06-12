from ultralytics import YOLO
from ultralytics.engine.results import Results, Boxes
import cv2

model = YOLO("modelos/yolo26l.pt")
vehicle_classes = [1, 2, 3, 5, 7]

def identify_img(normalized_img: cv2.Mat):
    global model

    results = model.predict(normalized_img, classes=vehicle_classes)

    return results[0]

def filter_classes(result: Results, filter_list: list[int] = vehicle_classes):
    mask = [int(clase) in filter_list for clase in result.boxes.cls]

    result.boxes = result.boxes[mask]

    return result

def set_boxes(img: cv2.Mat, result: Results, resize_info: dict[str, float | int]) -> cv2.Mat :
    boxes = result.boxes

    clases = boxes.cls.tolist()
    confs = boxes.conf.tolist()
    coords = boxes.xyxy.tolist()

    new_img = img

    for i in range(len(boxes)):
        clase = clases[i]
        conf = confs[i]
        x1, y1, x2, y2 = boxes.xyxy[i].tolist()

        x1, x2 = x1 - resize_info["left"], x2 - resize_info["left"]
        y1, y2 = y1 - resize_info["top"], y2 - resize_info["top"]
        x1, y1, x2, y2 = int(x1 // resize_info["scale"]), int(y1 // resize_info["scale"]), int(x2 // resize_info["scale"]), int(y2 // resize_info["scale"])

        box_color = (0, 255, 0)
        
        new_img = cv2.rectangle(new_img, (x1, y1), (x2, y2), box_color, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        (text_width, text_height), baseline = cv2.getTextSize(result.names[clase], font, font_scale, 1)

        cv2.rectangle(new_img, (x1, y1 - text_height - 10), (x1 + text_width, y1), box_color, -1)
        cv2.putText(new_img, result.names[clase], (x1, y1 - 5), font, font_scale, (255, 255, 255), 1, cv2.LINE_AA)

    return new_img
