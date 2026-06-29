import supervision as sv
import cv2
import sys
import os

counter = {}
# pending1 = set()
# pending2 = set()

drawn_line1: sv.LineZone
# drawn_line2: sv.LineZone
line1: sv.LineZone
# line2: sv.LineZone
line_annotator = sv.LineZoneAnnotator()

def initialize_counter(classes: tuple[str],
                       start1: tuple[int],
                       end1: tuple[int],
                    #    start2: tuple[int],
                    #    end2: tuple[int],
                       resize_info: dict[str, float | int]):
    global drawn_line1, line1, counter

    for c in classes:
        counter[c] = 0
    
    # pending1 = set()
    # pending2 = set()

    drawn_line1 = sv.LineZone(
        start=sv.Point(start1[0], start1[1]),
        end=sv.Point(end1[0], end1[1])
    )

    # drawn_line2 = sv.LineZone(
    #     start=sv.Point(start2[0], start2[1]),
    #     end=sv.Point(end2[0], end2[1])
    # )

    map_lineal = lambda x, y: (int(resize_info["left"] + resize_info["scale"] * x),
                               int(resize_info["top"] + resize_info["scale"] * y))
    
    real_start1 = map_lineal(start1[0], start1[1])
    real_end1 = map_lineal(end1[0], end1[1])
    # real_start2 = map_lineal(start2[0], start2[1])
    # real_end2 = map_lineal(end2[0], end2[1])

    line1 = sv.LineZone(
        triggering_anchors=[sv.Position.CENTER],
        start=sv.Point(real_start1[0], real_start1[1]),
        end=sv.Point(real_end1[0], real_end1[1])
    )

    # line2 = sv.LineZone(
    #     minimum_crossing_threshold=0.5,
    #     start=sv.Point(real_start2[0], real_start2[1]),
    #     end=sv.Point(real_end2[0], real_end2[1])
    # )

def count_detections(detections: sv.Detections, names):

    print("TRACKER IDs:", detections.tracker_id)
    print("CLASS IDs:", detections.class_id)

    global line1, counter
    
    (in1, out1) = line1.trigger(detections)
    # (in2, out2) = line2.trigger(detections)

    detections_in1 = set(zip(detections[in1].class_id, detections[in1].tracker_id))
    detections_out1 = set(zip(detections[out1].class_id, detections[out1].tracker_id))

    for det in detections_in1 | detections_out1:
        class_name = names[det[0]]
        counter[class_name] += 1

    # detections_in2 = set(zip(detections[in2].class_id, detections[in2].tracker_id))
    # detections_out2 = set(zip(detections[out2].class_id, detections[out2].tracker_id))

    # for det in detections_in2:
    #     if det not in pending1:
    #         continue

    #     class_name = names[det[0]]

    #     counter[class_name] += 1
    #     pending1.remove(det)

    # for det in detections_out1:
    #     if det not in pending2:
    #         continue

    #     class_name = names[det[0]]

    #     counter[class_name] += 1
    #     pending2.remove(det)

    # pending1.update(detections_in1)
    # pending2.update(detections_out2)

def draw_line(img: cv2.Mat) -> cv2.Mat:
    global drawn_line1, line1
    
    annotated_img = img.copy()

    drawn_line1._in_count_per_class = line1.in_count_per_class
    drawn_line1._out_count_per_class = line1.out_count_per_class
    
    # drawn_line2.in_count_per_class.update(line2.in_count_per_class)
    # drawn_line2.out_count_per_class.update(line2.out_count_per_class)

    annotated_img = line_annotator.annotate(annotated_img, drawn_line1)
    # annotated_img = line_annotator.annotate(annotated_img, drawn_line2)

    return annotated_img
