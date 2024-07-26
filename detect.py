import cv2
from ultralytics import YOLO
import requests
from datetime import datetime
from utils import create_webcam_url


def download_video(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded video to {output_path}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")


def detect_objects(input_video, output_video, num_frames=30):
    model = YOLO("yolov8n.pt")  # Load YOLOv8 model
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open input video {input_video}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Use H.264 codec for output video
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened() and frame_count < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, verbose=False)
        for result in results[0].boxes:
            x1, y1, x2, y2 = result.xyxy[0]
            conf = result.conf[0]
            cls = result.cls[0]
            label = f'{model.names[int(cls)]} {conf:.2f}'
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    print(f"Processed {frame_count} frames and saved to {output_video}")


if __name__ == "__main__":
    input_video = "input.mp4"
    output_video = "output.mp4"  # Ensure it saves to static directory
    specific_time = datetime.now()
    specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
    video_url = create_webcam_url(specific_time_str)
    download_video(video_url, input_video)
    detect_objects(input_video, output_video, num_frames=10)
