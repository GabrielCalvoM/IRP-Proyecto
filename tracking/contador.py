import supervision as sv

counter = {}
pending1 = set()
pending2 = set()

line1: sv.LineZone
line2: sv.LineZone

def initialize_counter(classes: tuple[str],
                       start1: tuple[int],
                       end1: tuple[int],
                       start2: tuple[int],
                       end2: tuple[int]):
    global line1, line2, counter, pending1, pending2

    for c in classes:
        counter[c] = 0
    
    pending1 = []
    pending2 = []

    line1 = sv.LineZone(start1, end1)
    line2 = sv.LineZone(start2, end2)

def count_detections(detections: sv.Detections):
    global line1, line2, counter, pending1, pending2
    
    (in1, out1) = line1.trigger(detections)
    (in2, out2) = line2.trigger(detections)

    detections_in1 = set([x[3:5] for x in detections[in1]])
    detections_out2 = set([x[3:5] for x in detections[out2]]) - detections_in1

    detections_in2 = set([x[3:5] for x in detections[in2]])
    detections_out1 = set([x[3:5] for x in detections[out1]]) - detections_in2

    for det in detections_in2:
        if det not in pending1:
            continue

        class_id = det[0]
        class_name = detections["names"][class_id]
        counter[class_name] += 1
        pending1.remove(det)

    for det in detections_out1:
        if det not in pending2:
            continue

        class_id = det[0]
        class_name = detections["names"][class_id]
        counter[class_name] += 1
        pending2.remove(det)

    pending1.update(detections_in1)
    pending2.update(detections_out2)
