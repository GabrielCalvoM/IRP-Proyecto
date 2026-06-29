import supervision as sv
import trackers as tr
from ultralytics.engine.results import Results
import os

tracker = tr.ByteTrackTracker()

def initialize_tracker():
    tracker.reset()

def track_frame(frame_results):

    detections = sv.Detections.from_ultralytics(frame_results)

    updated_detections = tracker.update(detections)
    # os.write(1, f"Track IDs: {updated_detections.tracker_id}\n".encode())

    return updated_detections, frame_results.names
    