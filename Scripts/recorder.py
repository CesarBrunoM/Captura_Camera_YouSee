import cv2
import datetime
import os

def start_recording(frame, base_path="videos"):
    os.makedirs(base_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(base_path, f"movimento_{timestamp}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    height, width = frame.shape[:2]
    out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
    return out, filename