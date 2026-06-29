import supervision as sv
import trackers as tr
from ultralytics.engine.results import Results

tracker = tr.ByteTrackTracker()

def initialize_tracker():
    tracker.reset()

def track_frame(frame_results):

    detections = sv.Detections.from_ultralytics(frame_results)

    updated_detections = tracker.update(detections)

    return updated_detections, frame_results.names
    