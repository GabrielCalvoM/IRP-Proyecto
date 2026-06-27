import supervision as sv
import trackers as tr
from ultralytics.engine.results import Results

tracker = tr.ByteTrackTracker()

def initialize_tracker():
    tracker.reset()

def track_frame(frame_results: Results) -> sv.Detections:
    global tracker

    detections = sv.Detections.from_ultralytics(frame_results)
    updated_detections = tracker.update(detections)
    updated_detections["names"] = {class_id: frame_results.names[class_id] for class_id in updated_detections.class_id}
    
    return updated_detections
    