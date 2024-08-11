import sys

import cv2
import requests
from ultralytics import YOLO
import subprocess
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


def detect_objects(input_video, temp_output_video, final_output_video, num_frames, confidence_threshold, verb, model_name):
    model = YOLO(model_name)  # Load YOLOv8 model
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open input video {input_video}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Use 'mp4v' codec for temporary output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_video, fourcc, fps, (width, height))

    frame_count = 0
    people_count_avg = 0
    while cap.isOpened() and frame_count < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=confidence_threshold, verbose=False)
        people_count = 0
        for result in results[0].boxes:
            x1, y1, x2, y2 = result.xyxy[0]
            conf = result.conf[0]
            cls = result.cls[0]
            label = f'{model.names[int(cls)]} {conf:.2f}'
            if model.names[int(cls)] == "person":
                people_count += 1
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, 'People count: {}'.format(people_count), (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        out.write(frame)
        #print('Detecting {} frame from {}'.format(frame_count, num_frames))
        if verb:
            print(f"Processed {frame_count} frames and saved to {temp_output_video}")
        sys.stdout.flush()
        frame_count += 1
        people_count_avg = max(people_count, people_count_avg)

    cap.release()
    out.release()
    print(f"Processed {frame_count} frames and saved to {temp_output_video}")

    # Re-encode the video to H.264 using ffmpeg
    ffmpeg_command = [
        'ffmpeg', '-loglevel', 'error', '-y', '-i', temp_output_video, '-c:v', 'libx264', '-crf', '23', '-preset',
        'fast', final_output_video
    ]

    subprocess.run(ffmpeg_command)
    print(f"Re-encoded video saved to {final_output_video}")
    # people_count_avg = round(people_count_avg/frame_count)
    print(f"People avg per frame is {people_count_avg}")
    return people_count_avg


if __name__ == "__main__":
    input_video = "input.mp4"
    temp_output_video = "temp_output.mp4"
    final_output_video = "output.mp4"

    specific_time = datetime.now()
    specific_time_str = specific_time.strftime('%Y%m%d%H%M%S')
    video_url = create_webcam_url(specific_time_str)
    download_video(video_url, input_video)

    detect_objects(input_video, temp_output_video, final_output_video, num_frames=10)
