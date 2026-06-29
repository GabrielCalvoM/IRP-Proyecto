import supervision as sv
import cv2
import sys
import os

counted_ids = set()
counter = {}

drawn_line1: sv.LineZone
line1: sv.LineZone
line_annotator = sv.LineZoneAnnotator()

def initialize_counter(classes: tuple[str],
                       start1: tuple[int],
                       end1: tuple[int],
                       resize_info: dict[str, float | int]):
    global drawn_line1, line1, counter, counted_ids

    for c in classes:
        counter[c] = 0

    drawn_line1 = sv.LineZone(
        start=sv.Point(start1[0], start1[1]),
        end=sv.Point(end1[0], end1[1])
    )


    map_lineal = lambda x, y: (int(resize_info["left"] + resize_info["scale"] * x),
                               int(resize_info["top"] + resize_info["scale"] * y))
    
    real_start1 = map_lineal(start1[0], start1[1])
    real_end1 = map_lineal(end1[0], end1[1])

    line1 = sv.LineZone(
        minimum_crossing_threshold=2,
        triggering_anchors=[sv.Position.BOTTOM_CENTER],
        start=sv.Point(real_start1[0], real_start1[1]),
        end=sv.Point(real_end1[0], real_end1[1])
    
    )

    counted_ids.clear()


def count_detections(detections: sv.Detections, names):

    print("TRACKER IDs:", detections.tracker_id)
    print("CLASS IDs:", detections.class_id)

    global line1, counter
    
    (in1, out1) = line1.trigger(detections)

    detections_in1 = set(zip(detections[in1].class_id, detections[in1].tracker_id))
    detections_out1 = set(zip(detections[out1].class_id, detections[out1].tracker_id))

    for class_id, tracker_id in detections_in1 | detections_out1:

        if tracker_id in counted_ids:
            continue

        counted_ids.add(tracker_id)

        class_name = names[class_id]

        counter[class_name] += 1

        print(
            f"CONTADO -> ID={tracker_id} "
            f"Clase={class_name}"
        )


def draw_line(img: cv2.Mat) -> cv2.Mat:
    global drawn_line1, line1
    
    annotated_img = img.copy()

    drawn_line1._in_count_per_class = line1.in_count_per_class
    drawn_line1._out_count_per_class = line1.out_count_per_class

    annotated_img = line_annotator.annotate(annotated_img, drawn_line1)

    return annotated_img
